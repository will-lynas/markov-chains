#!/usr/bin/env python3.11
import requests

r = requests.get("https://www.gutenberg.org/cache/epub/64317/pg64317.txt")
words = r.text.split()
bad_chars = "()-.,;'\"“”‘’:?!"
good = []
for word in words:
    for c in bad_chars:
        word = word.replace(c, "")
    word = word.lower()
    if word and all(c.isalpha() for c in word):
        good.append(word)

with open("gatsby.txt", "w") as f:
    f.write(" ".join(good))
