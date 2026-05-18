from utils.saucedemo_page import SauceDemoPage


def test_login_exitoso_redirige_a_inventario(driver, base_url):
    sauce_demo = SauceDemoPage(driver, base_url)

    sauce_demo.open_login_page()
    sauce_demo.login()

    assert sauce_demo.is_inventory_page_loaded(), (
        "El login debe redirigir a /inventory.html y mostrar Products / Swag Labs."
    )


def test_catalogo_muestra_productos_y_controles(driver, base_url):
    sauce_demo = SauceDemoPage(driver, base_url)

    sauce_demo.login_as_standard_user()
    products = sauce_demo.get_visible_products()
    first_product_name, first_product_price = sauce_demo.get_first_product_name_and_price()

    assert driver.title == "Swag Labs"
    assert len(products) > 0, "Debe existir al menos un producto visible en el catalogo."
    assert first_product_name, "El primer producto debe tener nombre visible."
    assert first_product_price.startswith("$"), "El primer producto debe mostrar precio."
    assert sauce_demo.catalog_controls_are_visible(), "Menu, filtro y carrito deben estar visibles."


def test_agregar_primer_producto_al_carrito(driver, base_url):
    sauce_demo = SauceDemoPage(driver, base_url)

    sauce_demo.login_as_standard_user()
    added_product_name = sauce_demo.add_first_product_to_cart()
    cart_counter = sauce_demo.get_cart_counter()
    sauce_demo.open_cart()
    cart_product_names = sauce_demo.get_cart_product_names()

    assert cart_counter == "1", "El contador del carrito debe incrementarse a 1."
    assert added_product_name in cart_product_names, "El producto agregado debe aparecer en el carrito."
