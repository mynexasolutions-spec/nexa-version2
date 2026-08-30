import importlib
import sys

import pytest


def make_blog(app_module, *, title, slug, published, views=0):
    from models import BlogPost, Category

    category = Category.query.filter_by(name="Preview").first()
    if category is None:
        category = Category(name="Preview")
        app_module.db.session.add(category)
        app_module.db.session.flush()
    post = BlogPost(
        title=title,
        slug=slug,
        summary=f"Summary for {title}",
        content=f"<p>Content for {title}</p>",
        author_name="Nexa",
        category=category,
        is_published=published,
        view_count=views,
    )
    app_module.db.session.add(post)
    app_module.db.session.commit()
    return post.id


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "password")

    for module_name in ("app", "api.index"):
        sys.modules.pop(module_name, None)

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with app_module.app.app_context():
        app_module.db.create_all()

    with app_module.app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            sess["_user_id"] = "admin:1"
            sess["_fresh"] = True
        yield test_client


def test_public_nav_footer_and_converter_links_render(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Tools" in html
    assert "WebP Converter" in html
    assert "/converter" in html
    assert "Website Development Agency India" in html
    assert "/best-website-development-agency-india/" in html


def test_converter_displays_batch_limit(client):
    response = client.get("/converter")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Up to 100 images per batch" in html
    assert "/static/js/converter.js" in html
    assert "/static/css/converter.css" in html
    assert "Conversion runs one image at a time" in client.get("/static/js/converter.js").get_data(as_text=True)


def test_converter_uses_shared_layout_and_unique_seo(client):
    response = client.get("/converter")
    html = response.get_data(as_text=True)

    assert "Nexa Image to WebP Converter" in html
    assert 'rel="canonical"' in html and "/converter" in html
    assert '"@type":"WebApplication"' in html
    assert "Nothing is uploaded to a server" in html
    assert "Explore web development" in html
    assert "footer" in html.lower()
    assert 'id="drop-zone" class="converter-drop-zone" aria-describedby="format-note"' in html
    assert 'id="drop-zone" class="converter-drop-zone" role="button"' not in html
    assert 'id="browse-btn" type="button"' in html


def test_converter_is_indexable_and_listed_in_sitemap(client):
    robots = client.get("/robots.txt").get_data(as_text=True)
    sitemap = client.get("/sitemap.xml").get_data(as_text=True)

    assert "Disallow: /converter" not in robots
    assert "/converter</loc>" in sitemap


@pytest.mark.parametrize("published", [False, True])
def test_admin_blog_preview_supports_drafts_and_published_without_counting_view(client, published):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        blog_id = make_blog(
            app_module,
            title="Draft Preview" if not published else "Published Preview",
            slug="draft-preview" if not published else "published-preview",
            published=published,
            views=7,
        )

    response = client.get(f"/admin/blogs/{blog_id}/preview")
    assert response.status_code == 200
    assert ("Draft Preview" if not published else "Published Preview") in response.get_data(as_text=True)

    with app_module.app.app_context():
        from models import BlogPost

        assert app_module.db.session.get(BlogPost, blog_id).view_count == 7


def test_admin_blog_preview_requires_auth_and_returns_404(client):
    missing = client.get("/admin/blogs/999999/preview")
    assert missing.status_code == 404

    with client.session_transaction() as session:
        session.clear()
    protected = client.get("/admin/blogs/999999/preview")
    assert protected.status_code in {302, 401}


def test_blog_list_has_views_and_accessible_preview_action(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        blog_id = make_blog(app_module, title="Visible Article", slug="visible-article", published=False, views=23)

    html = client.get("/admin/blogs").get_data(as_text=True)

    assert 'class="bl-th-views">Views' in html
    assert 'class="bl-views">23' in html
    assert f'/admin/blogs/{blog_id}/preview' in html
    assert 'rel="noopener"' in html
    assert 'aria-label="Preview Visible Article in a new tab"' in html


def test_lead_status_and_delete_alignment_hooks_render(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        app_module.db.session.add(
            app_module.ContactLead(
                name="Aligned Lead",
                email="aligned@example.com",
                subject="Project",
                message="A long message should not move the controls out of alignment.",
            )
        )
        app_module.db.session.commit()

    html = client.get("/admin/leads").get_data(as_text=True)

    assert 'class="lead-status-cell"' in html
    assert 'class="actions lead-actions-cell"' in html


def test_admin_blog_form_has_inline_category_creation(client):
    response = client.get("/admin/blogs/new")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Add category" in html
    assert "new-category-name" in html
    assert "/admin/categories/inline" in html


def test_inline_category_create_rejects_blank_and_duplicate(client):
    blank = client.post("/admin/categories/inline", json={"name": "  "})
    assert blank.status_code == 400
    assert blank.get_json()["error"] == "Enter a category name."

    created = client.post("/admin/categories/inline", json={"name": "Growth"})
    assert created.status_code == 201
    assert created.get_json()["name"] == "Growth"

    duplicate = client.post("/admin/categories/inline", json={"name": "growth"})
    assert duplicate.status_code == 409
    assert duplicate.get_json()["error"] == "Category already exists."


def test_lead_delete_route_removes_lead(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        lead = app_module.ContactLead(
            name="Test Lead",
            email="lead@example.com",
            subject="Project",
            message="Hello",
        )
        app_module.db.session.add(lead)
        app_module.db.session.commit()
        lead_id = lead.id

    response = client.post(f"/admin/leads/{lead_id}/delete", follow_redirects=True)

    assert response.status_code == 200
    assert "Lead deleted." in response.get_data(as_text=True)
    with app_module.app.app_context():
        assert app_module.db.session.get(app_module.ContactLead, lead_id) is None


def test_project_detail_contains_post_delete_action(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from models import Project

        project = Project(
            name="Site Refresh",
            client_name="Nexa",
            status="active",
            total_value=1000,
            advance_received=200,
        )
        app_module.db.session.add(project)
        app_module.db.session.commit()
        project_id = project.id

    response = client.get(f"/admin/projects/{project_id}")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert f"/admin/projects/{project_id}/delete" in html
    assert "Delete this project?" in html
