import importlib
from datetime import date, timedelta


def test_project_date_fields_and_due_helpers(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from models import Project

        today = date.today()
        project = Project(
            name="Launch Site",
            client_name="Acme",
            start_date=today,
            expected_end_date=today + timedelta(days=7),
            actual_completion_date=None,
            next_payment_due_date=today + timedelta(days=5),
            status="active",
            total_value=1000,
            advance_received=0,
        )
        app_module.db.session.add(project)
        app_module.db.session.commit()

        assert project.is_due_soon(today)
        assert not project.is_overdue(today)
        assert project.is_payment_due_soon(today)

        project.expected_end_date = today - timedelta(days=1)
        project.next_payment_due_date = today - timedelta(days=1)
        app_module.db.session.commit()

        assert project.is_overdue(today)
        assert project.is_payment_overdue(today)


def test_payment_create_and_delete_updates_project_totals(client):
    app_module = importlib.import_module("app")
    with app_module.app.app_context():
        from models import Project

        project = Project(
            name="CRM Build",
            client_name="Nexa",
            status="active",
            total_value=1000,
            advance_received=100,
        )
        app_module.db.session.add(project)
        app_module.db.session.commit()
        project_id = project.id

    created = client.post(
        f"/admin/projects/{project_id}/payments",
        data={"amount": "250.00", "paid_on": "2026-08-01", "note": "Milestone"},
        follow_redirects=True,
    )
    assert created.status_code == 200
    assert "Payment added." in created.get_data(as_text=True)

    with app_module.app.app_context():
        from models import Project, ProjectPayment

        project = app_module.db.session.get(Project, project_id)
        payment = ProjectPayment.query.filter_by(project_id=project_id).one()
        assert project.collected_amount_label == "250.00"
        assert project.remaining_amount_label == "750.00"
        payment_id = payment.id

    deleted = client.post(
        f"/admin/projects/{project_id}/payments/{payment_id}/delete",
        follow_redirects=True,
    )
    assert deleted.status_code == 200
    assert "Payment deleted." in deleted.get_data(as_text=True)

    with app_module.app.app_context():
        from models import Project, ProjectPayment

        project = app_module.db.session.get(Project, project_id)
        assert ProjectPayment.query.count() == 0
        assert project.collected_amount_label == "100.00"
        assert project.remaining_amount_label == "900.00"

