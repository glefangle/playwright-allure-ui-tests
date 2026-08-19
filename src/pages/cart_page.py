"""Cart and checkout pages of saucedemo.com."""

import re

from playwright.sync_api import Page, expect

from src.pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator("span.title", has_text="Your Cart")
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    url_pattern = re.compile(r"/cart\.html")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(self.url_pattern)
        expect(self.title).to_be_visible()

    def expect_item_in_cart(self, item_name: str) -> None:
        expect(self.page.locator(".inventory_item_name", has_text=item_name)).to_be_visible()

    def expect_items_count(self, count: int) -> None:
        expect(self.cart_items).to_have_count(count)

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.postal_code = page.get_by_role("textbox", name="Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.get_by_role("heading", name="Thank you for your order!")

    url_pattern = re.compile(r"/checkout-step-one\.html")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(self.url_pattern)
        expect(self.first_name).to_be_visible()

    def fill_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def expect_order_completed(self) -> None:
        expect(self.complete_header).to_be_visible()
