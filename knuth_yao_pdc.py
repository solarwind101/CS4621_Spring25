"""
### Information and Coding Thoery: CS-4621, Spring 2025
- **Author** Suraj Sharma
- **Email**: suraj.sharma_ugt2023@ashoka.edu.in
- **Assignment 1**: Simulation of Probability distribution via Knuth-Yao approach"
# **Date**: 3rd March 2025
# Description: 
#      This code implements a simulation of a probability distribution using the Knuth-Yao approach.
#       It generates a binary tree and simulates paths through the tree 
#       to produce a sequence of symbols based on given probabilities. 
#       The code also includes Huffman coding to create an optimal prefix-free code for the symbols, and encodes the generated sequence using the Huffman codes.
"""

import numpy as np
import random
from collections import Counter

class Node:
    def __init__(self):
        self.l = None
        self.r = None

def build_t(d):
    if d == 0:
        return None
    n = Node()
    n.l = build_t(d - 1) #left child
    n.r = build_t(d - 1) #right child
    return n

def sim_path(root, k):
    return "".join(str(random.choice([0, 1])) for _ in range(k)) #random flipping of coin with 1/2 probability each

syms = [1, 2, 3, 4, 5] #symbols
probs = [1/8, 1/4, 1/8, 1/4, 1/4] #probabilities
ks = [int(np.log2(1 / p)) for p in probs]  # li's for each symbol
tree = build_t(max(ks)) 


# random sample
samps = []
for _ in range(200):
    s = random.choices(syms, weights=probs, k=1)[0] #output a symbol based on the given probabilites 
    k = ks[syms.index(s)] #get index of the output symbol
    path = sim_path(tree, k) #simulate the path
    samps.append((s, path)) #collect the symbol and path taken by them.


print("Simulated Symbols:")
for i in range (20):
    print(f"{samps[i]}") #print first 20

counts = Counter(s for s, _ in samps)
print("\nFrequency:")
for s, c in sorted(counts.items()):
    print(f"{s}: {c}")


"""
# Create Optimal prefix free code (huffman code) code for the Symbols

# Algorithm is as follows:
## Create a node for each symbol with its probability.
## Insert all nodes into a min-heap (priority queue).
## Repeat until only one node remains in the heap:
## Remove the two nodes with the smallest probabilities.
       ### Create a new node with:
       ### Probability = sum of the two removed nodes.
       #### Left child = first removed node.
       #### Right child = second removed node.
       ### Insert the new node back into the heap.
## The last remaining node is the root of the Huffman tree.
## To generate Generate Huffman codes:
        Start at the root of the tree.
            Assign "0" to the left branch and "1" to the right branch.
            Traverse the tree and record codes for each symbol.
"""

import heapq

class PF_tree:
    def __init__(self, sym, prob):
        self.sym = sym
        self.prob = prob
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.prob < other.prob

def bld_huffman_tree(prob_map):
    heap = [PF_tree(sym, prob) for sym, prob in prob_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        parent = PF_tree(None, node1.prob + node2.prob)
        parent.left, parent.right = node1, node2
        heapq.heappush(heap, parent)

    return heap[0]

def gen_codes(tree, prefix="", code_map={}):
    if tree:
        if tree.sym is not None:
            code_map[tree.sym] = prefix
        gen_codes(tree.left, prefix + "0", code_map)
        gen_codes(tree.right, prefix + "1", code_map)
    return code_map

syms = [1, 2, 3, 4, 5]
probs = [1/8, 1/4, 1/8, 1/4, 1/4]
prob_map = {syms[i]: probs[i] for i in range(len(syms))}

huffman_tree = bld_huffman_tree(prob_map)
huffman_codes = gen_codes(huffman_tree)

print("Sym : Huffman Code")
print("-------------------")
for sym in sorted(huffman_codes.keys()):
    print(f" {sym}   :   {huffman_codes[sym]}")

# Encode the string using the Huffman code
string = []
for s, _ in samps: 
    code = huffman_codes[s]  
    string.append(code)

string = "".join(string)  

print("Encoded Huffman String:", string)

"""
## References:
- GeeksforGeeks. (n.d.). Huffman coding in Python. GeeksforGeeks. Retrieved March 3, 2025, from https://www.geeksforgeeks.org/huffman-coding-in-python/

- Programiz. (n.d.). Huffman coding algorithm. Programiz. Retrieved March 3, 2025, from https://www.programiz.com/dsa/huffman-coding"
"""
