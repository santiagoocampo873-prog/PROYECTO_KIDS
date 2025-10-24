# 📚 Documentación y Colecciones

Esta carpeta contiene la documentación y colecciones para importar en herramientas de testing de APIs.

## 📦 Archivo Incluido

### `API_ABB_AVL_Postman_Collection.json`

Colección completa de Postman con todos los endpoints de las APIs ABB y AVL.

**Contenido:**
- ✅ 2 endpoints generales (Inicio, Health Check)
- ✅ 11 endpoints de la API ABB
- ✅ 12 endpoints de la API AVL
- ✅ 5 ejemplos paso a paso del ABB (del documento ABB.md)
- ✅ 7 ejemplos paso a paso del AVL (del documento AVL.md)

**Total: 37 peticiones organizadas en carpetas**

---

## 🚀 Cómo Importar en Postman

### Método 1: Importar desde archivo

1. **Abre Postman**
2. Haz clic en **"Import"** (esquina superior izquierda)
3. Selecciona **"Choose Files"**
4. Navega a: `api_abb/docs/API_ABB_AVL_Postman_Collection.json`
5. Haz clic en **"Import"**

### Método 2: Arrastrar y soltar

1. **Abre Postman**
2. Arrastra el archivo `API_ABB_AVL_Postman_Collection.json` directamente a la ventana de Postman
3. La colección se importará automáticamente

---

## 📂 Estructura de la Colección

```
API ABB y AVL - Árboles Binarios
├── General
│   ├── Inicio - Información General
│   └── Health Check
│
├── ABB - Árbol Binario de Búsqueda
│   ├── Información ABB
│   ├── Agregar Niño
│   ├── Buscar Niño por ID
│   ├── Obtener Todos los Niños
│   ├── Ver Estructura del Árbol
│   ├── Recorrido Inorden
│   ├── Recorrido Preorden
│   ├── Recorrido Postorden
│   ├── Estadísticas del Árbol
│   ├── Contar Niños
│   └── Limpiar Árbol
│
├── AVL - Árbol Auto-balanceado
│   ├── Información AVL
│   ├── Agregar Niño (con auto-balanceo)
│   ├── Buscar Niño por ID
│   ├── Obtener Todos los Niños
│   ├── Ver Estructura del Árbol
│   ├── Recorrido Inorden
│   ├── Recorrido Preorden
│   ├── Recorrido Postorden
│   ├── Estadísticas del Árbol
│   ├── Verificar Balance ⭐
│   ├── Contar Niños
│   └── Limpiar Árbol
│
├── Ejemplos - ABB
│   ├── 1. Agregar Lucas (Raíz)
│   ├── 2. Agregar Sofía (Izquierda)
│   ├── 3. Agregar Mateo (Derecha)
│   ├── 4. Agregar Valentina
│   └── 5. Intentar ID Duplicado (Error)
│
└── Ejemplos - AVL
    ├── 1. Agregar Ana (Raíz)
    ├── 2. Agregar Luis
    ├── 3. Agregar María
    ├── 4. Agregar Carlos (Causa Rotación)
    ├── 5. Agregar Elena
    ├── 6. Agregar Pedro
    └── 7. Verificar Balance
```

---

## 🎯 Cómo Usar la Colección

### 1. Asegúrate de que el servidor esté corriendo

```bash
cd api_abb
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Base URL

La colección está configurada con una variable de entorno:
- **Variable:** `base_url`
- **Valor por defecto:** `http://localhost:8000`

Si tu servidor corre en otro puerto, puedes modificar esta variable en:
- Postman → Colección → Variables → Editar `base_url`

### 3. Probar los Ejemplos

#### Ejemplo ABB (Secuencia del documento):
1. Ve a **"Ejemplos - ABB"**
2. Ejecuta las peticiones en orden:
   - 1. Agregar Lucas (Raíz)
   - 2. Agregar Sofía (Izquierda)
   - 3. Agregar Mateo (Derecha)
   - 4. Agregar Valentina
3. Ahora ve a **"ABB - Árbol Binario de Búsqueda"**
4. Ejecuta **"Ver Estructura del Árbol"** para visualizar el ABB
5. Prueba **"Recorrido Inorden"** para ver los niños ordenados

#### Ejemplo AVL (Secuencia con rotaciones):
1. Ve a **"Ejemplos - AVL"**
2. Ejecuta las peticiones en orden:
   - 1. Agregar Ana (Raíz)
   - 2. Agregar Luis
   - 3. Agregar María
   - 4. Agregar Carlos (observa cómo se balancea automáticamente)
   - 5. Agregar Elena
   - 6. Agregar Pedro
   - 7. Verificar Balance (verás que está balanceado)
