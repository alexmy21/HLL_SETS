import itertools
from hll import Hll
from hll_set import HllSet
import random
import string
import torch

import matplotlib.pyplot as plt

random.seed(42)
strings = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(200000)]
print('Initial dataset size: ', len(strings))

set_A = set(random.sample(strings, 28000))
set_B = set(random.sample(strings, 100000))
set_C = set(random.sample(strings, 122000))

hll_A = Hll(13)
hll_A._append(set_A)

hll_B = Hll(13)
hll_B._append(set_B)

hll_C = Hll(13)
hll_C._append(set_C)

print('\n===== HLL operations =====')
print('Hll A: ', hll_A.card)
print('Hll B: ', hll_B.card)
print('Hll C: ', hll_C.card)
print()
print('Hll A union B: ', hll_A.union(hll_B).card)
print('Hll A intersect B: ', hll_A.intersect(hll_B).card)

print('\n===== HLL Sets measurement functions =====')
print('\nDependence is asymmetrical, non commutative function:')
print('Hll A dependence B: ', hll_A.dependence(hll_B))
print('Hll B dependence A: ', hll_B.dependence(hll_A))
print('Hll A dependence A: ', hll_A.dependence(hll_A))
print('\nTolerance is symmetrical, commutative function:')
print('Hll A tolerance B: ', hll_A.tolerance(hll_B))
print('Hll B tolerance A: ', hll_B.tolerance(hll_A))
print('Hll A tolerance A: ', hll_A.tolerance(hll_A))

print('\n===== Testing Hll Sets =====')
A = HllSet(hll_A, label='A')
print('HllSet A: ', A, A.card, A.delta, A.grad, )

B = HllSet(hll_B, label='B')
print('HllSet B: ', B, B.card, B.delta, B.grad)

C = HllSet(hll_C, label='C')
print('HllSet C: ', C, C.card, C.delta, C.grad)

# Local universe as a union of all available sets
U = A + B + C
print('HllSet U: ', U, )

# Empty set
Z = HllSet(Hll(13), label='Z') 
print('HllSet Z: ', Z, ) 

print('\n===== Hll Sets Fundamental properties =====')
Xab = A * B
Xbc = B * C
X = Xab + Xbc
print('\nX, Xab, Xbc, C: ', X.card, Xab.card, Xbc.card, C.card)
print('\nCommutative property:')
print('(A + B) == (B + A)', (A + B) == (B + A), (A + B).card, (A + B).delta, (A + B).grad)
print('(A * B) == (B * A)', (A * B) == (B * A), (A * B).card, (A * B).delta, (A * B).grad)

print('\nAssociative property')
print('(A * B) + B == B', (A * B) + B == B, ((A * B) + B).card, ((A * B) + B).delta, ((A * B) + B).grad)
print('(A + B) * B == B', (A + B) * B == B, ((A + B) * B).card, ((A + B) * B).delta, ((A + B) * B).grad)

print('\nDistributive property:')
print('((A + B) + C) == (A + (B + C))', (A + B) + C == A + (B + C), (A + B + C).card)
print('((A * B) * C) == (A * (B * C))', (A * B) * C == A * (B * C), (A * B * C).card)

print('\n((A + B) * C) == (A * C) + (B * C)', ((A + B) * C) == (A * C) + (B * C), ((A + B) * C).card)
print('((A * B) + C) == (A + C) * (B + C)', ((A * B) + C) == (A + C) * (B + C), ((A * B) + C).card)

print('\nIdentity:')
print('(A + Z) == A', (A + Z) == A, (A + Z).card)
print('(A * U) == A', (A * U) == A, (A * U).card)

print('\nIdempotent laws:')
print('(A + A) == A', (A + A) == A, (A + A).card)
print('(A * U) == A', (A * U) == A, (A * U).card)