import importlib
import sys

import pytest


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
    assert "MAX_IMAGES = 100" in html
    assert "Conversion runs one image at a time" in html


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
