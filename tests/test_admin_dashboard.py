import importlib
import json
from datetime import date, timedelta


def test_dashboard_renders_empty_state_and_charts(client):
    response = client.get("/admin/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Monthly revenue" in html
    assert "Revenue 0.00." in html
    assert "Expenses" in html
    assert "Expenses 0.00." in html
    assert html.count("bar-chart-fill bar-chart-revenue is-zero") == 6
    assert html.count("bar-chart-fill bar-chart-expense is-zero") == 6
    assert "Status distribution" in html
    assert "No projects yet." in html
    assert "Revenue collected" in html


def test_dashboard_uses_payment_revenue_and_monthly_grouping(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from models import Expense, Project, ProjectPayment

        project = Project(
            name="Storefront",
            client_name="Retail Co",
            start_date=date(2026, 8, 1),
            expected_end_date=date.today() + timedelta(days=4),
            next_payment_due_date=date.today() + timedelta(days=3),
            status="active",
            total_value=1000,
            advance_received=100,
        )
        complete = Project(
            name="Support Portal",
            client_name="Ops Co",
            start_date=date(2026, 7, 1),
            actual_completion_date=date(2026, 8, 20),
            status="completed",
            total_value=500,
            advance_received=0,
        )
        app_module.db.session.add_all([project, complete])
        app_module.db.session.flush()
        app_module.db.session.add_all([
            ProjectPayment(project=project, amount=300, paid_on=date(2026, 8, 3), note="Milestone"),
            ProjectPayment(project=complete, amount=500, paid_on=date(2026, 8, 12), note="Final"),
        ])
        app_module.db.session.add(
            Expense(
                description="Hosting",
                category="Infrastructure",
                amount=125,
                incurred_on=date(2026, 8, 15),
            )
        )
        app_module.db.session.commit()

    response = client.get("/admin/?period=12m")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "1,500.00" in html
    assert "900.00" in html
    assert "600.00" in html
    assert "Storefront" in html
    assert "Payments due soon" in html
    assert "Aug" in html
    assert "Expenses: 125.00" in html
    assert "Expenses</span><strong>125.00</strong>" in html
    assert "Net revenue</span><strong>775.00</strong>" in html


def test_expenses_sidebar_link_and_active_state(client):
    response = client.get("/admin/expenses")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'href="/admin/expenses"' in html
    assert 'class="active"' in html
    assert '>Expenses</a>' in html


def test_expense_ledger_has_scoped_responsive_layout(client):
    response = client.get("/admin/expenses")
    html = response.get_data(as_text=True)
    css = open("static/css/admin.css", encoding="utf-8").read()

    assert 'class="expense-filters"' in html
    assert 'class="expense-table-wrapper"' in html
    assert ".expense-inline-form button[type=\"submit\"] { margin: 0; }" in css


def test_vercel_enables_existing_additive_table_bootstrap():
    with open("vercel.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    assert config["env"]["ADMIN_AUTO_MIGRATE"] == "1"


def test_admin_login_password_toggle_markup(client):
    with client.session_transaction() as session:
        session.clear()

    html = client.get("/admin/login").get_data(as_text=True)

    assert 'id="admin-password"' in html
    assert 'class="password-toggle"' in html
    assert 'aria-controls="admin-password"' in html
    assert 'aria-pressed="false"' in html


def test_project_metrics_rows_and_empty_client_ring(client):
    html = client.get("/admin/projects/dashboard").get_data(as_text=True)

    charts = html.index('class="pm-grid pm-grid-charts"')
    donuts = html.index('class="pm-grid pm-grid-donuts"')
    details = html.index('class="pm-grid pm-grid-kpi-details"')
    assert charts < donuts < details
    assert 'class="pm-donut is-empty"' in html
    assert 'class="pm-donut is-empty" style="background: conic-gradient(' not in html


def test_admin_logo_has_no_added_background():
    css = open("static/css/admin.css", encoding="utf-8").read()

    logo_block = css.split(".admin-nav-brand img", 1)[1].split("}", 1)[0]
    assert "background: transparent" in logo_block
    assert "background: #fff" not in logo_block
