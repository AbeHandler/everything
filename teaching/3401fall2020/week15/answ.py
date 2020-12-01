from ptb import TreebankWordTokenizer

your_doc_name = "doc1.txt"

with open(your_doc_name, "r") as inf:
    txt = inf.read()
tokr = TreebankWordTokenizer()
print(txt)
V = set(tokr.tokenize(txt))


print(your_doc_name, len(V))
