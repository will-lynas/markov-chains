#!/usr/bin/env python3.11
from collections import defaultdict
import random
import argparse

with open("gatsby.txt") as f:
    words = f.read().split(" ")

def check_word(word):
    if word not in words:
        raise argparse.ArgumentTypeError(f"Word {word} not in text")
    return word

parser = argparse.ArgumentParser()
parser.add_argument("--ngrams", "-n", type=int, default=2)
parser.add_argument("--length", "-l", type=int, default=20)
parser.add_argument("start_word", type=check_word)
args = parser.parse_args()

print(f"length={args.length} ngrams={args.ngrams}")

graph = defaultdict(lambda: defaultdict(float))
for i in range(len(words) - args.ngrams):
    graph[" ".join(words[i:i+args.ngrams])][words[i+args.ngrams]] += 1

# Normalise
for d in graph.values():
    total = sum(d.values())
    for k, v in d.items():
        d[k] = v/total

out = [args.start_word]
for i in range(args.length):
    consider_length = min(args.ngrams, len(out))
    choices2 = []
    for k, v in graph.items():
        partial_key = k.split(" ")[-consider_length:]
        partial_search = out[-consider_length:]
        if partial_key == partial_search:
            choices2.append(v)
    choices = random.choice(choices2)
    out.append(random.choices(list(choices.keys()), weights=list(choices.values()))[0])

generated = " ".join(out)
print(generated)
