#!/bin/bash

for d in */; do
printf "%s: " "${d%/}"
find "$d" -type f | wc -l
done
