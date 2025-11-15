name = "chrF"

from sacrebleu.metrics import CHRF

metric = CHRF(word_order=2)   # chrF++

def evaluate(reference, hypothesis):
    try:
        score = metric.sentence_score(hypothesis, [reference])
        return float(score.score / 100)  # normalize to 0–1
    except Exception:
        return 0.0
