# -*- coding: utf-8 -*-

# Load up treasury tags
TreasuryTagMap = {}
for w in open('categories/treasury.txt', 'r').readlines():
    k, t = w.strip().split('\t')
    TreasuryTagMap[k] = t
