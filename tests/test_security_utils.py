from security_utils import (
    LoginRateLimiter,
    admin_ip_login_limiter,
    admin_login_limiter,
)


def test_admin_login_limiter_allows_nine_failures_and_limits_the_tenth():
    limiter = LoginRateLimiter(max_attempts=10, window_seconds=900)
    key = "admin:127.0.0.1:admin"

    for _ in range(9):
        limiter.record_failure(key)

    assert limiter.is_limited(key) is False

    limiter.record_failure(key)

    assert limiter.is_limited(key) is True


def test_admin_ip_limiter_allows_thirty_nine_failures_and_limits_the_fortieth():
    limiter = LoginRateLimiter(max_attempts=40, window_seconds=900)
    key = "admin:ip:127.0.0.1"

    for _ in range(39):
        limiter.record_failure(key)

    assert limiter.is_limited(key) is False

    limiter.record_failure(key)

    assert limiter.is_limited(key) is True


def test_reset_clears_a_login_lockout():
    limiter = LoginRateLimiter(max_attempts=2, window_seconds=900)
    key = "admin:127.0.0.1:admin"
    limiter.record_failure(key)
    limiter.record_failure(key)

    assert limiter.is_limited(key) is True

    limiter.reset(key)

    assert limiter.is_limited(key) is False


def test_admin_limiters_use_the_configured_thresholds():
    assert admin_login_limiter.max_attempts == 10
    assert admin_login_limiter.window.total_seconds() == 900
    assert admin_ip_login_limiter.max_attempts == 40
    assert admin_ip_login_limiter.window.total_seconds() == 900
