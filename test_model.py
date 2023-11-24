import random
import string
import torch
import torch.optim as optim
import torch.nn as nn
from collections import OrderedDict
from hll_model import HllModel
from hll_set import HllSet
from hll import Hll

from matplotlib import pyplot as plt 

# dset = [0.5,  14.0, 15.0, 28.0, 11.0,  8.0,  3.0, -4.0,  6.0, 13.0, 21.0]
# hll = [35.7, 55.9, 58.2, 81.9, 56.3, 48.9, 33.9, 21.8, 48.4, 60.4, 68.4]

strings = [''.join(random.choices(string.ascii_uppercase, k=10)) for _ in range(200000)]
print('Initial dataset size: ', len(strings))

# Generate n subsets from the initial dataset of strings. Subsets may have not empty intersection
def generate_subsets(strings, n, m, k):
    return [
        set(random.sample(strings, random.randint(m,k)))
        for _ in range(n)
    ]

# Convert a list of subsets to a list of HllSet objects and return set.card and hll.card
def sets_to_hllsets(sets):
    hll_sets = []
    set_card = []
    hll_card = []
    for i, s in enumerate(sets):
        hll = Hll(13)
        hll._append(s)
        # hll_sets.append(HllSet(hll, label=f'{i}'))
        set_card.append(len(s))
        hll_card.append(hll.card)
        
        # print(f'{i} set size: {len(s)}, hll size: {hll.card}')
        
    return set_card, hll_card

sets = generate_subsets(strings, 100, 10, 200000)
dset, hll = sets_to_hllsets(sets)

hll = torch.tensor(list(hll)).unsqueeze(1) 
dset = torch.tensor(list(dset)).unsqueeze(1)

neuron_count = 20
n_model = nn.Sequential(OrderedDict([
    ('hidden_linear', nn.Linear(1, neuron_count)),
    ('hidden_activation', nn.LeakyReLU()),
    ('output_linear', nn.Linear(neuron_count, 1))
]))

optimizer = optim.Adadelta(n_model.parameters(), lr=0.2)  

model = HllModel(hll, dset, 0.01)
model.training_loop(
    n_epochs = 50000,
    optimizer = optimizer,
    model = n_model,
    loss_fn = nn.MSELoss(),
    x_train = model.dsetn_train,
    x_val = model.dsetn_val,
    y_train = model.hll_train,
    y_val = model.hll_val
)

t_range = torch.arange(0., 200000.).unsqueeze(1)

fig = plt.figure(dpi=150)
plt.xlabel("dataset")
plt.ylabel("hll")
plt.plot(dset.numpy(), hll.numpy(), 'o')
plt.plot(t_range.numpy(), n_model(0.01 * t_range).detach().numpy(), 'c-')
plt.plot(dset.numpy(), n_model(0.01 * dset).detach().numpy(), 'kx')

plt.show()