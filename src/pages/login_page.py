"""Login page of saucedemo.com."""

from playwright.sync_api import Page, expect

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.get_by_role("textbox", name="username")
        self.password_input = page.get_by_role("textbox", name="password")
        self.login_button = page.get_by_role("button", name="login")
        # Error text is rendered inside an h3[data-test=error] block
        self.error_message = page.locator("[data-test='error']")

    def expect_loaded(self) -> None:
        expect(self.login_button).to_be_visible()
        expect(self.username_input).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as_standard_user(self, password: str) -> None:
        from src.config.settings import get_settings

        self.login(get_settings().standard_user, password)

    def expect_error(self, text: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)
