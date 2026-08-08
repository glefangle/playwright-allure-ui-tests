"""Inventory (product listing) page of saucedemo.com."""

import re

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.locator("span.title", has_text="Products")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.inventory_items = page.locator(".inventory_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")

    url_pattern = re.compile(r"/inventory\.html")

    def expect_loaded(self) -> None:
        # a glob would resolve against base_url and never match, so use a regex
        expect(self.page).to_have_url(self.url_pattern)
        expect(self.title).to_be_visible()
        expect(self.inventory_items).to_have_count(6)

    def _item_card(self, item_name: str) -> Locator:
        """Locator of one product card, scoped by the product's display name."""
        return self.page.locator(
            ".inventory_item",
            has=self.page.locator(".inventory_item_name", has_text=item_name),
        )

    def add_to_cart(self, item_name: str) -> None:
        self._item_card(item_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, item_name: str) -> None:
        self._item_card(item_name).get_by_role("button", name="Remove").click()

    def sort_by(self, option_value: str) -> None:
        self.sort_dropdown.select_option(option_value)

    def open_cart(self) -> None:
        self.page.locator(".shopping_cart_link").click()

    def get_item_prices(self) -> list[float]:
        return [float(text.removeprefix("$")) for text in self.item_prices.all_inner_texts()]
