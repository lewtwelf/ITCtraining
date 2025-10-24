def longest_common_substring(string1, string2):
    substring_matches = []
    for substring_1 in substrings(string1):
        for substring_2 in substrings(string2):
            if substring_1 == substring_2:
                substring_matches.append(substring_1)
    substring_matches.sort(key=len, reverse=True)
    print(substring_matches)
    try:
        return len(substring_matches[0])
    except:
        return 0
    
def substrings(instring):
    substrings = []
    for i in range(len(instring)):
        for j in range(len(instring)):
            substrings.append(instring[i:j])
    return [i for i in substrings if i != '']

print(longest_common_substring("ABCDE", "CACAABCDABC")) # expected: ABCD --> 4
print(longest_common_substring("ABCDEF", "FBDAMNCD"))   # expected: CD --> 2
print(longest_common_substring("NDER", "AYZX"))         # expected: --> 0
print(longest_common_substring("AGGTGXTAB", "GXTXAYB"))    # expected: GXT --> 3
print(longest_common_substring("AAAAAAAB", "AAABA"))    # expected: AAAB --> 4