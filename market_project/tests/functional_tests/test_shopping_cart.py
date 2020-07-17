import os
import time

import environ
import pytest


@pytest.mark.parametrize("wait_time", (.2,))
@pytest.mark.skipif(environ.Env(CI=(bool, False), ), reason="CircleCI/Codecov")
def test_shopping_cart(driver, live_server, product, featured_product, order, wait_time):
    driver.get(live_server.url)
    time.sleep(wait_time)
    # Only featured products should be visible in home
    assert featured_product.name in driver.page_source
    assert product.name not in driver.page_source

    # Test buying 2 featured products
    driver.find_element_by_link_text(featured_product.name).click()
    time.sleep(wait_time)
    assert featured_product.name in driver.title
    driver.find_element_by_class_name("buy-now").click()
    time.sleep(wait_time)
    assert "1" in driver.find_element_by_class_name("count").text
    driver.find_element_by_class_name("buy-now").click()
    assert "2" in driver.find_element_by_class_name("count").text
    time.sleep(wait_time)

    # And then one non featured product
    driver.find_element_by_link_text("CATALOG").click()
    time.sleep(wait_time)
    assert "Shop" in driver.title
    driver.find_element_by_link_text(product.name).click()
    time.sleep(wait_time)
    assert product.name in driver.title
    driver.find_element_by_class_name("buy-now").click()
    assert "3" in driver.find_element_by_class_name("count").text

    # Go to the shopping cart
    driver.find_element_by_class_name("site-cart").click()
    time.sleep(wait_time)
    assert product.name in driver.page_source
    assert featured_product.name in driver.page_source

    # Test that the products' quantities, subtotals and total price are displayed correctly

    product_quantity = "/html/body/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[4]/div/input"
    product_subtotal = "/html/body/div[3]/div/div[2]/div[1]/div/div/div[2]/div[2]/strong"
    featured_product_quantity = "/html/body/div[3]/div/div[1]/div/div/table/tbody/tr[2]/td[4]/div/input"
    featured_product_subtotal = "/html/body/div[3]/div/div[2]/div[1]/div/div/div[3]/div[2]/strong"
    total = "/html/body/div[3]/div/div[2]/div[1]/div/div/div[5]/div[2]/strong"
    assert driver.find_element_by_xpath(product_quantity).get_attribute("value") == "1"
    assert driver.find_element_by_xpath(product_subtotal).text == f"${product.price}"
    assert driver.find_element_by_xpath(featured_product_quantity).get_attribute("value") == "2"
    assert driver.find_element_by_xpath(featured_product_subtotal).text == f"${2 * featured_product.price}"
    assert driver.find_element_by_xpath(total).text == f"${2 * featured_product.price + product.price}"

    # Proceeds to checkout

    driver.find_element_by_partial_link_text("PROCEED").click()
    time.sleep(wait_time)
    driver.find_element_by_name("name").send_keys(order.customer_name)
    time.sleep(wait_time)
    driver.find_element_by_name("address").send_keys(order.customer_address.replace("\n", ""))
    time.sleep(wait_time)
    driver.find_element_by_name("email").send_keys(order.customer_email)
    time.sleep(wait_time)
    driver.find_element_by_tag_name("button").click()
    assert "Thank you!" in driver.page_source
    time.sleep(wait_time)
