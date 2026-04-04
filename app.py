from flask import Flask, render_template, request, redirect
import requests as http
import os

app = Flask(__name__)

# Credenciales (Asegúrate de que tu App en MeLi tenga permisos de Afiliado)
ML_CLIENT_ID = os.environ.get("ML_CLIENT_ID")
ML_CLIENT_SECRET = os.environ.get("ML_CLIENT_SECRET")
ML_API = "https://api.mercadolibre.com"

# Búsquedas automáticas
SEARCH_CONFIG = [
    {"query": "iphone 15 pro", "category": "Celulares", "badge": "🔥 Tendencia"},
    {"query": "samsung galaxy s24", "category": "Celulares", "badge": "✨ Nuevo"},
    {"query": "smart tv 50 pulgadas 4k", "category": "Televisores", "badge": "📺 Cine"},
    {"query": "notebook gamer rtx", "category": "Computadoras", "badge": "🚀 Gaming"},
    {"query": "macbook air m2", "category": "Computadoras", "badge": "🍏 Apple"},
    {"query": "auriculares sony wh1000xm5", "category": "Audio", "badge": "🎧 Top"}
]

CATEGORIES = ["Todos", "Celulares", "Televisores", "Computadoras", "Audio"]

def get_token():
    try:
        r = http.post(f"{ML_API}/oauth/token", data={
            "grant_type": "client_credentials",
            "client_id": ML_CLIENT_ID,
            "client_secret": ML_CLIENT_SECRET
        }, timeout=5)
        return r.json().get("access_token")
    except:
        return None

def generate_affiliate_link(original_url, token):
    """
    Convierte un link normal en un link de afiliado usando la API.
    Nota: Tu aplicación de MeLi debe estar vinculada a tu cuenta de afiliado.
    """
    if not token: return original_url
    
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        # Endpoint oficial para generar links de afiliados
        payload = {"url": original_url}
        r = http.post(f"{ML_API}/affiliates/links", headers=headers, json=payload, timeout=5)
        
        if r.status_code == 201:
            return r.json().get("short_link", original_url)
    except:
        pass
    return original_url

def get_automated_products():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    products = []

    for config in SEARCH_CONFIG:
        try:
            search_url = f"{ML_API}/sites/MLA/search?q={config['query']}&limit=1&sort=relevance"
            r = http.get(search_url, headers=headers, timeout=5)
            
            if r.status_code == 200:
                data = r.json().get("results", [])[0]
                if not data:
                    continue
                
                # OBTENEMOS EL LINK DE COMISIÓN AQUÍ
                raw_link = data.get("permalink")
                affiliate_link = generate_affiliate_link(raw_link, token)
                
                price = data.get("price", 0)
                old_price = data.get("original_price") or round(price / 0.85)
                
                products.append({
                    "id": data.get("id"),
                    "name": data.get("title"),
                    "price": price,
                    "old_price": old_price,
                    "discount": round((1 - price / old_price) * 100) if old_price else 0,
                    "image": data.get("thumbnail", "").replace("-I.jpg", "-O.jpg"),
                    "installments": data.get("installments"),
                    "stars": 4.8,
                    "reviews": 120,
                    "category": config["category"],
                    "badge": config["badge"],
                    "affiliate_url": affiliate_link # <--- LINK CON COMISIÓN
                })
        except:
            continue
    return products

@app.route("/")
def index():
    cat = request.args.get("cat", "Todos")
    all_p = get_automated_products()
    products = all_p if cat == "Todos" else [p for p in all_p if p["category"] == cat]
    return render_template("index.html", products=products, categories=CATEGORIES, active_cat=cat)

@app.route("/go/<path:product_id>")
def go(product_id):
    # Buscamos el link de afiliado generado en el proceso anterior
    # Para simplificar, en esta versión redirigimos al link de la API
    # En un entorno real, podrías guardar esto en una base de datos temporal
    all_p = get_automated_products()
    product = next((p for p in all_p if p["id"] == product_id), None)
    
    if product:
        return redirect(product["affiliate_url"])
    return redirect(f"https://articulo.mercadolibre.com.ar/{product_id}")

@app.route("/health")
def health():
    return "OK", 200 #texto

if __name__ == "__main__":
    app.run(debug=True)
