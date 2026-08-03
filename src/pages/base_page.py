"""Base page: navigation and shared state for all page objects."""

from playwright.sync_api import Page


class BasePage:
    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url: str = ""  # injected by fixtures

    def open(self) -> None:
        self.page.goto(f"{self.base_url}{self.path}")

    @property
    def url(self) -> str:
        return self.page.url
