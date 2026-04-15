# Catalogue des produits à comparer
# Format: { "Catégorie": [ { "name": str, "keywords": [str], "weight_g": int } ] }
#
# weight_g  = poids de référence pour le calcul €/kg quand le scraper ne le détecte pas

PRODUCTS = {
    "Protéines": [
        {"name": "Poitrine de poulet",        "keywords": ["poitrine poulet", "filet poulet"], "weight_g": 1000},
        {"name": "Viande hachée 5% MG",       "keywords": ["viande hachée 5%", "haché boeuf 5"], "weight_g": 500},
        {"name": "Viande hachée 10% MG",      "keywords": ["viande hachée 10%", "haché boeuf 10"], "weight_g": 500},
        {"name": "Skyr nature",               "keywords": ["skyr nature", "skyr 0%"], "weight_g": 500},
        {"name": "Carré blanc 0%",            "keywords": ["carré blanc 0", "fromage blanc 0%"], "weight_g": 500},
        {"name": "Truite filet",              "keywords": ["filet truite", "truite fumée"], "weight_g": 250},
        {"name": "Thon en boîte (eau)",       "keywords": ["thon eau naturelle", "thon boîte"], "weight_g": 160},
        {"name": "Pavé de saumon fumé",       "keywords": ["saumon fumé", "pavé saumon"], "weight_g": 200},
    ],
    "Légumes Surgelés": [
        {"name": "Myrtilles surgelées",       "keywords": ["myrtilles surgelées", "myrtille surgele"], "weight_g": 500},
        {"name": "Brocoli surgelé",           "keywords": ["brocoli surgelé", "brocoli surgele"], "weight_g": 1000},
        {"name": "Épinards surgelés",         "keywords": ["épinards surgelés", "epinards surgele"], "weight_g": 750},
        {"name": "Chou-fleur surgelé",        "keywords": ["chou-fleur surgelé", "choufleur surgele"], "weight_g": 1000},
        {"name": "Haricots verts surgelés",   "keywords": ["haricots verts surgelés", "haricots surgele"], "weight_g": 1000},
    ],
    "Féculents": [
        {"name": "Riz Basmati blanc",         "keywords": ["riz basmati blanc", "riz basmati"], "weight_g": 1000},
        {"name": "Riz Basmati complet",       "keywords": ["riz basmati complet", "riz complet basmati"], "weight_g": 1000},
        {"name": "Riz complet",               "keywords": ["riz complet", "riz brun"], "weight_g": 1000},
        {"name": "Lentilles vertes",          "keywords": ["lentilles vertes", "lentilles du puy"], "weight_g": 500},
    ],
}
