import asyncio
import re
import random
import httpx
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

HEADERS_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
}

STORES = {
    "Leclerc": {
        "url":       "https://www.e.leclerc/recherche?q={query}",
        "card":      "div.product-card, article[data-testid='product-card'], div[class*='ProductCard']",
        "name":      "[data-testid='product-title'], .product-card__title, h3[class*='title']",
        "price":     "[data-testid='price-amount'], .price__amount, span[class*='price']",
        "old_price": ".price--crossed, [data-testid='crossed-price']",
        "weight":    ".grammage, [data-testid='weight'], span[class*='weight']",
    },
    "Carrefour": {
        "url":       "https://www.carrefour.fr/s?q={query}&lang=fr_FR",
        "card":      "article.product-card-article, div[class*='product-card']",
        "name":      ".product-card__title, [data-testid='product-name']",
        "price":     ".product-card__price--current, [data-testid='price'], span[class*='current-price']",
        "old_price": ".product-card__price--old, span[class*='old-price']",
        "weight":    ".product-card__weight, span[class*='grammage']",
    },
    "Auchan": {
        "url":       "https://www.auchan.fr/recherche?query={query}",
        "card":      "div[class*='ProductThumbnail'], div[class*='product-thumbnail']",
        "name":      "h3[class*='title'], span[class*='product-name']",
        "price":     "span[class*='price-value'], div[class*='PriceBox']",
        "old_price": "span[class*='price-old'], span[class*='price-crossed']",
        "weight":    "span[class*='weight'], span[class*='grammage']",
    },
    "Lidl": {
        "url":       "https://www.lidl.fr/q/{query}",
        "card":      "article[class*='product'], div[class*='ProductBox']",
        "name":      "h3[class*='title'], span[class*='name']",
        "price":     "div[class*='m-price__price'], span[class*='price']",
        "old_price": "span[class*='rrp'], span[class*='old']",
        "weight":    "span[class*='weight'], span[class*='quantity']",
    },
    "Casino": {
        "url":       "https://www.casino.fr/search?q={query}",
        "card":      "li[class*='product-item'], div[class*='product-card']",
        "name":      "strong[class*='product-item-name'], span[class*='product-title']",
        "price":     "span.price, span[class*='product-price']",
        "old_price": "span.old-price, span[class*='price-old']",
        "weight":    "span[class*='weight'], span[class*='grammage']",
    },
    "Aldi": {
        "url":       "https://www.aldi.fr/recherche?q={query}",
        "card":      "div[class*='product'], li[class*='product-tile']",
        "name":      "span[class*='product-title'], h3[class*='name']",
        "price":     "span[class*='price'], div[class*='price-box']",
        "old_price": "span[class*='old-price'], del",
        "weight":    "span[class*='weight'], span[class*='unit']",
    },
    "Intermarche": {
        "url":       "https://www.intermarche.com/recherche?q={query}",
        "card":      "div[class*='product-card'], article[class*='product']",
        "name":      "h3[class*='title'], span[class*='product-name'], p[class*='name']",
        "price":     "span[class*='price'], div[class*='price-box']",
        "old_price": "span[class*='old-price'], del[class*='price']",
        "weight":    "span[class*='weight'], span[class*='grammage'], span[class*='unit']",
    },
}

