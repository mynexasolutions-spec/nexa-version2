import importlib
from datetime import date
from decimal import Decimal


def create_expense(client, **overrides):
    data = {
        "description": "Cloud hosting",
        "category": "Hosting",
        "amount": "125.50",
        "incurred_on": "2026-08-12",
        "notes": "August infrastructure",
    }
    data.update(overrides)
    return client.post("/admin/expenses/new", data=data, follow_redirects=True)


def test_expense_crud_and_positive_amount_validation(client):
    created = create_expense(client)
    assert created.status_code == 200
    assert "Expense added." in created.get_data(as_text=True)

    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from models import Expense

        expense = Expense.query.one()
        assert expense.description == "Cloud hosting"
        assert expense.amount == Decimal("125.50")
        expense_id = expense.id

    invalid = create_expense(client, description="Invalid", amount="0")
    assert "Expense amount must be greater than zero." in invalid.get_data(as_text=True)

    updated = client.post(
        f"/admin/expenses/{expense_id}/edit",
        data={
            "description": "Managed cloud hosting",
            "category": "Infrastructure",
            "amount": "150.00",
            "incurred_on": "2026-08-13",
            "notes": "",
        },
        follow_redirects=True,
    )
    assert "Expense updated." in updated.get_data(as_text=True)

    deleted = client.post(f"/admin/expenses/{expense_id}/delete", follow_redirects=True)
    assert "Expense deleted." in deleted.get_data(as_text=True)
    with app_module.app.app_context():
        from models import Expense

        assert Expense.query.count() == 0


def test_expense_filters_and_newest_first(client):
    create_expense(client, description="Older hosting", incurred_on="2026-07-01")
    create_expense(client, description="New design", category="Design", incurred_on="2026-08-20")
    create_expense(client, description="Newest hosting", incurred_on="2026-08-25")

    filtered = client.get("/admin/expenses?category=Hosting&date_from=2026-08-01&date_to=2026-08-31")
    html = filtered.get_data(as_text=True)
    assert "Newest hosting" in html
    assert "Older hosting" not in html
    assert "New design" not in html

    listing = client.get("/admin/expenses").get_data(as_text=True)
    assert listing.index("Newest hosting") < listing.index("New design") < listing.index("Older hosting")


def test_expense_routes_require_authentication(client):
    with client.session_transaction() as session:
        session.clear()

    response = client.get("/admin/expenses")
    assert response.status_code in {302, 401}


def test_monthly_expense_aggregation_uses_reporting_period(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from admin.routes import build_monthly_expenses
        from models import Expense

        expenses = [
            Expense(description="June", category="Ops", amount=Decimal("20.00"), incurred_on=date(2026, 6, 5)),
            Expense(description="August A", category="Ops", amount=Decimal("30.00"), incurred_on=date(2026, 8, 1)),
            Expense(description="August B", category="Tools", amount=Decimal("12.25"), incurred_on=date(2026, 8, 29)),
            Expense(description="Old", category="Ops", amount=Decimal("999.00"), incurred_on=date(2026, 2, 1)),
        ]
        result = build_monthly_expenses("6m", date(2026, 8, 29), expenses=expenses)

        assert [item["month"] for item in result] == [date(2026, month, 1) for month in range(3, 9)]
        assert result[3]["amount"] == Decimal("20.00")
        assert result[5]["amount"] == Decimal("42.25")
        assert result[5]["amount_label"] == "42.25"


def test_delete_rejects_missing_csrf_when_enabled(client):
    create_expense(client)
    app_module = importlib.import_module("app")
    app_module.app.config["WTF_CSRF_ENABLED"] = True
    try:
        response = client.post("/admin/expenses/1/delete")
        assert response.status_code in {302, 400}
        with app_module.app.app_context():
            from models import Expense

            assert Expense.query.count() == 1
    finally:
        app_module.app.config["WTF_CSRF_ENABLED"] = False
