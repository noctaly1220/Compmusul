import streamlit as st
import asyncio
from scraper import scrape_all_products
from products import PRODUCTS

st.set_page_config(
    page_title="PRIX MUSCU",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #000 !important;
    color: #fff;
    font-family: 'DM Mono', monospace;
}
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stMain"] > div {
    padding: 0 16px 40px 16px !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
footer { display: none !important; }
#MainMenu { display: none; }
.stDeployButton { display: none; }

.app-header {
    padding: 36px 0 24px 0;
    text-align: center;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 24px;
}
.app-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    letter-spacing: 4px;
    color: #C6F135;
    line-height: 1;
}
.app-subtitle {
    font-size: 11px;
    color: #444;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 8px;
}
.stButton > button {
    width: 100% !important;
    background: #C6F135 !important;
    color: #000 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 26px !important;
    letter-spacing: 3px !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 16px 0 !important;
    cursor: pointer !important;
    margin-bottom: 28px !important;
    box-shadow: 0 0 30px rgba(198,241,53,0.15) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    box-shadow: 0 0 40px rgba(198,241,53,0.3) !important;
}
.section-title {
    font-size: 10px;
    letter-spacing: 3px;
    color: #333;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #111;
}
.product-card {
    background: #0a0a0a;
    border: 1px solid #181818;
    border-radius: 4px;
    padding: 18px 16px;
    margin-bottom: 12px;
    position: relative;
}
.product-card.winner { border-color: #C6F135; }
.product-name {
    font-size: 10px;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.product-price {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px;
    color: #fff;
    letter-spacing: 2px;
    line-height: 1;
}
.product-pkg { font-size: 10px; color: #333; margin-left: 4px; }
.price-per-kg { font-size: 13px; color: #C6F135; margin-top: 2px; font-weight: 500; }
.store-badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-radius: 2px;
    margin-top: 10px;
    font-weight: 500;
}
.promo-tag { font-size: 9px; color: #ff6b35; letter-spacing: 1px; text-transform: uppercase; margin-top: 6px; }
.winner-badge {
    position: absolute;
    top: -1px; right: -1px;
    background: #C6F135;
    color: #000;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 11px;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 0 4px 0 4px;
}
.stores-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
.store-price-row { background: #111; padding: 8px 10px; border-radius: 2px; }
.store-price-name { font-size: 9px; color: #444; letter-spacing: 1px; text-transform: uppercase; }
.store-price-val { font-family: 'Bebas Neue', sans-serif; font-size: 20px; color: #888; }
.store-price-val.best { color: #C6F135; }
.store-price-kg { font-size: 9px; color: #333; }
.badge-leclerc   { background: #00205b22; color: #4a9eff; border: 1px solid #4a9eff44; }
.badge-carrefour { background: #00205b22; color: #ff4444; border: 1px solid #ff444444; }
.badge-auchan    { background: #ff450022; color: #ff7f00; border: 1px solid #ff7f0044; }
.badge-lidl      { background: #ffd60022; color: #ffd600; border: 1px solid #ffd60044; }
.badge-casino    { background: #e5000022; color: #ff6699; border: 1px solid #ff669944; }
.stProgress > div > div { background-color: #C6F135 !important; }
.status-msg { font-size: 11px; color: #444; letter-spacing: 1px; text-align: center; padding: 12px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <div class="app-title">PRIX MUSCU</div>
    <div class="app-subtitle">Leclerc &middot; Carrefour &middot; Auchan &middot; Lidl &middot; Casino</div>
</div>
""", unsafe_allow_html=True)

CATEGORIES = ["Tous", "Proteines", "Legumes Surgeles", "Feculents"]
CAT_LABELS = {
    "Tous": "Tous",
    "Proteines": "Proteines",
    "Legumes Surgeles": "Legumes",
    "Feculents": "Feculents",
}

if "category" not in st.session_state:
    st.session_state.category = "Tous"

cols = st.columns(len(CATEGORIES))
for i, cat in enumerate(CATEGORIES):
    with cols[i]:
        is_active = st.session_state.category == cat
        if st.button(
            CAT_LABELS[cat],
            key="cat_" + str(i),
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.category = cat
            st.rerun()

st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

compare_clicked = st.button("COMPARER", use_container_width=True)

STORE_BADGE = {
    "Leclerc":   "badge-leclerc",
    "Carrefour": "badge-carrefour",
    "Auchan":    "badge-auchan",
    "Lidl":      "badge-lidl",
    "Casino":    "badge-casino",
}


def render_card(result):
    winner = result["winner"]
    winner_price = result["winner_price"]
    winner_pkg = result["winner_pkg"]
    winner_per_kg = result["winner_per_kg"]
    promo = result.get("winner_promo", "")
    stores = result["stores"]
    badge_cls = STORE_BADGE.get(winner, "badge-leclerc")

    other_stores_html = ""
    for store_name, sdata in sorted(stores.items(), key=lambda x: x[1]["per_kg"]):
        is_best = store_name == winner
        val_cls = "best" if is_best else ""
        price_display = "{:.2f}".format(sdata["price"]) + "EUR"
        kg_display = "{:.2f}".format(sdata["per_kg"]) + "EUR/kg"
        promo_flag = " 🔥" if sdata.get("promo") else ""
        other_stores_html += (
            "<div class=\"store-price-row\">"
            "<div class=\"store-price-name\">" + store_name + promo_flag + "</div>"
            "<div class=\"store-price-val " + val_cls + "\">" + price_display + "</div>"
            "<div class=\"store-price-kg\">" + kg_display + "</div>"
            "</div>"
        )

    promo_html = "<div class=\"promo-tag\">🔥 " + promo + "</div>" if promo else ""

    price_str = "{:.2f}".format(winner_price) + "EUR"
    pkg_str = winner_pkg
    per_kg_str = "{:.2f}".format(winner_per_kg) + " EUR/kg"
    prod_name = result["name"]

    st.markdown(
        "<div class=\"product-card winner\">"
        "<div class=\"winner-badge\">MEILLEUR PRIX</div>"
        "<div class=\"product-name\">" + prod_name + "</div>"
        "<div><span class=\"product-price\">" + price_str + "</span>"
        "<span class=\"product-pkg\">" + pkg_str + "</span></div>"
        "<div class=\"price-per-kg\">" + per_kg_str + "</div>"
        + promo_html +
        "<span class=\"store-badge " + badge_cls + "\">" + winner + "</span>"
        "<div class=\"stores-grid\">" + other_stores_html + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_placeholder_card(name):
    st.markdown(
        "<div class=\"product-card\">"
        "<div class=\"product-name\">" + name + "</div>"
        "<div class=\"product-price\" style=\"color:#222\">-- EUR</div>"
        "<div class=\"price-per-kg\" style=\"color:#222\">-- EUR/kg</div>"
        "<div class=\"status-msg\">En attente...</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# Map display category to PRODUCTS keys
CAT_MAP = {
    "Tous": None,
    "Proteines": "Proteines",
    "Legumes Surgeles": "Legumes Surgeles",
    "Feculents": "Feculents",
}

if compare_clicked:
    cat_filter = st.session_state.category
    filtered = {
        cat: prods for cat, prods in PRODUCTS.items()
        if cat_filter == "Tous" or cat == cat_filter
    }

    progress_bar = st.progress(0, text="Connexion aux enseignes...")

    with st.spinner("Analyse en cours..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            raw = loop.run_until_complete(scrape_all_products(filtered))
        finally:
            loop.close()

    progress_bar.progress(1.0, text="Analyse terminee")

    for cat, prods in filtered.items():
        st.markdown(
            "<div class=\"section-title\">" + cat + "</div>",
            unsafe_allow_html=True,
        )
        for product in prods:
            key = cat + "/" + product["name"]
            if key in raw and raw[key]:
                render_card(raw[key])
            else:
                st.markdown(
                    "<div class=\"product-card\">"
                    "<div class=\"product-name\">" + product["name"] + "</div>"
                    "<div style=\"font-size:11px;color:#333;margin-top:8px;\">Prix non disponible</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
else:
    st.markdown(
        "<div class=\"status-msg\">Appuie sur COMPARER pour lancer l'analyse.</div>",
        unsafe_allow_html=True,
    )
    for cat, prods in PRODUCTS.items():
        if st.session_state.category == "Tous" or st.session_state.category == cat:
            st.markdown(
                "<div class=\"section-title\">" + cat + "</div>",
                unsafe_allow_html=True,
            )
            for p in prods:
                render_placeholder_card(p["name"])
