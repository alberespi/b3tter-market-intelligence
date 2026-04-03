"""
scraper_yotpo.py
----------------
Scraper de reviews de B3tter Foods via Yotpo widget API (batch endpoint).
No requiere Playwright — usa requests + BeautifulSoup.

Uso:
    python scraper_yotpo.py

Output:
    data/raw/yotpo_b3tter_reviews.csv
"""

import requests
import time
import random
import json
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime

# ── Configuración ────────────────────────────────────────────────────────────

APP_KEY = "rCyIpqRQah7Nzs5sSzQPIyzn170Ekp8uLXK7eqSu"
ENDPOINT = "https://staticw2.yotpo.com/batch"

# Productos de B3tter y sus product IDs (pid)
# El pid es el domain_key que aparece en la URL del widget de cada producto
# Formato: "nombre_legible": "pid"
PRODUCTS = {
    "granola_cacao":      "8731411054925",
    "granola_original":   "7569853317319",
    "cacao_bar":          "6573573341383",
    "cacahuete_bar":      "6571405934791",
    "coco_bar":           "10105300582733",
    "arandano_bar":       "6573534412999",
    "crema_cacao":        "6879615942855",
    "starter_pack":       "8773316575565",
    "original_pack":      "577297289415",
    "choco_lovers_pack":  "7579368947911",
    # Añade aquí el resto de productos cuando tengas sus pids
    # Para obtener el pid de cada producto:
    #   1. Abre la página del producto en b3tterfoods.com
    #   2. DevTools → Network → filtra por "yotpo" → click en "main_widget"
    #   3. Pestaña Payload → el campo "pid" es el que necesitas
}

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "yotpo_b3tter_reviews.csv")
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/133.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://b3tterfoods.com",
    "Referer": "https://b3tterfoods.com/",
}
 
# ── Funciones ────────────────────────────────────────────────────────────────
 
def build_payload(pid: str, page: int = 1) -> dict:
    """Construye el payload del POST request para un producto y página."""
    methods = json.dumps([{
        "method": "main_widget",
        "params": {
            "pid": pid,
            "order_metadata_fields": {},
            "widget_product_id": pid,
            "page": page,
            "per_page": 150,  # máximo por request
        }
    }])
    return {
        "methods": methods,
        "app_key": APP_KEY,
        "is_mobile": "false",
        "widget_version": "2026-03-24_08-38-12",
        "lang": "es",
    }
 
 
def parse_reviews(html: str, product_name: str) -> list[dict]:
    """Parsea el HTML del widget y extrae las reviews estructuradas."""
    soup = BeautifulSoup(html, "html.parser")
    reviews = []
 
    # Yotpo B3tter usa yotpo-review yotpo-regular-box como contenedor de cada review
    review_boxes = soup.find_all("div", class_="yotpo-review")
 
    for box in review_boxes:
        review = {
            "product_name": product_name,
            "brand": "B3tter",
            "source": "b3tterfoods.com",
            "scraped_at": datetime.now().strftime("%Y-%m-%d"),
        }
 
        # Rating — span.sr-only contiene texto tipo "4.9 star rating"
        sr_only = box.find("span", class_="sr-only")
        if sr_only:
            text = sr_only.get_text(strip=True)
            try:
                review["rating"] = float(text.split()[0].replace(",", "."))
            except (ValueError, IndexError):
                review["rating"] = None
        else:
            # Fallback: contar estrellas llenas
            filled = box.find_all(
                "span",
                class_=lambda c: c and "yotpo-icon-star" in c and "empty" not in c
            )
            review["rating"] = len(filled) if filled else None
 
        # Título — yotpo-review-wrapper > content-title
        title_tag = box.find(class_="content-title")
        review["title"] = title_tag.get_text(strip=True) if title_tag else ""
 
        # Cuerpo — yotpo-review-wrapper > content-review
        body_tag = box.find(class_="content-review")
        if not body_tag:
            body_tag = box.find(class_="yotpo-main")
        review["body"] = body_tag.get_text(separator=" ", strip=True) if body_tag else ""
 
        # Fecha — span.y-label.yotpo-review-date
        date_tag = box.find("span", class_="yotpo-review-date")
        review["date"] = date_tag.get_text(strip=True) if date_tag else ""
 
        # Reviewer — span.y-label.yotpo-user-name
        reviewer_tag = box.find("span", class_="yotpo-user-name")
        review["reviewer"] = reviewer_tag.get_text(strip=True) if reviewer_tag else ""
 
        # Compra verificada — div.yotpo-header-element con clase verified-buyer
        verified = box.find(class_="verified-buyer")
        review["verified_purchase"] = bool(verified)
 
        # Solo guardamos si tiene al menos cuerpo o título
        if review["title"] or review["body"]:
            reviews.append(review)
 
    return reviews
 
 
def scrape_product(product_name: str, pid: str) -> list[dict]:
    """Scrape todas las páginas de reviews de un producto."""
    all_reviews = []
    page = 1
 
    print(f"\n{'─'*50}")
    print(f"Scraping: {product_name} (pid={pid})")
 
    while True:
        payload = build_payload(pid, page)
 
        try:
            response = requests.post(
                ENDPOINT,
                data=payload,
                headers=HEADERS,
                timeout=15,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  ✗ Error en página {page}: {e}")
            break
 
        try:
            data = response.json()
            # El HTML de las reviews está en la clave "result", no "widget"
            widget_html = data[0].get("result", "")
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"  ✗ Error parseando JSON en página {page}: {e}")
            break
 
        reviews = parse_reviews(widget_html, product_name)
 
        if not reviews:
            print(f"  ✓ Sin más reviews en página {page}. Total: {len(all_reviews)}")
            break
 
        all_reviews.extend(reviews)
        print(f"  → Página {page}: {len(reviews)} reviews encontradas")
 
        # Delay aleatorio para no saturar el servidor
        time.sleep(random.uniform(1.5, 3.0))
        page += 1
 
    return all_reviews
 
 
def save_to_csv(reviews: list[dict], filepath: str):
    """Guarda las reviews en un CSV estructurado."""
    if not reviews:
        print("\n⚠ No hay reviews para guardar.")
        return
 
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
 
    fieldnames = [
        "product_name", "brand", "source", "rating",
        "title", "body", "date", "reviewer",
        "verified_purchase", "scraped_at",
    ]
 
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)
 
    print(f"\n✓ Dataset guardado en: {filepath}")
    print(f"  Total reviews: {len(reviews)}")
 
 
# ── Main ─────────────────────────────────────────────────────────────────────
 
def main():
    print("=" * 50)
    print("B3tter Market Intelligence — Yotpo Scraper")
    print("=" * 50)
 
    all_reviews = []
 
    for product_name, pid in PRODUCTS.items():
        reviews = scrape_product(product_name, pid)
        all_reviews.extend(reviews)
        # Delay entre productos
        time.sleep(random.uniform(2.0, 4.0))
 
    save_to_csv(all_reviews, OUTPUT_FILE)
 
 
if __name__ == "__main__":
    main()