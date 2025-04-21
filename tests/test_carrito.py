## Ejemplo de prueba
# tests/test_carrito.py

import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

def test_agregar_producto_nuevo(carrito, producto_laptop):
    """
    AAA:
    Arrange: Se crea un carrito y se genera un producto.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que el carrito contiene un item con el producto y cantidad 1.
    """
    # Arrange & Act
    carrito.agregar_producto(producto_laptop)

    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].producto.nombre == "Laptop"
    assert items[0].cantidad == 1

def test_agregar_producto_existente_incrementa_cantidad(carrito, producto_mouse):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se agrega el mismo producto nuevamente aumentando la cantidad.
    Assert: Se verifica que la cantidad del producto se incrementa en el item.
    """
    # Arrange
    carrito.agregar_producto(producto_mouse, cantidad=1)
    
    # Act
    carrito.agregar_producto(producto_mouse, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3

def test_remover_producto(carrito, producto_teclado):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con cantidad 3.
    Act: Se remueve una unidad del producto.
    Assert: Se verifica que la cantidad del producto se reduce a 2.
    """
    # Arrange
    carrito.agregar_producto(producto_teclado, cantidad=3)
    
    # Act
    carrito.remover_producto(producto_teclado, cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 2

def test_remover_producto_completo(carrito, producto_monitor):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se remueve la totalidad de la cantidad del producto.
    Assert: Se verifica que el producto es eliminado del carrito.
    """
    # Arrange
    carrito.agregar_producto(producto_monitor, cantidad=2)
    
    # Act
    carrito.remover_producto(producto_monitor, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0

def test_actualizar_cantidad_producto(carrito, producto_auriculares):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 5.
    Assert: Se verifica que la cantidad se actualiza correctamente.
    """
    # Arrange
    carrito.agregar_producto(producto_auriculares, cantidad=1)
    
    # Act
    carrito.actualizar_cantidad(producto_auriculares, nueva_cantidad=5)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 5

def test_actualizar_cantidad_a_cero_remueve_producto(carrito, producto_cargador):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 0.
    Assert: Se verifica que el producto se elimina del carrito.
    """
    # Arrange
    carrito.agregar_producto(producto_cargador, cantidad=3)
    
    # Act
    carrito.actualizar_cantidad(producto_cargador, nueva_cantidad=0)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0

def test_calcular_total(carrito, producto_impresora, producto_escaner):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos con distintas cantidades.
    Act: Se calcula el total del carrito.
    Assert: Se verifica que el total es la suma correcta de cada item (precio * cantidad).
    """
    # Arrange
    producto2 = ProductoFactory(nombre="", precio=150.00)
    carrito.agregar_producto(producto_impresora, cantidad=2)  # Total 400
    carrito.agregar_producto(producto_escaner, cantidad=1)  # Total 150
    
    # Act
    total = carrito.calcular_total()
    
    # Assert
    assert total == 550.00

@pytest.mark.parametrize("porcentaje, esperado, es_valido", [
    (0, 1000.00, True),
    (10, 900.00, True),
    (100, 0.00, True),
    (-10, None, False),
    (150, None, False)
])
# Como usamos los valores de conftest.py, producto_tablet ya está definido con un precio de $500.00
def test_aplicar_descuento_parametrizado(carrito, producto_tablet, porcentaje, esperado, es_valido):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con una cantidad determinada.
    Act: Se aplica un descuento del según 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Arrange
    carrito.agregar_producto(producto_tablet, cantidad=2)  # Total 1000
    # Act & Assert
    # La condicional sirve para decidir si deberá comprobar un valor esperado o esperar un error
    if es_valido:
        total = carrito.aplicar_descuento(porcentaje)
        assert total == esperado
    else:
        with pytest.raises(ValueError):
            carrito.aplicar_descuento(porcentaje)

def test_vaciar_carrito(carrito, producto_smartphone, producto_iphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan productos
    Act: Se vacía el carrito
    Assert: Se verifica que el carrito esté vacío
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    carrito.agregar_producto(producto_iphone, cantidad=1)

    # Act
    carrito.vaciar()
    items = carrito.obtener_items()

    # Assert
    assert len(items)==0 and carrito.calcular_total() == 0

def test_aplicar_descuento_condicionado(carrito, producto_smartphone, producto_iphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan productos
    Act: Se verifica si cumple los requisitos para aplicar un descuento
    Assert: Se verifica si el costo total es menor al inicial
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    carrito.agregar_producto(producto_iphone, cantidad=1)

    # Act
    monto_antes = carrito.calcular_total()
    monto_actual = carrito.aplicar_descuento_condicional(porcentaje=15, minimo=500)

    # Assert
    assert monto_actual < monto_antes

def test_NO_aplicar_descuento_condicionado(carrito, producto_yogurt, producto_mochila):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan productos
    Act: Se verifica si cumple los requisitos para aplicar un descuento
    Assert: Se verifica que el costo actual es igual al inicial
    """
    # Arrange
    carrito.agregar_producto(producto_yogurt, cantidad=1)
    carrito.agregar_producto(producto_mochila, cantidad=1)

    # Act
    monto_antes = carrito.calcular_total()
    monto_actual = carrito.aplicar_descuento_condicional(porcentaje=15, minimo=500)

    # Assert
    assert monto_actual == monto_antes

def test_hay_stock(carrito, producto_smartphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un productp
    Act: Se agregan se agrega el mismo producto
    Assert: Se verifica que no supere el stock
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    # Act
    carrito.agregar_producto(producto_smartphone, cantidad=2)
    items = carrito.obtener_items()
    # Assert
    assert len(items)==1 and items[0].cantidad<=items[0].producto.stock

def test_NO_hay_stock(carrito, producto_smartphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un productp
    Act: Se agregan se agrega el mismo producto
    Assert: Se verifica que ocurre un error al superar el stock
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    # Act & Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto_smartphone, cantidad=5)

def test_items_ordenados_por_precio(carrito, producto_smartphone, producto_iphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan dos productos
    Act: Se ordenan de acuerdo al precio
    Assert: Se verifica que los precios vayan de orden ascedente
    """
    # Arrange
    carrito.agregar_producto(producto_iphone, cantidad=1) #1000
    carrito.agregar_producto(producto_smartphone, cantidad=1) #800
    # Act
    items = carrito.obtener_items_ordenados("precio")
    # Assert
    assert items[0].producto.precio < items[1].producto.precio

def test_items_ordenados_por_nombre(carrito, producto_smartphone, producto_iphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan dos productos
    Act: Se ordenan de acuerdo al nombre
    Assert: Se verifica que los nombres vayan de orden ascedente
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    carrito.agregar_producto(producto_iphone, cantidad=1)
    # Act
    items = carrito.obtener_items_ordenados("nombre")
    # Assert
    assert items[0].producto.nombre < items[1].producto.nombre

def test_items_ordenados_por_criterio_equivocado(carrito, producto_smartphone, producto_iphone):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan dos productos
    Act: Se ordenan de acuerdo a un criterio que no existe
    Assert: Se verifica que los precios vayan de orden ascedente
    """
    # Arrange
    carrito.agregar_producto(producto_smartphone, cantidad=1)
    carrito.agregar_producto(producto_iphone, cantidad=1)
    # Act & Assert
    with pytest.raises(ValueError):
        items = carrito.obtener_items_ordenados("criterioOtro")
