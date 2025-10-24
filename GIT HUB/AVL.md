ÁRBOL AVL (Adelson-Velsky and Landis)

Un Árbol AVL es un árbol binario de búsqueda auto-balanceado que mantiene su altura balanceada mediante rotaciones automáticas. Fue inventado en 1962 por los matemáticos soviéticos Georgy Adelson-Velsky y Evgenii Landis.

La principal característica del árbol AVL es que para cada nodo, la diferencia de altura entre su subárbol izquierdo y su subárbol derecho es como máximo 1. Esta propiedad garantiza que el árbol permanezca balanceado y que todas las operaciones se realicen en tiempo O(log n).

El árbol se maneja de la siguiente forma:

Nodo raíz: es el primer nodo insertado en el árbol. A partir de este se organizan los demás.

Factor de balance: es la diferencia entre la altura del subárbol izquierdo y la altura del subárbol derecho de un nodo. Un nodo está balanceado si su factor de balance es -1, 0 o 1.

Altura: es la distancia desde un nodo hasta su hoja más lejana. La altura de un nodo hoja es 1, y la altura de None es 0.

Inserción con auto-balanceo: cuando se inserta un nuevo nodo, el árbol verifica el factor de balance de cada nodo en el camino desde la raíz hasta el nodo insertado. Si algún nodo queda desbalanceado (factor de balance > 1 o < -1), se realizan rotaciones para restaurar el balance.

Rotaciones: son operaciones que reorganizan los nodos del árbol para mantener el balance. Existen 4 tipos de rotaciones:
  - Rotación Simple Derecha (LL): se usa cuando el desbalance está en la izquierda del hijo izquierdo
  - Rotación Simple Izquierda (RR): se usa cuando el desbalance está en la derecha del hijo derecho
  - Rotación Doble Izquierda-Derecha (LR): se usa cuando el desbalance está en la derecha del hijo izquierdo
  - Rotación Doble Derecha-Izquierda (RL): se usa cuando el desbalance está en la izquierda del hijo derecho

EJEMPLO CON NIÑOS

Supongamos que queremos crear un árbol AVL donde cada nodo representa a un niño. Cada niño tiene tres datos: un ID, un nombre y una edad. El ID será un número único que se usará como clave principal del árbol.

PASO A PASO

Insertamos al primer niño, que será la raíz del árbol:
Niño: ID = 50, Nombre: Ana, Edad: 10.
Ana se convierte en la raíz del árbol. Factor de balance = 0, Altura = 1.

Insertamos otro niño:
Niño: ID = 25, Nombre: Luis, Edad: 8.
Como 25 es menor que 50, Luis se coloca a la izquierda de Ana.
Ana: Factor de balance = 1 (izquierda=1, derecha=0). Está balanceado.

Insertamos otro niño:
Niño: ID = 75, Nombre: María, Edad: 12.
Como 75 es mayor que 50, María se coloca a la derecha de Ana.
Ana: Factor de balance = 0 (izquierda=1, derecha=1). Está balanceado.

Insertamos otro niño:
Niño: ID = 10, Nombre: Carlos, Edad: 6.
10 < 50, va a la izquierda (donde está Luis).
10 < 25, va a la izquierda de Luis.
Luis: Factor de balance = 1. Ana: Factor de balance = 2. ¡DESBALANCEADO!

Como el factor de balance de Ana es 2 (mayor que 1), se requiere una rotación.
El desbalance está en la izquierda del hijo izquierdo (caso LL).
Se realiza una ROTACIÓN SIMPLE DERECHA en Ana:

Antes de la rotación:
            [50 - Ana]
           /          \
    [25 - Luis]    [75 - María]
      /
[10 - Carlos]

Después de la rotación derecha:
         [25 - Luis]
        /           \
 [10 - Carlos]   [50 - Ana]
                    \
                  [75 - María]

Ahora todos los nodos están balanceados. Luis es la nueva raíz.

Insertamos otro niño:
Niño: ID = 30, Nombre: Elena, Edad: 9.
30 > 25, va a la derecha de Luis.
30 < 50, va a la izquierda de Ana.
Todos los nodos siguen balanceados.

