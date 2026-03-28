from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# ─────────────────────────────────────────────
#  PRODUCTOS — Reemplazá los links con tus URLs
#  de afiliado de Mercado Libre
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "id": 1,
        "name": "iPhone 15 128GB",
        "category": "Celulares",
        "price": 1_450_000,
        "old_price": 1_699_000,
        "discount": 15,
        "image": "https://http2.mlstatic.com/D_NQ_NP_904598-MLA71782869418_092023-O.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/",  # ← Tu link de afiliado
        "badge": "🔥 Más vendido",
        "stars": 4.8,
        "reviews": 2341,
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S26 Ultra, 512 gb, 12 gb, cámara cuádruple violeta",
        "category": "Celulares",
        "price": 1_290_000,
        "old_price": 1_550_000,
        "discount": 17,
        "image": "https://http2.mlstatic.com/D_NQ_NP_2X_763049-MLA107401577298_032026-F.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/samsung-galaxy-s26-ultra-512-gb-12-gb-camara-cuadruple-violeta/p/MLA65503965?pdp_filters=item_id%3AMLA3050589592&matt_tool=89488245#origin=share&sid=share&wid=MLA3050589592&action=copy",
        "badge": "🔥 Más vendido",
        "stars": 4.7,
        "reviews": 1870,
    },
    {
        "id": 3,
        "name": 'Smart TV 55" 4K QLED',
        "category": "Televisores",
        "price": 780_000,
        "old_price": 990_000,
        "discount": 21,
        "image": "https://http2.mlstatic.com/D_NQ_NP_769397-MLA51568073726_092022-O.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/",
        "badge": "💎 Premium",
        "stars": 4.6,
        "reviews": 987,
    },
    {
        "id": 4,
        "name": "MacBook Air M2 256GB",
        "category": "Computadoras",
        "price": 2_100_000,
        "old_price": 2_450_000,
        "discount": 14,
        "image": "https://http2.mlstatic.com/D_NQ_NP_715089-MLA51374425807_082022-O.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/",
        "badge": "🍏 Apple",
        "stars": 4.9,
        "reviews": 3201,
    },
    {
        "id": 5,
        "name": "AirPods Pro 2da Gen",
        "category": "Audio",
        "price": 320_000,
        "old_price": 399_000,
        "discount": 20,
        "image": "https://http2.mlstatic.com/D_NQ_NP_617038-MLA51635183745_092022-O.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/",
        "badge": "🎧 Top Audio",
        "stars": 4.8,
        "reviews": 4521,
    },
    {
        "id": 6,
        "name": "PlayStation 5 Slim",
        "category": "Gaming",
        "price": 980_000,
        "old_price": 1_150_000,
        "discount": 15,
        "image": "https://http2.mlstatic.com/D_NQ_NP_939868-MLA71455484636_082023-O.webp",
        "affiliate_url": "https://www.mercadolibre.com.ar/",
        "badge": "🎮 Gaming",
        "stars": 4.9,
        "reviews": 5870,
    },
]

CATEGORIES = ["Todos", "Celulares", "Televisores", "Computadoras", "Audio", "Gaming"]


@app.route("/")
def index():
    category = request.args.get("cat", "Todos")
    if category == "Todos":
        products = PRODUCTS
    else:
        products = [p for p in PRODUCTS if p["category"] == category]
    return render_template(
        "index.html",
        products=products,
        categories=CATEGORIES,
        active_cat=category,
    )


@app.route("/go/<int:product_id>")
def go(product_id):
    """Redirige al link de afiliado — acá podés trackear clics si querés."""
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        return redirect(product["affiliate_url"])
    return redirect("/")


import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
