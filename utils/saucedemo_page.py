from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SauceDemoPage:
    """Funciones de navegacion e interaccion reutilizables para SauceDemo."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    INVENTORY_TITLE = (By.CLASS_NAME, "title")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    SORT_FILTER = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    FIRST_PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    FIRST_PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".inventory_item button")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_ITEM = (By.CLASS_NAME, "cart_item")

    def __init__(self, driver, base_url="https://www.saucedemo.com/", timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open_login_page(self):
        """Navega a la pagina principal de login."""
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def login(self, username="standard_user", password="secret_sauce"):
        """Ingresa credenciales validas y envia el formulario de login."""
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login_as_standard_user(self):
        """Atajo usado por los tests que necesitan partir desde inventario."""
        self.open_login_page()
        self.login()
        self.wait_for_inventory_page()

    def wait_for_inventory_page(self):
        """Espera la redireccion y confirma que la vista de inventario cargo."""
        self.wait.until(EC.url_contains("/inventory.html"))
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_TITLE))

    def is_inventory_page_loaded(self):
        """Valida URL, encabezado del catalogo y logo principal de la aplicacion."""
        current_url = self.driver.current_url
        page_title = self.wait.until(EC.visibility_of_element_located(self.INVENTORY_TITLE)).text
        app_logo = self.wait.until(EC.visibility_of_element_located(self.APP_LOGO)).text
        return "/inventory.html" in current_url and page_title == "Products" and app_logo == "Swag Labs"

    def catalog_controls_are_visible(self):
        """Comprueba controles importantes de la interfaz del catalogo."""
        menu_visible = self.wait.until(EC.visibility_of_element_located(self.BURGER_MENU)).is_displayed()
        filter_visible = self.wait.until(EC.visibility_of_element_located(self.SORT_FILTER)).is_displayed()
        cart_visible = self.wait.until(EC.visibility_of_element_located(self.CART_LINK)).is_displayed()
        return menu_visible and filter_visible and cart_visible

    def get_visible_products(self):
        """Devuelve los productos visibles en la pagina de inventario."""
        return self.wait.until(EC.visibility_of_all_elements_located(self.INVENTORY_ITEM))

    def get_first_product_name_and_price(self):
        """Obtiene nombre y precio del primer producto visible."""
        first_product = self.get_visible_products()[0]
        name = first_product.find_element(*self.FIRST_PRODUCT_NAME).text
        price = first_product.find_element(*self.FIRST_PRODUCT_PRICE).text
        return name, price

    def add_first_product_to_cart(self):
        """Agrega al carrito el primer producto del catalogo y devuelve su nombre."""
        first_product = self.get_visible_products()[0]
        product_name = first_product.find_element(*self.FIRST_PRODUCT_NAME).text
        first_product.find_element(*self.ADD_TO_CART_BUTTON).click()
        self.wait.until(EC.text_to_be_present_in_element(self.CART_BADGE, "1"))
        return product_name

    def get_cart_counter(self):
        """Lee el contador visible del carrito."""
        return self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text

    def open_cart(self):
        """Navega al carrito de compras."""
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()
        self.wait.until(EC.url_contains("/cart.html"))

    def get_cart_product_names(self):
        """Devuelve los nombres de productos visibles dentro del carrito."""
        self.wait.until(EC.visibility_of_all_elements_located(self.CART_ITEM))
        return [item.text for item in self.driver.find_elements(*self.FIRST_PRODUCT_NAME)]
