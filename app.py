from flask import Flask, render_template, request, redirect
import requests as http
import os

app = Flask(__name__)

ML_CLIENT_ID     = os.environ.get("ML_CLIENT_ID", "1433797948764704")
ML_CLIENT_SECRET = os.environ.get("ML_CLIENT_SECRET", "dIFBHXHWumKTL2pjwMhdbH244uwn0tXu")
ML_API           = "https://api.mercadolibre.com"

PRODUCTS_CONFIG = [
    {"mla_id": "MLA1340233696", "category": "Celulares",     "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🔥 Más vendido"},
    {"mla_id": "MLA1389506995", "category": "Celulares",     "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "⚡ Oferta"},
    {"mla_id": "MLA1413645196", "category": "Televisores",   "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "💎 Premium"},
    {"mla_id": "MLA1350143419", "category": "Computadoras",  "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🍏 Apple"},
    {"mla_id": "MLA1362315957", "category": "Audio",         "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🎧 Top Audio"},
    {"mla_id": "MLA1365779959", "category": "Gaming",        "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🎮 Gaming"},
]

CATEGORIES = ["Todos", "Celulares", "Televisores", "Computadoras", "Audio", "Gaming"]
_cache = {}


def get_token():
    if "token" in _cache:
        return _cache["token"]
    try:
        resp = http.post(f"{ML_API}/oauth/token", data={
            "grant_type": "client_credentials",
            "client_id": ML_CLIENT_ID,
            "client_secret": ML_CLIENT_SECRET,
        }, timeout=5)
        if resp.status_code == 200:
            _cache["token"] = resp.json().get("access_token")
            return _cache["token"]
    except Exception:
        pass
    return None


def fetch_product(config):
    mla_id = config["mla_id"]
    if mla_id in _cache:
        p = _cache[mla_id].copy()
        p.update({"affiliate_url": config["affiliate_url"], "badge": config["badge"], "category": config["category"]})
        return p
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        r = http.get(f"{ML_API}/items/{mla_id}", headers=headers, timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()
        rev = http.get(f"{ML_API}/reviews/item/{mla_id}", headers=headers, timeout=5)
        rating, n_reviews = 0.0, 0
        if rev.status_code == 200:
            rd = rev.json()
            rating = round(rd.get("rating_average", 0.0), 1)
            n_reviews = rd.get("paging", {}).get("total", 0)
        price = data.get("price", 0)
        old_price = data.get("original_price") or round(price * 1.15)
        discount = round((1 - price / old_price) * 100) if old_price else 0
        image = (data.get("thumbnail") or "").replace("http://", "https://").replace("-I.jpg", "-O.jpg")
        product = {"id": mla_id, "name": data.get("title", "Producto"), "price": price,
                   "old_price": old_price, "discount": discount, "image": image,
                   "stars": rating, "reviews": n_reviews}
        _cache[mla_id] = product
    except Exception:
        return None
    p = product.copy()
    p.update({"affiliate_url": config["affiliate_url"], "badge": config["badge"], "category": config["category"]})
    return p

FALLBACK_PRODUCTS = [
    {"id": "F1", "name": "Samsung Galaxy S25 Ultra 512GB", "category": "Celulares",
     "price": 1_450_000, "old_price": 1_699_000, "discount": 15,
     "image": "https://http2.mlstatic.com/D_NQ_NP_904598-MLA71782869418_092023-O.webp",
     "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🔥 Más vendido", "stars": 4.8, "reviews": 2341},
    {"id": "F2", "name": "MacBook Air M2 256GB", "category": "Computadoras",
     "price": 2_100_000, "old_price": 2_450_000, "discount": 14,
     "image": "https://http2.mlstatic.com/D_NQ_NP_715089-MLA51374425807_082022-O.webp",
     "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🍏 Apple", "stars": 4.9, "reviews": 3201},
    {"id": "F3", "name": "PlayStation 5 Slim", "category": "Gaming",
     "price": 980_000, "old_price": 1_150_000, "discount": 15,
     "image": "https://http2.mlstatic.com/D_NQ_NP_939868-MLA71455484636_082023-O.webp",
     "affiliate_url": "https://www.mercadolibre.com.ar/", "badge": "🎮 Gaming", "stars": 4.9, "reviews": 5870},
]

def get_all_products():
    products = [p for p in (fetch_product(c) for c in PRODUCTS_CONFIG) if p]
    return products if products else FALLBACK_PRODUCTS


@app.route("/")
def index():
    category = request.args.get("cat", "Todos")
    all_products = get_all_products()
    products = all_products if category == "Todos" else [p for p in all_products if p["category"] == category]
    return render_template("index.html", products=products, categories=CATEGORIES, active_cat=category)


@app.route("/go/<path:product_id>")
def go(product_id):
    config = next((c for c in PRODUCTS_CONFIG if c["mla_id"] == product_id), None)
    return redirect(config["affiliate_url"] if config else "/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
