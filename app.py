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
    background: #000 !important; color: #fff;
    font-family: 'DM Mono', monospace;
}
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stMain"] > div {
    padding: 0 16px 40px 16px !important;
    max-width: 480px !important; margin: 0 auto !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], footer, #MainMenu, .stDeployButton { display: none !important; }

.app-header { padding: 32px 0 20px 0; text-align: center; border-bottom: 1px solid #1a1a1a; margin-bottom: 20px; }
.app-title { font-family: 'Bebas Neue', sans-serif; font-size: 52px; letter-spacing: 4px; color: #C6F135; line-height: 1; }
.app-subtitle { font-size: 10px; color: #444; letter-spacing: 2px; text-transform: uppercase; margin-top: 6px; }

.toggle-row { display: flex; gap: 0; margin-bottom: 20px; border: 1px solid #222; border-radius: 4px; overflow: hidden; }
.toggle-opt {
    flex: 1; padding: 10px 0; text-align: center;
    font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
    cursor: pointer; color: #444; background: #0a0a0a;
    border: none; font-family: 'DM Mono', monospace;
}
.toggle-opt.active { background: #C6F135; color: #000; font-weight: bold; }

.stButton > button {
    width: 100% !important; background: #C6F135 !important; color: #000 !important;
    font-family: 'Bebas Neue', sans-serif !important; font-size: 26px !important;
    letter-spacing: 3px !important; border: none !important; border-radius: 3px !important;
    padding: 16px 0 !important; margin-bottom: 24px !important;
    box-shadow: 0 0 30px rgba(198,241,53,0.15) !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

.section-title {
    font-size: 10px; letter-spacing: 3px; color: #333; text-transform: uppercase;
    margin: 16px 0 10px 0; padding-bottom: 8px; border-bottom: 1px solid #111;
}
.product-card {
    background: #0a0a0a; border: 1px solid #181818;
    border-radius: 4px; padding: 16px; margin-bottom: 10px; position: relative;
}
.product-card.winner { border-color: #C6F135; }
.product-name { font-size: 10px; color: #555; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
.product-price { font-family: 'Bebas Neue', sans-serif; font-size: 40px; color: #fff; letter-spacing: 2px; line-height: 1; }
.product-pkg { font-size: 10px; color: #333; margin-left: 4px; }
.price-per-kg { font-size: 13px; color: #C6F135; margin-top: 2px; }
.promo-tag { font-size: 9px; color: #ff6b35; letter-spacing: 1px; text-transform: uppercase; margin-top: 5px; }
.winner-badge {
    position: absolute; top: -1px; right: -1px;
    background: #C6F135; color: #000;
    font-family: 'Bebas Neue', sans-serif; font-size: 11px;
    letter-spacing: 2px; padding: 3px 10px; border-radius: 0 4px 0 4px;
}
.stores-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 10px; }
.store-price-row { background: #111; padding: 7px 9px; border-radius: 2px; }
.store-price-name { font-size: 9px; color: #444; letter-spacing: 1px; text-transform: uppercase; }
.store-price-val { font-family: 'Bebas Neue', sans-serif; font-size: 19px; color: #888; }
.store-price-val.best { color: #C6F135; }
.store-price-kg { font-size: 9px; color: #333; }
.store-badge {
    display: inline-block; padding: 3px 8px; font-size: 9px;
    letter-spacing: 2px; text-transform: uppercase; border-radius: 2px; margin-top: 8px;
}
.badge-leclerc     { background: #00205b22; color: #4a9eff; border: 1px solid #4a9eff44; }
.badge-carrefour   { background: #ff000022; color: #ff4444; border: 1px solid #ff444444; }
.badge-auchan      { background: #ff450022; color: #ff7f00; border: 1px solid #ff7f0044; }
.badge-lidl        { background: #ffd60022; color: #ffd600; border: 1px solid #ffd60044; }
.badge-casino      { background: #e5000022; color: #ff6699; border: 1px solid #ff669944; }
.badge-intermarche { background: #00800022; color: #00cc66; border: 1px solid #00cc6644; }
.badge-aldi        { background: #00529b22; color: #00aaff; border: 1px solid #00aaff44; }
.stProgress > div > div { background-color: #C6F135 !important; }
.status-msg { font-size: 11px; color: #444; letter-spacing: 1px; text-align: center; padding: 12px 0; }
.mode-label { font-size: 10px; color: #333; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-title">PRIX MUSCU</div>
    <div class="app-subtitle">Leclerc · Carrefour · Auchan · Lidl · Casino · Intermarche · Aldi</div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "category" not in st.session_state:
    st.session_state.category = "Tous"
if "mode" not in st.session_state:
    st.session_state.mode = "pp"   # "pp" = premier prix, "marque" = marque

# ── TOGGLE MARQUE / PREMIER PRIX ─────────────────────────────────────────────
st.markdown('<div class="mode-label">Type de produit</div>', unsafe_allow_html=True)
col_pp, col_mq = st.columns(2)
with col_pp:
    pp_type = "primary" if st.session_state.mode == "pp" else "secondary"
    if st.button("PREMIER PRIX", key="mode_pp", use_container_width=True, type=pp_type):
        st.session_state.mode = "pp"
        st.rerun()
with col_mq:
    mq_type = "primary" if st.session_state.mode == "marque" else "secondary"
    if st.button("MARQUE", key="mode_mq", use_container_width=True, type=mq_type):
        st.session_state.mode = "marque"
        st.rerun()

st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

# ── CATEGORY FILTER ───────────────────────────────────────────────────────────
CATEGORIES = ["Tous", "Proteines", "Legumes Surgeles", "Feculents"]
CAT_LABELS  = {"Tous": "Tous", "Proteines": "Proteines", "Legumes Surgeles": "Legumes", "Feculents": "Feculents"}

cols = st.columns(len(CATEGORIES))
for i, cat in enumerate(CATEGORIES):
    with cols[i]:
        t = "primary" if st.session_state.category == cat else "secondary"
        if st.button(CAT_LABELS[cat], key="cat_" + str(i), type=t, use_container_width=True):
            st.session_state.category = cat
            st.rerun()

st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

# ── COMPARE BUTTON ────────────────────────────────────────────────────────────
compare_clicked = st.button("COMPARER", use_container_width=True)

# ── STORE BADGES ──────────────────────────────────────────────────────────────
STORE_BADGE = {
    "Leclerc":     "badge-leclerc",
    "Carrefour":   "badge-carrefour",
    "Auchan":      "badge-auchan",
    "Lidl":        "badge-lidl",
    "Casino":      "badge-casino",
    "Intermarche": "badge-intermarche",
    "Aldi":        "badge-aldi",
}

# ── RENDER HELPERS ────────────────────────────────────────────────────────────
def render_card(result):
    winner      = result["winner"]
    badge_cls   = STORE_BADGE.get(winner, "badge-leclerc")
    promo       = result.get("winner_promo", "")
    stores      = result["stores"]

    rows_html = ""
    for sname, sd in sorted(stores.items(), key=lambda x: x[1]["per_kg"]):
        best_cls = "best" if sname == winner else ""
        pf = " 🔥" if sd.get("promo") else ""
        rows_html += (
            "<div class='store-price-row'>"
            "<div class='store-price-name'>" + sname + pf + "</div>"
            "<div class='store-price-val " + best_cls + "'>" + "{:.2f}".format(sd["price"]) + "E</div>"
            "<div class='store-price-kg'>" + "{:.2f}".format(sd["per_kg"]) + " E/kg</div>"
            "</div>"
        )

    promo_html = "<div class='promo-tag'>🔥 " + promo + "</div>" if promo else ""

    st.markdown(
        "<div class='product-card winner'>"
        "<div class='winner-badge'>MEILLEUR PRIX</div>"
        "<div class='product-name'>" + result["name"] + "</div>"
        "<div><span class='product-price'>" + "{:.2f}".format(result["winner_price"]) + "E</span>"
        "<span class='product-pkg'> " + result["winner_pkg"] + "</span></div>"
        "<div class='price-per-kg'>" + "{:.2f}".format(result["winner_per_kg"]) + " E/kg</div>"
        + promo_html +
        "<span class='store-badge " + badge_cls + "'>" + winner + "</span>"
        "<div class='stores-grid'>" + rows_html + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_placeholder(name):
    st.markdown(
        "<div class='product-card'>"
        "<div class='product-name'>" + name + "</div>"
        "<div class='product-price' style='color:#1a1a1a'>--E</div>"
        "<div class='price-per-kg' style='color:#1a1a1a'>-- E/kg</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ── MAIN LOGIC ────────────────────────────────────────────────────────────────
cat_filter = st.session_state.category
mode       = st.session_state.mode  # "pp" or "marque"

filtered = {
    cat: prods for cat, prods in PRODUCTS.items()
    if cat_filter == "Tous" or cat == cat_filter
}

if compare_clicked:
    # Injecter le bon set de keywords selon le mode
    filtered_with_kw = {}
    for cat, prods in filtered.items():
        adapted = []
        for p in prods:
            kw_key = "keywords_marque" if mode == "marque" else "keywords_pp"
            adapted.append({
                "name":     p["name"],
                "keywords": p.get(kw_key) or p.get("keywords_pp") or [""],
                "weight_g": p["weight_g"],
            })
        filtered_with_kw[cat] = adapted

    progress_bar = st.progress(0, text="Connexion aux enseignes...")

    with st.spinner("Analyse en cours..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            raw = loop.run_until_complete(scrape_all_products(filtered_with_kw, mode=mode))
        finally:
            loop.close()

    progress_bar.progress(1.0, text="Analyse terminee ✓")

    if not raw:
        st.markdown("<div class='status-msg'>Aucun resultat — verifie ta connexion.</div>", unsafe_allow_html=True)
    else:
        for cat, prods in filtered_with_kw.items():
            st.markdown("<div class='section-title'>" + cat + "</div>", unsafe_allow_html=True)
            for product in prods:
                key = cat + "/" + product["name"]
                if key in raw and raw[key]:
                    render_card(raw[key])
                else:
                    st.markdown(
                        "<div class='product-card'>"
                        "<div class='product-name'>" + product["name"] + "</div>"
                        "<div style='font-size:11px;color:#333;margin-top:6px'>Prix indisponible</div>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
else:
    for cat, prods in filtered.items():
        st.markdown("<div class='section-title'>" + cat + "</div>", unsafe_allow_html=True)
        for p in prods:
            render_placeholder(p["name"])
