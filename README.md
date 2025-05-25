# Invoice Extractor

Un outil d'extraction de données de factures basé sur la vision par ordinateur et le traitement d'images.

## Fonctionnalités

- Analyse d'images de factures (JPG, PNG, PDF)
- Détection des zones de texte et OCR
- Regroupement intelligent des données par position verticale
- Extraction structurée des informations clés :
  - Informations d'en-tête (fournisseur, numéro de facture, date, montant total)
  - Lignes de produits/services (description, quantité, prix unitaire, total ligne)
  - Informations fiscales (labels et montants des taxes)
- Export au format JSON normalisé

## Installation

```bash
git clone https://github.com/votre-nom/invoice-extractor.git
cd invoice-extractor
pip install -r requirements.txt

# Installation de Tesseract OCR si nécessaire
# Sur Ubuntu/Debian: apt-get install tesseract-ocr
# Sur MacOS: brew install tesseract
# Sur Windows: télécharger l'installateur depuis https://github.com/UB-Mannheim/tesseract/wiki
```

## Utilisation

```bash
# Traiter une seule facture
python src/main.py --input sample_data/invoice_001.jpg --output result.json

# Traiter un dossier de factures
python src/main.py --input-dir ./factures/ --output-dir ./resultats/
```

## Approche technique

1. **Détection et OCR** : Utilisation d'OpenCV et Tesseract pour la détection des zones de texte et l'OCR
2. **Analyse de disposition** : Regroupement des zones de texte par proximité verticale (même ordonnée Y ± tolérance)
3. **Classification sémantique** : Attribution des groupes de texte aux champs appropriés via des expressions régulières et des mots-clés
4. **Structuration des données** : Organisation des informations extraites dans un modèle JSON normalisé validé par Pydantic

## Structure du projet

```
invoice-extractor/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py       # Point d'entrée CLI
│   ├── ocr.py        # Détection + OCR
│   ├── layout.py     # Regroupement par position Y
│   ├── parser.py     # Mapping vers le schéma JSON
│   ├── schemas.py    # Modèles Pydantic
│   └── utils/
│       └── geometry.py  # Calcul de distances, IoU, etc.
├── tests/
│   └── test_parser.py
└── sample_data/
    └── invoice_001.jpg
```

## Licence

MIT