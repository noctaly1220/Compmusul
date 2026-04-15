"""
scraper.py — Scraping asynchrone (Playwright stealth) des prix GMS
Enseignes : Leclerc Drive, Carrefour Drive, Auchan Drive, Lidl, Casino Drive
"""

import asyncio
import re
import random
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser

# ─── CONFIG ──────────────────────────────────────────────────────────────────

STORES = {
    "Leclerc":   "https://www.e.leclerc/recherche?q={query}",
    "Carrefour": "https://www.carrefour.fr/s?q={query}&lang=fr_FR",
    "Auchan":    "https://www.auchan.fr/recherche?query={query}",
    "Lidl":      "https://www.lidl.fr/p/{query}",
    "Casino":    "https://www.casino.fr/search?q={query}",
}

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.111 Mobile/15E148 Safari/604.1",
]

# Sélecteurs CSS par enseigne — à ajuster si les sites changent leur structure
SELECTORS = {
    "Leclerc": {
        "card":      "[data-testid='product-card'], .product-card",
        "name":      "[data-testid='product-title'], .product-card__title",
        "price":     "[data-testid='price-amount'], .price__amount",
        "promo":     "[data-testid='crossed-price'], .price--crossed",
        "weight":    "[data-testid='weight'], .product-card__weight, .grammage",
    },
    "Carrefour": {
        "card":      ".product-card-article, [data-testid='product-card']",
        "name":      ".product-card__title, [data-testid='product-name']",
        "price":     ".product-card__price--current, [data-testid='price']",
        "promo":     ".product-card__price--old",
        "weight":    ".product-card__weight, .grammage",
    },
    "Auchan": {
        "card":      ".product-thumbnail, [class*='product-card']",
        "name":      ".product-thumbnail__title, [class*='product-name']",
        "price":     ".product-thumbnail__price, [class*='price-value']",
        "promo":     "[class*='price-old'], [class*='price-crossed']",
        "weight":    "[class*='weight'], [class*='grammage']",
    },
    "Lidl": {
        "card":      ".product-grid-box, [class*='ProductBox']",
        "name":      ".product-grid-box__title, [class*='ProductBox__title']",
        "price":     ".m-price__price, [class*='PriceBox']",
        "promo":     ".m-price__rrp",
        "weight":    "[class*='weight'], [class*='quantity']",
    },
    "Casino": {
        "card":      ".product-item, [class*='product-card']",
        "name":      ".product-item-name, [class*='product-title']",
        "price":     ".price, [class*='product-price']",
        "promo":     ".old-price, [class*='price-old']",
        "weight":    "[class*='weight'], [class*='grammage']",
    },
}

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def parse_price(text: str) -> Optional[float]:
    """Extrait un float depuis un texte type '3,49 €' ou '3.49€'."""
    if not text:
        return None
    cleaned = text.replace(",", ".").replace("\xa0", "").replace(" ", "")
    m = re.search(r"(\d+\.\d{1,2})", cleaned)
    return float(m.group(1)) if m else None


def parse_weight_kg(text: str) -> Optional[float]:
    """Retourne un poids en kg depuis '500g', '1kg', '1,5 kg', etc."""
    if not text:
        return None
    text = text.lower().replace(",", ".").replace(" ", "")
    m_kg = re.search(r"(\d+\.?\d*)\s*kg", text)
    if m_kg:
        return float(m_kg.group(1))
    m_g = re.search(r"(\d+\.?\d*)\s*g", text)
    if m_g:
        return float(m_g.group(1)) / 1000
    m_cl = re.search(r"(\d+\.?\d*)\s*cl", text)
    if m_cl:
        return float(m_cl.group(1)) / 100
    m_l = re.search(r"(\d+\.?\d*)\s*l", text)
    if m_l:
        return float(m_l.group(1))
    return None


def weight_from_name(name: str) -> Optional[float]:
    """Essaie d'extraire le poids directement depuis le nom du produit."""
    return parse_weight_kg(name)


async def human_delay(min_ms=400, max_ms=1200):
    await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


