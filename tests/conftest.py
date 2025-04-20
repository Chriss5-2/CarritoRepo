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
