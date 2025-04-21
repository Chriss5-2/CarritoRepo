# tests/test_cupon.py
import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

@pytest.mark.parametrize("desc_porcentaje, desc_maximo, prod, cumple", [
    (20, 50, "producto_impresora", True),
    (-5, 50, "producto_impresora", False),
    (-5, -50, "producto_impresora", False),
    (150, 50, "producto_impresora", False),
    (150, -50, "producto_impresora", False),
])
def test_aplicar_cupon_con_limite(carrito, desc_porcentaje, desc_maximo, prod, cumple, request):
    """
    Red: Se espera que al aplicar un cupón, el descuento no supere el límite máximo.
    """
    # Arrange
    producto = request.getfixturevalue(prod)
    carrito.agregar_producto(producto, cantidad=2)  # Total = 400

    # Act & Assert
    if cumple:
        total_con_cupon = carrito.aplicar_cupon(desc_porcentaje, desc_maximo)  # 20% de 400 = 80, pero límite es 50
        assert total_con_cupon == 350.00
    else:
        with pytest.raises(ValueError):
            carrito.aplicar_cupon(desc_porcentaje, desc_maximo)
