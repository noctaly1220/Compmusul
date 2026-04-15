# Catalogue des produits
# Format: { "Categorie": [ { "name": str, "keywords_marque": [str], "keywords_pp": [str], "weight_g": int } ] }
# keywords_marque = marques connues (Bonduelle, Herta...)
# keywords_pp     = premier prix / MDD (sans marque)

PRODUCTS = {
    "Proteines": [
        {
            "name": "Poitrine de poulet",
            "keywords_marque": ["poulet rotisserie label rouge", "filet poulet Herta"],
            "keywords_pp":     ["poitrine poulet", "filet poulet"],
            "weight_g": 1000,
        },
        {
            "name": "Viande hachee 5% MG",
            "keywords_marque": ["viande hachee 5 Charal", "hache boeuf 5 Bigard"],
            "keywords_pp":     ["viande hachee 5%", "hache boeuf 5"],
            "weight_g": 500,
        },
        {
            "name": "Viande hachee 10% MG",
            "keywords_marque": ["viande hachee 10 Charal", "hache boeuf 10 Bigard"],
            "keywords_pp":     ["viande hachee 10%", "hache boeuf 10"],
            "weight_g": 500,
        },
        {
            "name": "Skyr nature",
            "keywords_marque": ["skyr Arla", "skyr Siggi"],
            "keywords_pp":     ["skyr nature", "skyr 0%"],
            "weight_g": 500,
        },
        {
            "name": "Carre blanc 0%",
            "keywords_marque": ["fromage blanc 0 Danone", "fromage blanc 0 Yoplait"],
            "keywords_pp":     ["carre blanc 0", "fromage blanc 0%"],
            "weight_g": 500,
        },
        {
            "name": "Truite filet",
            "keywords_marque": ["truite fumee Labeyrie", "truite filet Farne"],
            "keywords_pp":     ["filet truite", "truite fumee"],
            "weight_g": 250,
        },
        {
            "name": "Thon en boite (eau)",
            "keywords_marque": ["thon Petit Navire", "thon Saupiquet"],
            "keywords_pp":     ["thon eau naturelle", "thon boite"],
            "weight_g": 160,
        },
        {
            "name": "Pave de saumon fume",
            "keywords_marque": ["saumon fume Labeyrie", "saumon Pacific"],
            "keywords_pp":     ["saumon fume", "pave saumon"],
            "weight_g": 200,
        },
    ],
    "Legumes Surgeles": [
        {
            "name": "Myrtilles surgelees",
            "keywords_marque": ["myrtilles Picard", "myrtilles Bonduelle"],
            "keywords_pp":     ["myrtilles surgelees", "myrtille surgele"],
            "weight_g": 500,
        },
        {
            "name": "Brocoli surgele",
            "keywords_marque": ["brocoli Bonduelle", "brocoli Picard"],
            "keywords_pp":     ["brocoli surgele", "brocoli surgele"],
            "weight_g": 1000,
        },
        {
            "name": "Epinards surgeles",
            "keywords_marque": ["epinards Bonduelle", "epinards Picard"],
            "keywords_pp":     ["epinards surgeles", "epinards surgele"],
            "weight_g": 750,
        },
        {
            "name": "Chou-fleur surgele",
            "keywords_marque": ["choufleur Bonduelle", "choufleur Picard"],
            "keywords_pp":     ["chou-fleur surgele", "choufleur surgele"],
            "weight_g": 1000,
        },
        {
            "name": "Haricots verts surgeles",
            "keywords_marque": ["haricots verts Bonduelle", "haricots Picard"],
            "keywords_pp":     ["haricots verts surgeles", "haricots surgele"],
            "weight_g": 1000,
        },
    ],
    "Feculents": [
        {
            "name": "Riz Basmati blanc",
            "keywords_marque": ["riz basmati Taureau Aile", "basmati Uncle Ben's"],
            "keywords_pp":     ["riz basmati blanc", "riz basmati"],
            "weight_g": 1000,
        },
        {
            "name": "Riz Basmati complet",
            "keywords_marque": ["riz basmati complet Taureau", "basmati complet bio"],
            "keywords_pp":     ["riz basmati complet", "riz complet basmati"],
            "weight_g": 1000,
        },
        {
            "name": "Riz complet",
            "keywords_marque": ["riz complet Taureau Aile", "riz brun Uncle Ben"],
            "keywords_pp":     ["riz complet", "riz brun"],
            "weight_g": 1000,
        },
        {
            "name": "Lentilles vertes",
            "keywords_marque": ["lentilles Vivien Paille", "lentilles du Puy AOP"],
            "keywords_pp":     ["lentilles vertes", "lentilles"],
            "weight_g": 500,
        },
    ],
}
