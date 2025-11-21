import os, re, sys

root = '/Users/ninaherrmann/Research/toad/experiments/results/valtest'
seed_dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and 'seed' in d.lower()]
if not seed_dirs:
    print("Keine seed*-Ordner gefunden.")
    sys.exit(0)

counts = {}
for sd in seed_dirs:
    subdirs = [name for name in os.listdir(root + '/' + sd) if os.path.isdir(os.path.join(root + '/' + sd, name))]
    for name in subdirs:
        counts[name] = counts.get(name, 0) + 1

if not counts:
    print("Keine Dataset-Ordner in den seed*-Ordnern gefunden.")
    sys.exit(0)

total = len(seed_dirs)
print(counts)
for name, c in counts.items():
    print(f"{name}\t{c}/{total}")