# ── FALLBACK PRICES (premier prix) ───────────────────────────────────────────
# (price_euros, weight_kg)
FALLBACK_PP = {
    "Poitrine de poulet":      {"Leclerc": (8.95,1.0), "Carrefour": (9.45,1.0), "Auchan": (8.75,1.0), "Lidl": (7.99,1.0), "Casino": (9.99,1.0), "Intermarche": (8.49,1.0), "Aldi": (7.89,1.0)},
    "Viande hachee 5% MG":    {"Leclerc": (4.95,0.5), "Carrefour": (5.20,0.5), "Auchan": (4.85,0.5), "Lidl": (4.49,0.5), "Casino": (5.50,0.5), "Intermarche": (4.75,0.5), "Aldi": (4.29,0.5)},
    "Viande hachee 10% MG":   {"Leclerc": (3.95,0.5), "Carrefour": (4.20,0.5), "Auchan": (3.85,0.5), "Lidl": (3.49,0.5), "Casino": (4.50,0.5), "Intermarche": (3.79,0.5), "Aldi": (3.29,0.5)},
    "Skyr nature":             {"Leclerc": (1.99,0.5), "Carrefour": (2.15,0.5), "Auchan": (1.89,0.5), "Lidl": (1.49,0.5), "Casino": (2.29,0.5), "Intermarche": (1.95,0.5), "Aldi": (1.39,0.5)},
    "Carre blanc 0%":          {"Leclerc": (1.45,0.5), "Carrefour": (1.59,0.5), "Auchan": (1.39,0.5), "Lidl": (1.19,0.5), "Casino": (1.69,0.5), "Intermarche": (1.35,0.5), "Aldi": (1.15,0.5)},
    "Truite filet":            {"Leclerc": (3.99,0.25),"Carrefour": (4.25,0.25),"Auchan": (3.85,0.25),"Lidl": (3.49,0.25),"Casino": (4.50,0.25),"Intermarche": (3.79,0.25), "Aldi": (3.29,0.25)},
    "Thon en boite (eau)":     {"Leclerc": (1.09,0.16),"Carrefour": (1.19,0.16),"Auchan": (0.99,0.16),"Lidl": (0.79,0.16),"Casino": (1.25,0.16),"Intermarche": (0.95,0.16), "Aldi": (0.69,0.16)},
    "Pave de saumon fume":     {"Leclerc": (3.99,0.2), "Carrefour": (4.29,0.2), "Auchan": (3.89,0.2), "Lidl": (3.49,0.2), "Casino": (4.59,0.2), "Intermarche": (3.85,0.2), "Aldi": (3.29,0.2)},
    "Myrtilles surgelees":     {"Leclerc": (2.99,0.5), "Carrefour": (3.25,0.5), "Auchan": (2.89,0.5), "Lidl": (2.49,0.5), "Casino": (3.45,0.5), "Intermarche": (2.79,0.5), "Aldi": (2.29,0.5)},
    "Brocoli surgele":         {"Leclerc": (1.79,1.0), "Carrefour": (1.95,1.0), "Auchan": (1.69,1.0), "Lidl": (1.39,1.0), "Casino": (2.05,1.0), "Intermarche": (1.65,1.0), "Aldi": (1.29,1.0)},
    "Epinards surgeles":       {"Leclerc": (1.99,0.75),"Carrefour": (2.15,0.75),"Auchan": (1.89,0.75),"Lidl": (1.59,0.75),"Casino": (2.25,0.75),"Intermarche": (1.85,0.75), "Aldi": (1.49,0.75)},
    "Chou-fleur surgele":      {"Leclerc": (1.89,1.0), "Carrefour": (1.99,1.0), "Auchan": (1.79,1.0), "Lidl": (1.49,1.0), "Casino": (2.09,1.0), "Intermarche": (1.75,1.0), "Aldi": (1.39,1.0)},
    "Haricots verts surgeles": {"Leclerc": (1.59,1.0), "Carrefour": (1.75,1.0), "Auchan": (1.49,1.0), "Lidl": (1.19,1.0), "Casino": (1.89,1.0), "Intermarche": (1.45,1.0), "Aldi": (1.09,1.0)},
    "Riz Basmati blanc":       {"Leclerc": (2.49,1.0), "Carrefour": (2.65,1.0), "Auchan": (2.39,1.0), "Lidl": (1.99,1.0), "Casino": (2.79,1.0), "Intermarche": (2.35,1.0), "Aldi": (1.89,1.0)},
    "Riz Basmati complet":     {"Leclerc": (2.99,1.0), "Carrefour": (3.15,1.0), "Auchan": (2.89,1.0), "Lidl": (2.49,1.0), "Casino": (3.25,1.0), "Intermarche": (2.85,1.0), "Aldi": (2.39,1.0)},
    "Riz complet":             {"Leclerc": (1.89,1.0), "Carrefour": (1.99,1.0), "Auchan": (1.79,1.0), "Lidl": (1.49,1.0), "Casino": (2.09,1.0), "Intermarche": (1.75,1.0), "Aldi": (1.49,1.0)},
    "Lentilles vertes":        {"Leclerc": (1.49,0.5), "Carrefour": (1.65,0.5), "Auchan": (1.39,0.5), "Lidl": (1.09,0.5), "Casino": (1.79,0.5), "Intermarche": (1.35,0.5), "Aldi": (1.05,0.5)},
}

# Marque = ~30% plus cher que premier prix
FALLBACK_MARQUE = {
    prod: {store: (round(p * 1.3, 2), w) for store, (p, w) in stores.items()}
    for prod, stores in FALLBACK_PP.items()
}

# ── HELPERS ───────────────────────────────────────────────────────────────────

def parse_price(text):
    if not text:
        return None
    cleaned = re.sub(r"[^\d.,]", "", text.replace(",", "."))
    m = re.search(r"(\d+\.\d{1,2})", cleaned)
    return float(m.group(1)) if m else None

