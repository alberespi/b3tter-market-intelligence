# 🌿 B3tter Market Intelligence
### A Data-Driven Sentiment & Competitive Analysis of the Healthy Snack Market in Spain

> **Disclaimer:** This is an independent, unsolicited project. I have no affiliation with B3tter. All data used is publicly available.

---

## 📌 Motivation

B3tter is one of the most interesting healthy food brands in the Spanish market — not just because of their products, but because of how they've built their brand around a lifestyle and a community. As a data scientist and ML engineer with a strong interest in health, nutrition, and endurance sports, I wanted to go beyond applying to companies with a CV and instead **show what I can do with their own data**.

This project applies NLP, sentiment analysis, and topic modeling to publicly available customer reviews to answer concrete business questions about B3tter's product perception, competitive positioning, and brand differentiation.

---

## 🎯 Business Hypotheses

The analysis is structured around six hypotheses:

| # | Hypothesis |
|---|-----------|
| H1 | Flavor is the primary satisfaction driver for granolas; satiety for bars; Nutella comparison for the cocoa cream |
| H2 | Negative reviews concentrate on price and quantity per pack, not product quality |
| H3 | B3tter customers mention lifestyle attributes (health, sport, clean ingredients) more than competitors' customers, who focus on macros |
| H4 | B3tter has higher average sentiment than Paleobull and Nakd but lower review volume, suggesting a consolidated but less-penetrated brand |
| H5 | Bundle and pack reviews have higher average ratings than individual products, indicating the bundle format drives loyalty |
| H6 | B3tter has a higher proportion of reviews and mentions referencing community and lifestyle vs pure product, consistent with a founder-led content marketing strategy |

---

## 🗂️ Project Structure

```
b3tter-market-intelligence/
│
├── README.md
│
├── data/
│   ├── raw/          # No incluido en git — ejecutar src/scraper_yotpo.py para regenerar
│   └── processed/    # No incluido en git — generado por los notebooks de preprocessing
│
├── notebooks/
│   ├── 01_data_collection.ipynb    # Scraping pipeline (Amazon, Trustpilot)
│   ├── 02_preprocessing.ipynb      # Text cleaning, normalization
│   ├── 03_sentiment_analysis.ipynb # Sentiment models, benchmarking
│   └── 04_topic_modeling.ipynb     # BERTopic, cluster analysis, visualization
│
├── src/
│   ├── scraper.py                  # Playwright-based Amazon scraper
│   ├── preprocessing.py            # Text cleaning utilities
│   ├── sentiment.py                # Sentiment inference pipeline
│   └── topic_model.py              # BERTopic training and visualization
│
├── reports/
│   └── executive_summary.pdf       # Final report — business language, no jargon
│
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Tech Stack

| Area | Tools |
|------|-------|
| Data Collection | `Playwright`, `BeautifulSoup`, `pandas` |
| NLP Preprocessing | `spaCy` (es_core_news_lg), `nltk`, `emoji` |
| Sentiment Analysis | `pysentimiento`, `HuggingFace Transformers` (RoBERTa-BNE) |
| Topic Modeling | `BERTopic`, `sentence-transformers` (paraphrase-multilingual-MiniLM-L12-v2) |
| Visualization | `Plotly`, `WordCloud`, `matplotlib` |
| Reporting | `Jupyter`, `nbconvert`, custom PDF |

---

## 📦 Products Analyzed

**B3tter:**
- Granola Natural / Granola Cacao
- Barritas: Cacahuete, Arándanos, Cacao, Coco
- Crema de Cacao y Avellana
- Bundles & Packs

**Competitors:**
- Nakd, Paleobull, You Snacks, Brave, Foodspring, Rude Health, Nutwork

---

## 📊 Deliverables

- [ ] **Notebook 01** — Scraping pipeline functional and documented
- [ ] **Notebook 02** — Clean, processed dataset
- [ ] **Notebook 03** — Sentiment analysis results with model comparison
- [ ] **Notebook 04** — Topic clusters, heatmaps, and cross-analysis
- [ ] **Executive Summary PDF** — Business-ready report for B3tter

---

## 🗓️ Timeline

| Week | Deliverable |
|------|------------|
| 1 | Repo setup, hypothesis definition, environment |
| 2–3 | Data collection (scraping pipeline) |
| 4 | Preprocessing + sentiment analysis |
| 5–6 | Topic modeling + visualizations |
| 7 | Executive report + final repo polish |

---

## 📬 About

Built by **Alberto Espinosa** — Junior AI Researcher & ML Engineer.

- 🔗 [LinkedIn](https://linkedin.com/in/alberto-espinosa-perez)
- 📸 [Instagram @albertoespi\_](https://instagram.com/albertoespi__)
- 💻 [GitHub](https://github.com/alberespi)

*Documenting the full process publicly — technical posts on LinkedIn, behind-the-scenes on Instagram.*
