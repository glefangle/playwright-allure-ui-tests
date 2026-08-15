import allure
import pytest
from faker import Faker

from src.pages.cart_page import CartPage, CheckoutPage
from src.pages.inventory_page import InventoryPage

fake = Faker()


@allure.feature("Cart")
@allure.story("Cart management")
@pytest.mark.regression
def test_item_appears_in_cart(inventory_page: InventoryPage) -> None:
    with allure.step("Add a product and open the cart"):
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.open_cart()

    cart = CartPage(inventory_page.page)
    cart.base_url = inventory_page.base_url

    with allure.step("The cart contains exactly the added product"):
        cart.expect_items_count(1)
        cart.expect_item_in_cart("Sauce Labs Backpack")


@allure.feature("Checkout")
@allure.story("Order placement")
@pytest.mark.smoke
def test_full_checkout_flow(inventory_page: InventoryPage) -> None:
    first_name, last_name, postal_code = fake.first_name(), fake.last_name(), fake.zipcode()

    with allure.step("Add a product and open the cart"):
        inventory_page.add_to_cart("Sauce Labs Fleece Jacket")
        inventory_page.open_cart()
        cart = CartPage(inventory_page.page)
        cart.base_url = inventory_page.base_url
        cart.expect_items_count(1)

    with allure.step("Fill in checkout details"):
        cart.proceed_to_checkout()
        checkout = CheckoutPage(inventory_page.page)
        checkout.base_url = inventory_page.base_url
        checkout.fill_details(first_name, last_name, postal_code)

    with allure.step("Finish the order"):
        checkout.finish()
        checkout.expect_order_completed()