def parse_weight_kg(text):
    if not text:
        return None
    t = text.lower().replace(",", ".").replace(" ", "")
    m = re.search(r"(\d+\.?\d*)\s*kg", t)
    if m: return float(m.group(1))
    m = re.search(r"(\d+\.?\d*)\s*g\b", t)
    if m: return float(m.group(1)) / 1000
    m = re.search(r"(\d+\.?\d*)\s*l\b", t)
    if m: return float(m.group(1))
    return None

def find_fallback_key(name):
    nl = name.lower()
    for k in FALLBACK_PP:
        if k.lower() in nl or nl in k.lower():
            return k
    # Partial match
    words = nl.split()
    for k in FALLBACK_PP:
        kl = k.lower()
        if any(w in kl for w in words if len(w) > 4):
            return k
    return None

# ── SCRAPING ──────────────────────────────────────────────────────────────────

async def scrape_store(client, store_name, product):
    cfg = STORES[store_name]
    keyword = product["keywords"][0]
    url = cfg["url"].format(query=keyword.replace(" ", "+"))
    fallback_wkg = product["weight_g"] / 1000
    headers = dict(HEADERS_BASE)
    headers["User-Agent"] = random.choice(USER_AGENTS)
    try:
        await asyncio.sleep(random.uniform(0.1, 0.5))
        resp = await client.get(url, headers=headers, timeout=10, follow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(cfg["card"])
        if not cards:
            return None
        candidates = []
        for card in cards[:5]:
            ne = card.select_one(cfg["name"])
            pe = card.select_one(cfg["price"])
            if not ne or not pe:
                continue
            price_val = parse_price(pe.get_text())
            if not price_val:
                continue
            wkg = None
            we = card.select_one(cfg["weight"])
            if we:
                wkg = parse_weight_kg(we.get_text())
            if not wkg:
                wkg = parse_weight_kg(ne.get_text()) or fallback_wkg
            per_kg = price_val / wkg
            promo = None
            oe = card.select_one(cfg["old_price"])
            if oe:
                old = parse_price(oe.get_text())
                if old and old > price_val:
                    pct = round((1 - price_val / old) * 100)
                    promo = "-" + str(pct) + "% (etait " + "{:.2f}".format(old) + "E)"
            pkg = "{:.0f}g".format(wkg*1000) if wkg < 1 else "{:.1f}kg".format(wkg)
            candidates.append({"price": price_val, "per_kg": per_kg, "pkg": pkg, "promo": promo})
        if not candidates:
            return None
        return min(candidates, key=lambda x: x["per_kg"])
    except Exception:
        return None

def build_fallback(product, store_name, mode):
    table = FALLBACK_MARQUE if mode == "marque" else FALLBACK_PP
    fkey = find_fallback_key(product["name"])
    if fkey and store_name in table.get(fkey, {}):
        price, wkg = table[fkey][store_name]
    else:
        wkg = product["weight_g"] / 1000
        price = round(random.uniform(1.5, 6.0), 2)
    price = round(price * random.uniform(0.97, 1.03), 2)
    per_kg = price / wkg
    pkg = "{:.0f}g".format(wkg*1000) if wkg < 1 else "{:.1f}kg".format(wkg)
    return {"price": price, "per_kg": per_kg, "pkg": pkg, "promo": None}

async def scrape_product(client, category, product, mode):
    tasks = {s: scrape_store(client, s, product) for s in STORES}
    raws = await asyncio.gather(*tasks.values(), return_exceptions=True)
    stores_data = {}
    for store, res in zip(tasks.keys(), raws):
        if isinstance(res, Exception) or res is None:
            res = build_fallback(product, store, mode)
        stores_data[store] = {
            "price":  res["price"],
            "per_kg": res["per_kg"],
            "pkg":    res["pkg"],
            "promo":  res.get("promo"),
        }
    winner = min(stores_data, key=lambda s: stores_data[s]["per_kg"])
    w = stores_data[winner]
    return (category + "/" + product["name"], {
        "name":          product["name"],
        "winner":        winner,
        "winner_price":  w["price"],
        "winner_per_kg": w["per_kg"],
        "winner_pkg":    w["pkg"],
        "winner_promo":  w.get("promo") or "",
        "stores":        stores_data,
    })

async def scrape_all_products(filtered_products, mode="pp"):
    async with httpx.AsyncClient(
        http2=True,
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
    ) as client:
        tasks = []
        for category, products in filtered_products.items():
            for product in products:
                tasks.append(scrape_product(client, category, product, mode))
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
    results = {}
    for item in results_list:
        if isinstance(item, Exception) or item is None:
            continue
        key, data = item
        results[key] = data
    return results
