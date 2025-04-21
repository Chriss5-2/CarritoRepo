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

@pytest.mark.parametrize("porcentaje, minimo, cumple, prod1, prod2", [
    (15, 500, True, "producto_smartphone", "producto_iphone"),
    (15, 500, False, "producto_yogurt", "producto_mochila")
])
def test_aplicar_descuento_condiciocado_parametrizado(carrito, prod1, prod2, porcentaje, minimo, cumple, request):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan productos
    Act: Se verifica si cumple los requisitos para aplicar un descuento
    Assert: Se verifica si cumple o no y luego verifica si el costo total es menor al inicial o si son iguales
    """
    # Arrange
    producto1 = request.getfixturevalue(prod1)
    producto2 = request.getfixturevalue(prod2)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    monto_antes = carrito.calcular_total()
    # Act
    monto_actual = carrito.aplicar_descuento_condicional(porcentaje, minimo)
    # Assert
    if cumple:
        assert monto_actual < monto_antes
    else:
        assert monto_actual == monto_antes

@pytest.mark.parametrize("cantidad1, cantidad2, prod, sin_stock", [
    (1, 2, "producto_smartphone", False),
    (1, 5, "producto_smartphone", True),
])
def test_verificar_stock_parametrizado(carrito, prod, cantidad1, cantidad2, sin_stock, request):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un productp
    Act: Se agregan se agrega el mismo producto
    Assert: Se verifica que no supere el stock
    """
    # Arrange
    producto = request.getfixturevalue(prod)
    carrito.agregar_producto(producto, cantidad1)

    #Act & Assert
    if sin_stock:
        with pytest.raises(ValueError):
            carrito.agregar_producto(producto, cantidad2)
    else:
        carrito.agregar_producto(producto, cantidad2)
        items = carrito.obtener_items()
        assert len(items)==1
        assert items[0].cantidad <= producto.stock

@pytest.mark.parametrize("prod1, prod2, criterio, ordena",[
    ("producto_smartphone", "producto_mochila", "precio", True),
    ("producto_smartphone", "producto_mochila", "nombre", True),
    ("producto_smartphone", "producto_mochila", "stock", False),
])
def test_items_ordenar_por_criterio_parametrizado(carrito, prod1, prod2, criterio, ordena, request):
    """
    AAA:
    Arrange: Se crea un carrito y se agregan dos productos
    Act: Se ordenan de acuerdo al precio
    Assert: Se verifica que los precios vayan de orden ascedente
    """
    # Arrange
    producto1 = request.getfixturevalue(prod1)
    producto2 = request.getfixturevalue(prod2)
    carrito.agregar_producto(producto1, cantidad=1) # Precio 1000, Nombre Smartphone
    carrito.agregar_producto(producto2, cantidad=1) # Precio 200.5, Nombre Mochila
    # Act
    if ordena:
        items = carrito.obtener_items_ordenados(criterio)
        # El getattr nos ayuda a acceder al atributo indicado como texto
        valor1 = getattr(items[0].producto, criterio)
        valor2 = getattr(items[1].producto, criterio)
        assert valor1 <= valor2
    else:
        with pytest.raises(ValueError):
            carrito.obtener_items_ordenados(criterio)

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