3. Ahora ve a **"AVL - Árbol Auto-balanceado"**
4. Ejecuta **"Ver Estructura del Árbol"** para ver el AVL balanceado
5. Ejecuta **"Estadísticas del Árbol"** para ver la altura

---

## 📝 Notas Importantes

### IDs Únicos
- ❌ No puedes agregar dos niños con el mismo ID
- ✅ Si lo intentas, recibirás un error 409 (Conflict)

### Árboles Independientes
- El árbol ABB y el árbol AVL son **independientes**
- Puedes tener diferentes niños en cada árbol
- Los datos no se comparten entre árboles

### Datos en Memoria
- ⚠️ Los datos se almacenan en **memoria RAM**
- Si reinicias el servidor, los árboles se vacían
- Usa **"Limpiar Árbol"** para vaciar manualmente

---

## 🔄 Flujo de Trabajo Recomendado

### Para ABB:
1. **Limpiar Árbol** (si tiene datos previos)
2. **Agregar varios niños** con diferentes IDs
3. **Ver Estructura del Árbol** para visualizar
4. **Recorrido Inorden** para ver ordenados
5. **Estadísticas** para ver información general

### Para AVL:
1. **Limpiar Árbol** (si tiene datos previos)
2. **Agregar niños en secuencia** (observa el auto-balanceo en las respuestas)
3. **Verificar Balance** (debe ser `true`)
4. **Ver Estructura del Árbol** para visualizar el balance
5. **Estadísticas** para ver altura y balance

---

## 📊 Respuestas Esperadas

### POST Exitoso (ABB):
```json
{
  "success": true,
  "message": "Niño 'Lucas' con ID 10 agregado exitosamente al árbol",
  "child": {
    "id": 10,
    "name": "Lucas",
    "age": 7
  }
}
```

### POST Exitoso (AVL con info de balance):
```json
{
  "success": true,
  "message": "Niño 'Ana' con ID 50 agregado exitosamente al árbol AVL",
  "child": {
    "id": 50,
    "name": "Ana",
    "age": 10
  },
  "balanced": true,
  "tree_height": 3
}
```

### Error ID Duplicado (409):
```json
{
  "detail": "No se puede agregar el niño. El ID 10 ya existe en el árbol"
}
```

### Error Niño No Encontrado (404):
```json
{
  "detail": "Niño con ID 99 no encontrado en el árbol"
}
```

---

## 🎨 Personalizar las Peticiones

Todas las peticiones pueden ser modificadas en Postman:

1. **Cambiar datos del niño:**
   - Haz clic en la petición
   - Ve a **"Body"**
   - Modifica el JSON (id, name, age)

2. **Cambiar ID de búsqueda:**
   - Haz clic en la petición
   - Modifica el número en la URL
   - Ejemplo: `.../children/10` → `.../children/25`

3. **Agregar headers adicionales:**
   - Ve a la pestaña **"Headers"**
   - Agrega los headers que necesites

---

## 🌐 Exportar Respuestas

Postman te permite guardar las respuestas:

1. Ejecuta una petición
2. Haz clic en **"Save Response"**
3. Guarda como ejemplo en la colección
4. Útil para documentar comportamientos

---

## 🔧 Troubleshooting

### "Could not get any response"
- ✅ Verifica que el servidor esté corriendo
- ✅ Confirma que esté en `http://localhost:8000`
- ✅ Revisa que no haya firewall bloqueando

### Error 404 en todas las peticiones
- ✅ Verifica la base URL en las variables
- ✅ Asegúrate de que el servidor está en el puerto 8000

### Error 422 (Validation Error)
- ✅ Verifica el formato del JSON en el body
- ✅ Asegúrate de que los campos tengan los tipos correctos
- ✅ ID debe ser un número entero positivo
- ✅ Age debe estar entre 0 y 150

---

## 📖 Documentación Adicional

- **README_ABB.md** - Documentación completa de la API ABB
- **README_AVL.md** - Documentación completa de la API AVL
- **INSTRUCCIONES_COMPLETAS.md** - Guía general de ambas APIs
- **Swagger UI:** http://localhost:8000/docs

---

## ✨ Características de la Colección

- ✅ **Organizada por carpetas** temáticas
- ✅ **Descripciones detalladas** en cada petición
- ✅ **Ejemplos pre-configurados** con datos de los documentos
- ✅ **Variables de entorno** para fácil configuración
- ✅ **Headers configurados** automáticamente
- ✅ **Bodies pre-llenados** con datos de ejemplo
- ✅ **Lista para usar** sin configuración adicional

---

**¡Disfruta probando las APIs de ABB y AVL! 🚀**
