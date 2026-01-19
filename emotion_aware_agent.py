import re
import time
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from Bio import Entrez
from urllib.error import HTTPError

# -----------------------------------
# CONFIG
# -----------------------------------
Entrez.email = "anassiddiqui634@gmail.com"
QUERY = "autoreactive TCR epitope specificity"
MAX_ABSTRACTS = 20

FRUSTRATION_THRESHOLD = 0.3
CURIOSITY_THRESHOLD = 0.15
RARITY_THRESHOLD = 0.8

# -----------------------------------
# DOMAIN LEXICONS
# -----------------------------------
POSITIVE_CUES = [
    "induces", "promotes", "activates", "enhances", "drives"
]

NEGATIVE_CUES = [
    "inhibits", "suppresses", "fails to", "unclear",
    "controversial", "conflicting", "inconsistent", "unknown"
]

GENES = ["tcr", "cd4", "cd8", "foxp3", "il17", "il6"]
PATHWAYS = [
    "immune tolerance",
    "autoimmunity",
    "inflammation",
    "t cell activation"
]

# -----------------------------------
# PUBMED FETCH
# -----------------------------------
def fetch_pubmed_abstracts(query, max_results=20):
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        pmids = record["IdList"]

        abstracts = []
        for pmid in pmids:
            time.sleep(0.4)
            fetch = Entrez.efetch(
                db="pubmed", id=pmid,
                rettype="abstract", retmode="text"
            )
            abstracts.append(fetch.read())

        return abstracts

    except HTTPError:
        print("⚠️ PubMed rate limit hit — using mock abstracts.")
        return load_mock_abstracts()


def load_mock_abstracts():
    return [
        "Gamma delta T cells promote IL-17 mediated inflammation.",
        "The role of gamma delta T cells in IL-17 signaling remains unclear.",
        "IL-17 production by γδ T cells is controversial.",
        "Some studies suggest γδ T cells induce immune tolerance.",
        "Other reports indicate γδ T cells fail to suppress autoimmunity.",
        "TCR signaling promotes inflammation.",
        "CD4 T cells activate immune tolerance.",
        "CD8 T cells induce inflammation.",
        "TCR involvement in immune tolerance is unclear.",
        "Foxp3 expression suppresses inflammation."
    ]

# -----------------------------------
# CLAIM-LEVEL CONTRADICTION ANALYSIS
# -----------------------------------
def analyze_claims(abstracts):
    paper_claims = []
    contradictions = []

    for i, abs in enumerate(abstracts):
        text = abs.lower()
        pos_hits = [p for p in POSITIVE_CUES if p in text]
        neg_hits = [n for n in NEGATIVE_CUES if n in text]

        if pos_hits and neg_hits:
            label = "BOTH"
        elif pos_hits:
            label = "POSITIVE"
        elif neg_hits:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        paper_claims.append({
            "paper": i,
            "label": label,
            "positive": pos_hits,
            "negative": neg_hits
        })

    # cross-paper contradiction detection
    for i in paper_claims:
        for j in paper_claims:
            if i["paper"] < j["paper"]:
                if i["label"] == "POSITIVE" and j["label"] == "NEGATIVE":
                    contradictions.append((i, j))
                if i["label"] == "NEGATIVE" and j["label"] == "POSITIVE":
                    contradictions.append((i, j))

    frustration = len(contradictions) / max(len(paper_claims), 1)
    return paper_claims, contradictions, frustration

# -----------------------------------
# TERM-LEVEL CURIOSITY (TF-IDF)
# -----------------------------------
def compute_term_curiosity(abstracts):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=100)
    tfidf = vectorizer.fit_transform(abstracts)

    scores = np.mean(tfidf.toarray(), axis=0)
    terms = vectorizer.get_feature_names_out()

    return dict(zip(terms, scores))

# -----------------------------------
# GENE–PATHWAY RARITY ANALYSIS
# -----------------------------------
def gene_pathway_rarity(abstracts):
    co_occurrence = defaultdict(int)
    total_mentions = defaultdict(int)

    for abs in abstracts:
        text = abs.lower()
        for g in GENES:
            if g in text:
                total_mentions[g] += 1
                for p in PATHWAYS:
                    if p in text:
                        co_occurrence[(g, p)] += 1

    rarity_scores = {}
    for (g, p), count in co_occurrence.items():
        rarity = 1 - (count / total_mentions[g])
        rarity_scores[(g, p)] = rarity

    return rarity_scores
