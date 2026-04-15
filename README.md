# 💪 PRIX MUSCU

Comparateur de prix alimentaires (musculation) — Dark mode, mobile-first.

## Structure du projet

```
├── app.py           # Interface Streamlit principale
├── scraper.py       # Scraping asynchrone Playwright
├── products.py      # Catalogue des produits
├── requirements.txt # Dépendances Python
├── packages.txt     # Dépendances système (Chromium)
└── setup.sh         # Post-install script (install Playwright browsers)
```

## Déploiement sur Streamlit Cloud

### 1. Créer un repo GitHub
Pousse tous les fichiers à la racine du repo.

### 2. Connecter sur share.streamlit.io
- App file : `app.py`
- Python version : 3.11+

### 3. Ajouter le post-install script
Dans les paramètres avancés de l'app Streamlit Cloud :
- **"Custom install commands"** → `bash setup.sh`  
ou créer un fichier `.streamlit/config.toml` avec :
```toml
[server]
runOnSave = false
```

### 4. Variables d'environnement (optionnel)
Si tu veux proxifier les requêtes (recommandé pour la prod) :
```
PLAYWRIGHT_PROXY_SERVER=http://...
PLAYWRIGHT_PROXY_USERNAME=...
PLAYWRIGHT_PROXY_PASSWORD=...
```
Puis dans `scraper.py`, passer les options proxy à `browser.new_context(...)`.

## Lancer en local

```bash
pip install -r requirements.txt
playwright install chromium
streamlit run app.py
```

## Personnalisation

### Ajouter un produit
Dans `products.py`, ajoute un dict dans la bonne catégorie :
```python
{"name": "Blanc d'œuf liquide", "keywords": ["blanc oeuf liquide"], "weight_g": 1000},
```

### Ajouter une enseigne
1. Ajoute l'URL dans `STORES` dans `scraper.py`
2. Ajoute les sélecteurs CSS dans `SELECTORS`
3. Ajoute la couleur du badge dans `STORE_BADGE` dans `app.py`

## ⚠️ Notes importantes

- Le scraping peut être bloqué par les sites si les sélecteurs CSS changent.
  → Inspecte la page avec les DevTools et mets à jour `SELECTORS` dans `scraper.py`.
- Pour une version robuste en production, envisage un service de proxy rotatif
  (BrightData, Oxylabs) ou une API de prix dédiée (Ouestfrance-immo ou équivalent GMS).
- Les promotions "carte fidélité" ne sont visibles qu'une fois connecté → 
  le scraper ne capture que les promo immédiates (barre de prix barrée).
