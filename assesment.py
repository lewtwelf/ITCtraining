"""Total number of unique words(case sensitive) in 
a given input sentence. Example: input: "netflix fb apple facebook apple', output: 4"""

sen = "netflix fb apple facebook apple"

def countUniqueWords(inSTring):
    words = inSTring.split()
    return set(words)

print(countUniqueWords(sen))