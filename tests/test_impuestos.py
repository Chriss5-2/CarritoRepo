# tests/test_impuestos.py
import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

# REFRACTOR
@pytest.mark.parametrize("prod1, porcentaje, cumple", [
    ("producto_smartwatch", 10, True),
    ("producto_smartwatch", 110, False),
    ("producto_smartwatch", -5, False)
])
def test_calcular_impuestos(carrito, prod1, porcentaje, cumple, request):
    """
    Red: Se espera que calcular_impuestos retorne el valor del impuesto.
    """
    # Arrange
    producto = request.getfixturevalue(prod1)

    carrito.agregar_producto(producto, cantidad=4)  # Total = 1000

    # Act & Assert
    if cumple:
        impuesto = carrito.calcular_impuestos(porcentaje)  # 10% de 1000 = 100
        total_impuesto = carrito.calcular_total()*porcentaje/100 # 100
        assert impuesto == total_impuesto
    else:
        with pytest.raises(ValueError):
            carrito.calcular_impuestos(porcentaje)