Árbol resultante:
         [25 - Luis]
        /           \
 [10 - Carlos]   [50 - Ana]
                /         \
          [30 - Elena]  [75 - María]

Insertamos otro niño:
Niño: ID = 60, Nombre: Pedro, Edad: 11.
60 > 25, va a la derecha.
60 > 50, va a la derecha de Ana.
60 < 75, va a la izquierda de María.
Ana: Factor de balance = -2. ¡DESBALANCEADO!

El desbalance está en la izquierda del hijo derecho (caso RL).
Se requiere una ROTACIÓN DOBLE:
1. Rotación derecha en María (hijo derecho de Ana).
2. Rotación izquierda en Ana.

Después de las rotaciones:
         [25 - Luis]
        /           \
 [10 - Carlos]   [60 - Pedro]
                /           \
          [50 - Ana]    [75 - María]
             \
        [30 - Elena]

VENTAJAS DEL ÁRBOL AVL

Rendimiento garantizado: todas las operaciones (búsqueda, inserción, eliminación) tienen complejidad O(log n) en el peor caso, a diferencia de un ABB normal que puede degradarse a O(n).

Ideal para búsquedas frecuentes: si tu aplicación realiza muchas búsquedas y pocas inserciones, el AVL es perfecto.

Auto-balanceo: no necesitas preocuparte por el balance del árbol, se mantiene automáticamente.

Altura controlada: la altura del árbol siempre es logarítmica respecto al número de nodos.

DESVENTAJAS

Más complejo: la implementación es más compleja que un ABB simple debido a las rotaciones.

Overhead en inserción: cada inserción puede requerir rotaciones, lo que añade un pequeño costo.

Más lento que ABB en inserciones: si los datos se insertan de forma aleatoria, un ABB simple puede ser más rápido.

COMPARACIÓN: ABB vs AVL

ABB (Árbol Binario de Búsqueda):
- Búsqueda promedio: O(log n)
- Búsqueda peor caso: O(n) (árbol degenerado)
- No garantiza balance
- Más simple de implementar

AVL (Árbol Auto-balanceado):
- Búsqueda siempre: O(log n) ✓
- Inserción siempre: O(log n) ✓
- Garantiza balance
- Más complejo (rotaciones)

CUÁNDO USAR AVL

Usa AVL cuando:
✓ Necesitas garantía de rendimiento O(log n)
✓ Realizas muchas búsquedas frecuentes
✓ Los datos pueden insertarse en orden (ascendente o descendente)
✓ No puedes permitir que el árbol se degenere a O(n)
✓ La consistencia de rendimiento es crítica

Usa ABB simple cuando:
✓ Los datos se insertan de forma aleatoria
✓ Pocas operaciones de búsqueda
✓ La simplicidad es más importante que el rendimiento garantizado

CASO DE ID REPETIDO

Al igual que en un ABB, si intentamos agregar un niño con el mismo ID que otro, por ejemplo:
Niño: ID = 50, Nombre: Andrés, Edad: 9.
El árbol no permitirá la inserción porque ya existe un nodo con el ID 50 (el de Ana).
En un Árbol AVL cada ID debe ser único, ya que es el valor que determina la posición y las comparaciones de los nodos.

RESUMEN DE ROTACIONES

1. Rotación Simple Derecha (LL):
   Desbalance en izquierda-izquierda
   
2. Rotación Simple Izquierda (RR):
   Desbalance en derecha-derecha
   
3. Rotación Doble LR (Izquierda-Derecha):
   Primero rotación izquierda en hijo izquierdo
   Luego rotación derecha en el nodo
   
4. Rotación Doble RL (Derecha-Izquierda):
   Primero rotación derecha en hijo derecho
   Luego rotación izquierda en el nodo

El árbol AVL es una de las estructuras de datos más eficientes para mantener datos ordenados con acceso rápido garantizado. Es ampliamente usado en bases de datos, sistemas de archivos y aplicaciones que requieren búsquedas eficientes.

Referencias:
- Paper original: "An algorithm for the organization of information" (1962)
- Georgy Adelson-Velsky y Evgenii Landis
- Complejidad temporal garantizada: O(log n) para todas las operaciones
