import time

import allure
import pytest

from src.config.settings import get_settings
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.smoke
def test_successful_login_redirects_to_inventory(login_page: LoginPage) -> None:
    with allure.step("Login as standard user"):
        login_page.login_as_standard_user(get_settings().password)

    with allure.step("User lands on the inventory page"):
        inventory = InventoryPage(login_page.page)
        inventory.base_url = login_page.base_url
        inventory.expect_loaded()


@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.regression
def test_performance_glitch_user_can_login_but_slowly(login_page: LoginPage) -> None:
    """saucedemo injects a multi-second delay for this user: login works, but visibly slow."""
    started_at = time.monotonic()
    with allure.step("Login as performance_glitch_user"):
        login_page.login(get_settings().performance_glitch_user, get_settings().password)

        inventory = InventoryPage(login_page.page)
        inventory.base_url = login_page.base_url
        inventory.expect_loaded()
    login_seconds = time.monotonic() - started_at

    with allure.step(f"Login took {login_seconds:.1f}s instead of a fraction of a second"):
        assert login_seconds > 2.0, "performance_glitch_user should add a noticeable delay"


@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.negative
def test_locked_user_cannot_login(login_page: LoginPage) -> None:
    with allure.step("Login as locked-out user"):
        login_page.login(get_settings().locked_user, get_settings().password)

    with allure.step("Login is rejected with an explanatory message"):
        login_page.expect_error("Sorry, this user has been locked out.")


@allure.feature("Authentication")
@allure.story("Login")
@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("wrong_user", "wrong_password", "do not match any user"),
    ],
    ids=["empty-credentials", "missing-password", "invalid-credentials"],
)
def test_invalid_login_shows_error(
    login_page: LoginPage, username: str, password: str, expected_error: str
) -> None:
    with allure.step(f"Attempt login: {username!r} / {password!r}"):
        login_page.login(username, password)

    with allure.step("Error message explains the problem"):
        login_page.expect_error(expected_error)
