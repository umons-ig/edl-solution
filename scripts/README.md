# Scripts de Génération de PDF

Ce dossier contient les scripts Node.js pour générer les PDFs des ateliers.

## 📦 Installation

```bash
cd scripts
npm install
```

## 🚀 Usage

### Générer un PDF spécifique

```bash
# ATELIER-1 uniquement
npm run generate-pdf-atelier1

# ATELIER-2 uniquement
npm run generate-pdf-atelier2
```

### Générer tous les PDFs

```bash
npm run generate-all-pdfs
```

## 📄 Fichiers Générés

Les PDFs sont créés dans le dossier `docs/` :

- `docs/ATELIER-1.pdf` (~618 KB)
- `docs/ATELIER-2.pdf` (~967 KB)

## 🛠️ Technologies

- **Puppeteer** : Génération de PDF via Chromium headless
- **Marked** : Conversion Markdown → HTML
- **Node.js** : Runtime JavaScript

## 📝 Structure

```
scripts/
├── package.json                 # Dépendances et scripts npm
├── generate-pdf.js             # Générateur pour ATELIER-1
├── generate-pdf-atelier2.js    # Générateur pour ATELIER-2
└── README.md                   # Ce fichier
```

## 🎨 Styles

Les PDFs utilisent les mêmes styles pour cohérence :

- Police : System fonts (SF Pro, Segoe UI)
- Couleurs : Bleu (headings), Gris foncé (code blocks)
- Format : A4 avec marges de 15-20mm
- Syntax highlighting : Fond sombre pour les blocs de code

## 🔧 Personnalisation

Pour modifier les styles, éditez les sections `<style>` dans les fichiers `generate-pdf*.js`.
