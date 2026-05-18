# Pre-entrega Automation Testing - SauceDemo

Proyecto de automatizacion QA para la pre-entrega del curso. El objetivo es validar flujos basicos de navegacion web en [SauceDemo](https://www.saucedemo.com/) usando Python, Pytest y Selenium WebDriver.

## Tecnologias utilizadas

- Python 3.10 o superior
- Pytest
- Selenium WebDriver
- Pytest HTML
- Git y GitHub

## Casos automatizados

- Login exitoso con el usuario `standard_user`.
- Validacion de redireccion a `/inventory.html`.
- Validacion del titulo `Swag Labs` y encabezado `Products`.
- Verificacion de productos visibles en el catalogo.
- Obtencion del nombre y precio del primer producto.
- Validacion de elementos importantes de la interfaz: menu, filtro y carrito.
- Agregado del primer producto al carrito.
- Validacion del contador del carrito.
- Verificacion del producto agregado dentro del carrito.

## Estructura del proyecto

```text
.
├── requirements.txt
├── pytest.ini
├── README.md
├── reports/
│   └── screenshots/
├── tests/
│   ├── conftest.py
│   └── test_saucedemo.py
└── utils/
    └── saucedemo_page.py
```

## Instalacion

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion de pruebas

Ejecutar todas las pruebas y generar el reporte HTML:

```bash
pytest
```

Comando equivalente:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Para ejecutar sin abrir una ventana visible de Chrome:

```bash
pytest --headless
```

## Reportes y evidencias

- El reporte HTML se genera en `reports/reporte.html`.
- Si falla una prueba, se guarda una captura automatica en `reports/screenshots/`.

## Datos de prueba

Credenciales usadas en SauceDemo:

- Usuario: `standard_user`
- Password: `secret_sauce`

## Entrega en GitHub

Nombre sugerido del repositorio:

```text
pre-entrega-automation-testing-nombre-apellido
```

Se recomienda realizar commits frecuentes con mensajes descriptivos, por ejemplo:

```bash
git add .
git commit -m "Crear estructura inicial del proyecto"
git commit -m "Agregar pruebas de login e inventario"
git commit -m "Agregar validacion de carrito y reporte HTML"
```
