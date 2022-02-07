import random

import numpy as np

rng = np.random.default_rng()
l1 = [1,2,3,4,5,6]
l2 = ["a","b","c","d","e","f"]
num_cross = random.randint(1, len(l1)-1)
print(num_cross)
g1_a, g2_a = list(l1), list(l2)
new_gene1_a = g1_a[:num_cross] + g2_a[num_cross:]
new_gene1_b = g1_a[:num_cross] + g2_a[num_cross:]
new_gene_c = new_gene1_a[:3]
new_gene_d = new_gene1_a[3:]
new = np.array([new_gene_c, [0,0,0], new_gene_d])
print(new)

print(l1[:4]) #primeiros 4
print(l1[5:]) #remove primeiros 5
