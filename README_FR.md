# Bulletin Multilingue des Articles Quotidiens HuggingFace

<div align="center">
  <a href="https://internlm.org/">
    <img src="https://internlm.org/assets/logo-a0611363.svg" alt="InternLM" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/">
    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="HuggingFace" height="80"/>
  </a>
</div>

<p align="center">
  <em>Traduction des articles quotidiens HuggingFace avec InternLM</em>
</p>

<div align="center">

[English](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md)

</div>

---

Ce projet télécharge et traite automatiquement les données des articles quotidiens de HuggingFace et les traduit en plusieurs langues en utilisant le modèle de langage InternLM. Le projet s'exécute automatiquement chaque jour pour assurer la collecte et la traduction en temps opportun des derniers articles.

## Modèle Utilisé

- **Modèle de Traduction**: [InternLM-3](https://internlm.org/)
  - Développeur: Laboratoire d'IA de Shanghai
  - Version: internlm3-latest
  - Caractéristiques:
    - Puissante capacité de traduction multilingue
    - Compréhension et traduction précises des textes académiques
    - Traduction en temps réel via API

## Fonctionnalités

- Téléchargement automatique des données d'articles quotidiens HuggingFace
- Support pour le téléchargement de données historiques à des dates spécifiques
- Utilisation de l'heure de Pékin comme fuseau horaire par défaut
- Journalisation complète des activités
- Stockage des métadonnées d'articles au format JSON
- Traduction d'articles en anglais vers plusieurs langues avec InternLM-3:
  - Japonais
  - Coréen
  - Espagnol
  - Français
- Flux de travail automatisé:
  - Téléchargement automatique quotidien des derniers articles
  - Traduction automatique multilingue
  - Mise à jour automatique du dépôt

## Installation

1. Cloner le dépôt:
```bash
git clone https://github.com/yourusername/hf-daily-paper-newsletter-multilingual.git
cd hf-daily-paper-newsletter-multilingual
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

### Exécution Manuelle

#### Télécharger les articles du jour

```bash
python download_papers.py
```

#### Télécharger les articles d'une date spécifique

```bash
python download_papers.py --date 2024-03-20
```

#### Traduire les articles

Obtenir d'abord une clé API InternLM puis exécuter:

```bash
python translate_papers.py --date 2024-03-20 --api_key your_api_key_here
```

### Exécution Automatique

Le projet est configuré avec deux workflows GitHub Actions:

1. `daily-paper-download.yml`: Téléchargement automatique des derniers articles à 9h00 heure de Pékin
2. `daily-paper-translate.yml`: Traduction automatique après le téléchargement

Pour activer la traduction automatique, il faut configurer `INTERNLM_API_KEY` dans les Secrets du dépôt.

## Stockage des Données

- Les données originales des articles en anglais sont stockées dans le répertoire `Paper_metadata_download`
- Les articles traduits sont stockés dans le répertoire `Translated_papers`, organisés par code de langue:
  - ja/: Traductions japonaises
  - ko/: Traductions coréennes
  - es/: Traductions espagnoles
  - fr/: Traductions françaises
- Tous les fichiers sont sauvegardés au format JSON avec des noms au format `YYYY-MM-DD.json`

## États de Retour

- Succès: code de sortie 0
- Erreur: code de sortie 1
- Pas de données: code de sortie 0 (avec avertissement dans le journal)

## Remerciements

- [InternLM](https://internlm.org/) - Pour fournir de puissantes capacités de traduction
- [HuggingFace](https://huggingface.co/) - Pour fournir les données d'articles quotidiens 