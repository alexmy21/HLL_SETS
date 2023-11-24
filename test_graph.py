
import string
import networkx as nx
import random
from hll import Hll
import matplotlib.pyplot as plt

# create 12 Hll objects
hlls = [Hll(13) for _ in range(12)]
# create 12 lists with random strings
strings = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(12)]

# append strings to Hll objects
for i, hll in enumerate(hlls):
    hll._append(strings[i])

# create a directed graph with 12 nodes edge if hlls[i] and hlls[j] have non empty intersection
G_dir = nx.DiGraph()
for i in range(12):
    for j in range(12):
        if i != j and hlls[i].dependence(hlls[j]) > .5 and hlls[i].dependence(hlls[j]) > hlls[j].dependence(hlls[i]):
            G_dir.add_edge(i, j)


# create an undirected graph with 12 nodes edge if hlls[i] and hlls[j] have non empty intersection
# G_undir = nx.Graph()
# for i in range(12):
#     for j in range(12):
#         if i != j and hlls[i].tolerance(hlls[j]) > .3:
#             G_undir.add_edge(i, j)

# Save the directed graph
nx.draw(G_dir, with_labels=True)
plt.savefig('directed_graph.png')
plt.show()

# Save the undirected graph
# nx.draw(G_undir, with_labels=True)
# plt.savefig('undirected_graph.png')

# plt.show()

