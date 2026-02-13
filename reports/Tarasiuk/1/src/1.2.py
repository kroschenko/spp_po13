class Solution:
    def longestCommonPrefix(strs):
        word = ""
        min_word = min(strs)
        for i in enumerate(min_word):
            for j in enumerate(strs):
                if min_word[i] == strs[j][i]:
                    continue
                return word
            word += min_word[i]
        return word
    