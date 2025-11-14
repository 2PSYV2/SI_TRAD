# ROUGE-L Implementation:
# Ref: https://en.wikipedia.org/wiki/ROUGE_(metric)

def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]

def compute_togue_l(reference: str, hypothesis: str) -> float:
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()

    lcs_len = lcs(ref_tokens, hyp_tokens)

    if len(ref_tokens) == 0 or len(hyp_tokens) == 0:
        return 0.0
    
    precision = lcs_len / len(hyp_tokens)
    recall = lcs_len / len(ref_tokens)

    if precision+recall==0:
        return 0.0
    
    return (2*precision*recall)/(precision+recall)