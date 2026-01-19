# Emotion-Aware Agent for Detecting Contradictions in Autoreactive TCR Literature

This repository provides a lightweight, explainable Python agent that analyzes
PubMed abstracts related to autoreactive T-cell receptor (TCR) epitope specificity.
The agent detects cross-paper contradictions, novelty signals, and rare gene–pathway
associations using domain-informed lexical cues and TF-IDF statistics.

## 🔬 Scientific Motivation
Conflicting findings are common in immunology literature, particularly in autoimmunity
and TCR epitope specificity. This tool demonstrates how an automated agent can:
- Detect contradictory claims across papers
- Estimate "frustration" due to conflicting evidence
- Highlight underexplored gene–pathway associations

## ⚙️ Features
- PubMed abstract retrieval via Entrez
- Claim polarity detection (positive / negative / neutral / both)
- Cross-paper contradiction analysis
- Term-level novelty detection using TF-IDF
- Gene–pathway rarity analysis

## 🧠 Agent Outputs
- Frustration score based on contradiction density
- List of contradictory paper pairs
- High-curiosity terms
- Rare gene–pathway co-occurrences

## 📁 Repository Structure
EmotionAware_Tcell/
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│ └── emotion_aware_agent.py
└── results/
├── sample_output.txt
└── fetched_papers_summary.txt
## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
### 2. Run the agent
python src/emotion_aware_agent.py
⚠️ Notes

PubMed rate limits may trigger fallback to mock abstracts

This repository is intended as a proof-of-concept and methodological demonstration

📜 License

This project is released under the MIT License.
