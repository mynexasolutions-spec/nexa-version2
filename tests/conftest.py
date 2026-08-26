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
