# TER implementation

from sacrebleu.metrics import TER

name = "TER"

def evaluate(reference: str, hypothesis: str) -> float:
    try:
        metric = TER()
        score = metric.sentence_score(hypothesis, [reference])
        return float(score.score / 100)
    except:
        return 1.0