async def stealth_setup(page: Page, ua: str):
    """Applique des patches anti-bot basiques."""
    await page.set_extra_http_headers({
        "User-Agent":      ua,
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT":             "1",
    })
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3] });
        window.chrome = { runtime: {} };
    """)

# ─── SCRAPING PAR ENSEIGNE ───────────────────────────────────────────────────

async def scrape_store(browser: Browser, store_name: str, product: dict) -> Optional[dict]:
    """
    Scrape une enseigne pour un produit donné.
    Retourne un dict {price, per_kg, pkg, promo, store} ou None.
    """
    keyword = product["keywords"][0]
    fallback_weight_kg = product["weight_g"] / 1000
    url = STORES[store_name].format(query=keyword.replace(" ", "+"))
    sel = SELECTORS[store_name]

    context = await browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent=random.choice(USER_AGENTS),
        locale="fr-FR",
        timezone_id="Europe/Paris",
    )
    page = await context.new_page()
    await stealth_setup(page, random.choice(USER_AGENTS))

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await human_delay(600, 1400)

        # Accepter cookies si nécessaire
        for btn_text in ["Accepter", "Tout accepter", "J'accepte", "OK"]:
            try:
                btn = page.get_by_role("button", name=re.compile(btn_text, re.I))
                if await btn.count() > 0:
                    await btn.first.click(timeout=3000)
                    await human_delay(300, 600)
                    break
            except Exception:
                pass

        await human_delay(400, 800)

        # Chercher les cartes produits
        cards = await page.query_selector_all(sel["card"])
        if not cards:
            return None

        # Prendre les 3 premiers résultats, garder le moins cher
        candidates = []
        for card in cards[:5]:
            try:
                name_el  = await card.query_selector(sel["name"])
                price_el = await card.query_selector(sel["price"])
                if not name_el or not price_el:
                    continue

                name_txt  = (await name_el.inner_text()).strip()
                price_txt = (await price_el.inner_text()).strip()
                price_val = parse_price(price_txt)
                if not price_val:
                    continue

                # Poids
                weight_kg = None
                weight_el = await card.query_selector(sel["weight"])
                if weight_el:
                    weight_txt = (await weight_el.inner_text()).strip()
                    weight_kg  = parse_weight_kg(weight_txt)
                if not weight_kg:
                    weight_kg = weight_from_name(name_txt) or fallback_weight_kg

                per_kg = price_val / weight_kg

                # Promo
                promo_txt = None
                promo_el  = await card.query_selector(sel["promo"])
                if promo_el:
                    raw = (await promo_el.inner_text()).strip()
                    old = parse_price(raw)
                    if old and old > price_val:
                        pct = round((1 - price_val / old) * 100)
                        promo_txt = f"-{pct}% (était {old:.2f}€)"

                pkg_str = f"{weight_kg*1000:.0f}g" if weight_kg < 1 else f"{weight_kg:.1f}kg"

                candidates.append({
                    "price":  price_val,
                    "per_kg": per_kg,
                    "pkg":    pkg_str,
                    "promo":  promo_txt,
                    "store":  store_name,
                    "name":   name_txt,
                })
            except Exception:
                continue

        if not candidates:
            return None

        # Meilleur €/kg parmi les candidats
        best = min(candidates, key=lambda x: x["per_kg"])
        return best

    except Exception:
        return None
    finally:
        await context.close()


# ─── ORCHESTRATION ASYNCHRONE ────────────────────────────────────────────────

async def scrape_product(browser: Browser, category: str, product: dict) -> tuple:
    """Lance le scraping en parallèle sur toutes les enseignes pour 1 produit."""
    tasks = {
        store: scrape_store(browser, store, product)
        for store in STORES
    }
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    stores_data = {}
    for store, res in zip(tasks.keys(), results):
        if isinstance(res, Exception) or res is None:
            continue
        stores_data[store] = {
            "price":  res["price"],
            "per_kg": res["per_kg"],
            "pkg":    res["pkg"],
            "promo":  res.get("promo"),
        }

    if not stores_data:
        return (f"{category}/{product['name']}", None)

    winner = min(stores_data, key=lambda s: stores_data[s]["per_kg"])
    w = stores_data[winner]

    return (f"{category}/{product['name']}", {
        "name":          product["name"],
        "winner":        winner,
        "winner_price":  w["price"],
        "winner_per_kg": w["per_kg"],
        "winner_pkg":    w["pkg"],
        "winner_promo":  w.get("promo", ""),
        "stores":        stores_data,
    })


async def scrape_all_products(filtered_products: dict) -> dict:
    """
    Point d'entrée principal.
    Reçoit le dict filtré { catégorie: [produits] } et retourne les résultats.
    """
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        tasks = []
        for category, products in filtered_products.items():
            for product in products:
                tasks.append(scrape_product(browser, category, product))

        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        await browser.close()

    results = {}
    for item in results_list:
        if isinstance(item, Exception) or item is None:
            continue
        key, data = item
        results[key] = data

    return results
