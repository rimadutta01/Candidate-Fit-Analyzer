"""
Fast numeric baseline: cosine similarity between CV and JD embeddings.
This runs locally (no API call) and gives an instant score while the
Azure OpenAI call (slower, richer) is also running.
"""

from functools import lru_cache
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def _get_model():
    # Loaded once and cached — avoids reloading the model on every rerun.
    # 'all-MiniLM-L6-v2' is small and fast, good enough for this similarity task.
    return SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity_score(cv_text: str, jd_text: str) -> float:
    """
    Returns a similarity score between 0 and 100.
    """
    model = _get_model()
    embeddings = model.encode([cv_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 2)