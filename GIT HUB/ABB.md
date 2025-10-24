ÁRBOL BINARIO DE BÚSQUEDA (ABB)

Un Árbol Binario de Búsqueda (ABB) es una estructura de datos que organiza la información de manera jerárquica, permitiendo realizar operaciones de búsqueda, inserción y eliminación de forma rápida y ordenada. Cada elemento o nodo del árbol contiene un valor o clave única, y puede tener como máximo dos hijos: uno izquierdo y uno derecho.

El principio fundamental del ABB es que todos los valores que se encuentran en el subárbol izquierdo de un nodo son menores que el valor del nodo, mientras que todos los valores que se encuentran en el subárbol derecho son mayores. Gracias a esta regla, el ABB facilita la localización de un dato sin necesidad de recorrer todos los elementos, ya que en cada comparación se reduce el espacio de búsqueda a la mitad.

El árbol se maneja de la siguiente forma:

Nodo raíz: es el primer nodo insertado en el árbol. A partir de este se organizan los demás.

Inserción: si el nuevo valor es menor que el valor del nodo actual, se coloca en el subárbol izquierdo; si es mayor, se coloca en el subárbol derecho. Si el valor ya existe, no se puede insertar porque el ABB no permite valores repetidos.

Búsqueda: se compara el valor que se busca con el nodo actual. Si es igual, se ha encontrado el dato; si es menor, se busca por la izquierda; y si es mayor, se busca por la derecha.

Recorrido: el árbol puede recorrerse de distintas maneras (inorden, preorden o postorden). Por ejemplo, el recorrido inorden muestra los valores de menor a mayor.

EJEMPLO CON NIÑOS

Supongamos que queremos crear un ABB donde cada nodo representa a un niño. Cada niño tiene tres datos: un ID, un nombre y una edad. El ID será un número único que se usará como clave principal del árbol. Este ID no se puede repetir y debe ser numérico, ya que el árbol usa el valor del ID para decidir si el nuevo nodo se coloca a la izquierda o a la derecha.

PASO A PASO

Insertamos al primer niño, que será la raíz del árbol:
Niño: ID = 10, Nombre: Lucas, Edad: 7.
Lucas se convierte en la raíz del árbol.

Insertamos otro niño:
Niño: ID = 6, Nombre: Sofía, Edad: 5.
Como 6 es menor que 10, Sofía se coloca a la izquierda de Lucas.

Insertamos otro niño:
Niño: ID = 15, Nombre: Mateo, Edad: 8.
Como 15 es mayor que 10, Mateo se coloca a la derecha de Lucas.

Insertamos otro niño:
Niño: ID = 4, Nombre: Valentina, Edad: 6.
Se compara con la raíz (10): 4 es menor que 10, por lo tanto va a la izquierda (donde está Sofía).
Luego se compara con 6: 4 es menor que 6, por lo tanto se coloca a la izquierda de Sofía.

El árbol quedaría de la siguiente manera:

            [10 - Lucas]
           /             \
    [6 - Sofía]       [15 - Mateo]
       /
[4 - Valentina]


CASO DE ID REPETIDO

Si intentamos agregar un niño con el mismo ID que otro, por ejemplo:
Niño: ID = 10, Nombre: Andrés, Edad: 9.
El árbol no permitirá la inserción porque ya existe un nodo con el ID 10 (el de Lucas).
En un Árbol Binario de Búsqueda cada ID debe ser único, ya que es el valor que determina la posición y las comparaciones de los nodos.

https://keepcoding.io/blog/arboles-binarios-en-programacion/ te puedes apoyar de este enlace para entender mejor el concepto de ABB. 