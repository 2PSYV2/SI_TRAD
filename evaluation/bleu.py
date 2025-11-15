# BLEU implementation
# Ref: https://machinetranslate.org/bleu

name = "BLEU"

from sacrebleu.metrics import BLEU

metric = BLEU(effective_order=True)

def evaluate(reference, hypothesis):
    try:
        score = metric.sentence_score(hypothesis, [reference])
        return float(score.score / 100)
    except:
        return 0.0