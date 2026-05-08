def levenshtein_distance(s, t):
    """
    Calculate Levenshtein distance between two strings.
    Special cases:
        - If both are None -> raises TypeError
        - If one is None -> returns -1
        - Otherwise returns integer distance.
    """
    if s is None and t is None:
        raise TypeError("Both arguments cannot be None")
    if s is None or t is None:
        return -1

    # Convert to strings in case of other types? Spec expects strings.
    s = str(s)
    t = str(t)

    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # deletion
                                   dp[i][j - 1],      # insertion
                                   dp[i - 1][j - 1])  # substitution
    return dp[m][n]
