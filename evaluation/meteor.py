# METEOR Implementation
# Ref: https://machinetranslate.org/meteor

def compute_meteor(reference: str, hypothesis: str) -> float:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()

    if not ref_tokens or not hyp_tokens:
        return 0.0
    
    mathces = sum(1 for w in hyp_tokens if w in ref_tokens)

    precision = mathces / len(hyp_tokens)
    recall = mathces / len(ref_tokens)

    if precision+recall==0:
        return 0.0
    
    f_score = (10*precision*recall) / (recall+9*precision)

    penalty = 0.5*(1-(mathces/max(1, len(ref_tokens))))

    return f_score * (1-penalty)