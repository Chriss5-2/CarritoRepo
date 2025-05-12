import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

@pytest.fixture
def carrito():
    return Carrito()


@pytest.fixture
def producto_generico():
    return ProductoFactory(nombre="Genérico", precio=100.00)

@pytest.fixture
def producto_laptop():
    return ProductoFactory(nombre="Laptop", precio=1000.00)

@pytest.fixture
def producto_mouse():
    return ProductoFactory(nombre="Mouse", precio=50.00)

@pytest.fixture
def producto_teclado():
    return ProductoFactory(nombre="Teclado", precio=75.00)

@pytest.fixture
def producto_monitor():
    return ProductoFactory(nombre="Monitor", precio=300.00)

@pytest.fixture
def producto_auriculares():
    return ProductoFactory(nombre="Auriculares", precio=150.00)

@pytest.fixture
def producto_cargador():
    return ProductoFactory(nombre="Cargador", precio=25.00)

@pytest.fixture
def producto_impresora():
    return ProductoFactory(nombre="Impresora", precio=200.00)

@pytest.fixture
def producto_escaner():
    return ProductoFactory(nombre="Escáner", precio=150.00)

@pytest.fixture
def producto_tablet():
    return ProductoFactory(nombre="Tablet", precio=500.00)

@pytest.fixture
def producto_smartphone():
    return ProductoFactory(nombre="Smartphone", precio=800.00, stock=5)

@pytest.fixture
def producto_iphone():
    return ProductoFactory(nombre="Iphone", precio=1000.50, stock=2)

@pytest.fixture
def producto_yogurt():
    return ProductoFactory(nombre="Yogurt", precio=50.00)

@pytest.fixture
def producto_mochila():
    return ProductoFactory(nombre="Mochila", precio=200.50)

@pytest.fixture
def producto_smartwatch():
    return ProductoFactory(nombre="Smartwatch", precio=250.00)
