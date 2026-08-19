"""Fixtures: configured browser context with tracing, failure artifacts attached to Allure."""

import logging
import re
import sys
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.config.settings import get_settings
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage

ARTIFACTS_DIR = Path("test-artifacts")


@pytest.fixture(scope="session", autouse=True)
def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


@pytest.fixture(scope="session", autouse=True)
def allure_environment() -> None:
    """Fill the Allure report's Environment widget with run settings (no secrets)."""
    settings = get_settings()
    entries = {
        "Base URL": settings.base_url,
        "Standard User": settings.standard_user,
        "Browser": "chromium",
        "Headless": str(settings.headless),
        "Timeout": f"{settings.timeout:g}s",
    }
    Path("allure-results").mkdir(exist_ok=True)
    (Path("allure-results") / "environment.properties").write_text(
        "\n".join(f"{key}={value}" for key, value in entries.items()), encoding="utf-8"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, Any, None]:
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def context(browser: Browser, browser_context_args: dict[str, Any]) -> Iterator[BrowserContext]:
    """Context with tracing enabled from the very first action."""
    context = browser.new_context(**browser_context_args)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Iterator[Page]:
    settings = get_settings()
    page = context.new_page()
    page.set_default_timeout(settings.timeout * 1000)
    yield page

    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        ARTIFACTS_DIR.mkdir(exist_ok=True)
        allure.attach(
            page.screenshot(full_page=True),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    trace_path = ARTIFACTS_DIR / f"{request.node.name}-trace.zip"
    context.tracing.stop(path=str(trace_path))
    if failed:
        allure.attach.file(
            str(trace_path), name="playwright-trace", attachment_type="application/zip"
        )


@pytest.fixture
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.base_url = get_settings().base_url
    login_page.open()
    login_page.expect_loaded()
    return login_page


@pytest.fixture
def inventory_page(page: Page, login_page: LoginPage) -> InventoryPage:
    """Logs in via UI and waits for the inventory page to fully load."""
    login_page.login_as_standard_user(get_settings().password)
    # regex, not glob: a relative glob resolves against base_url and never matches
    expect(page).to_have_url(re.compile(r"/inventory\.html"), timeout=10000)
    inventory_page = InventoryPage(page)
    inventory_page.base_url = get_settings().base_url
    inventory_page.expect_loaded()
    return inventory_page
