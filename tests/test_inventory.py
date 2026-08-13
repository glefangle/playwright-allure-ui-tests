import allure
import pytest

from src.pages.inventory_page import InventoryPage


@allure.feature("Inventory")
@allure.story("Product listing")
@pytest.mark.smoke
def test_six_products_displayed(inventory_page: InventoryPage) -> None:
    with allure.step("Open inventory"):
        pass  # fixture already verified 6 items, keep the step for report readability

    with allure.step("All product cards have a name and a price"):
        names = inventory_page.item_names.all_inner_texts()
        prices = inventory_page.get_item_prices()
        assert len(names) == 6
        assert len(prices) == 6
        assert all(names)


@allure.feature("Inventory")
@allure.story("Sorting")
@pytest.mark.regression
def test_sort_prices_low_to_high(inventory_page: InventoryPage) -> None:
    with allure.step("Sort by Price (low to high)"):
        inventory_page.sort_by("lohi")

    with allure.step("Prices are in ascending order"):
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices)


@allure.feature("Inventory")
@allure.story("Sorting")
@pytest.mark.regression
def test_sort_prices_high_to_low(inventory_page: InventoryPage) -> None:
    with allure.step("Sort by Price (high to low)"):
        inventory_page.sort_by("hilo")

    with allure.step("Prices are in descending order"):
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices, reverse=True)


@allure.feature("Cart")
@allure.story("Add to cart")
@pytest.mark.regression
def test_add_to_cart_updates_badge(inventory_page: InventoryPage) -> None:
    with allure.step("Add two products to the cart"):
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.add_to_cart("Sauce Labs Bike Light")

    with allure.step("Cart badge shows 2"):
        assert inventory_page.shopping_cart_badge.inner_text() == "2"
