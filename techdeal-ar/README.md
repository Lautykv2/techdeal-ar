# ⚡ TechDeal AR — Sitio de Afiliados Mercado Libre

Página web para el sistema de afiliados de Mercado Libre, especializada en tecnología y electrónica.

---

## 🚀 Instalación y uso

### 1. Abrir el proyecto en VS Code
Abrí la carpeta `techdeal-ar` en Visual Studio Code.

### 2. Crear un entorno virtual (recomendado)
En la terminal integrada de VS Code (`Ctrl+Ñ`):

```bash
python -m venv venv
```

Activarlo:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Correr la app
```bash
python app.py
```

### 5. Abrir en el navegador
Visitá: **http://127.0.0.1:5000**

---

## 🔗 Cómo agregar tus links de afiliado

Abrí `app.py` y en la lista `PRODUCTS`, reemplazá el valor de `"affiliate_url"` de cada producto con tu link de afiliado de Mercado Libre.

```python
{
    "name": "iPhone 15 128GB",
    "affiliate_url": "https://click.mlafiliados.com/...",  # ← TU LINK AQUÍ
    ...
}
```

## ➕ Cómo agregar un producto nuevo

Copiá este bloque dentro de la lista `PRODUCTS` en `app.py`:

```python
{
    "id": 7,                        # ID único (correlativo)
    "name": "Nombre del producto",
    "category": "Celulares",        # Debe coincidir con una categoría de CATEGORIES
    "price": 500_000,               # Precio actual
    "old_price": 600_000,           # Precio anterior (tachado)
    "discount": 17,                 # % de descuento
    "image": "URL_DE_LA_IMAGEN",    # URL de la imagen del producto en MeLi
    "affiliate_url": "TU_LINK",     # Tu link de afiliado
    "badge": "🔥 Oferta",           # Etiqueta sobre la imagen
    "stars": 4.5,                   # Calificación (0-5)
    "reviews": 1234,                # Número de reviews
},
```

## 📁 Estructura del proyecto

```
techdeal-ar/
├── app.py               # Servidor Flask (productos y rutas)
├── requirements.txt     # Dependencias Python
├── templates/
│   └── index.html       # Plantilla HTML principal
└── static/
    ├── css/
    │   └── style.css    # Estilos de la página
    └── js/
        └── main.js      # Animaciones e interacciones
```
