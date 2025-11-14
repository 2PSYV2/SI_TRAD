# BLEU implementation
# Ref: https://machinetranslate.org/bleu

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def compute_bleu(reference: str, hypothesis: str) -> float:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()

    smoothie = SmoothingFunction().method4 # method 4 works better for phrase convertions
    # TODO Expose the method so the user could edit it

    try:
        return sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)
    except:
        return 0.0