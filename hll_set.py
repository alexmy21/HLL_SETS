from hll import Hll
from scipy.spatial import distance

class HllSet:
    # card = 0
    def __init__(self, data, _children=(), _op='init', label=''):
        # super().__init__(data, _children, _op)
        self.data = data
        self.card = self.data.card
        self.delta = self._delta(Hll(data.ex), data)
        self.grad = self._grad((0, 0, 0), self.delta)
        # self.forward = lambda:None
        self._prev = set(_children)
        self.label = label
        self._op = _op
        
        self.card = data.card
    
    def __add__(self, other):
        return self.union(other)
    
    def __mul__(self, other):
        return self.intersect(other)
    
    def __eq__(self, other):
        return self.equal(other)
     
    def __repr__(self):
        return f"HllSet(card: {self.data.card}, op: {self._op}, label: {self.label})"
    
    #===========================================================================
    # Operators
    #===========================================================================      
    def union(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        
        out = Hll(self.data.ex).union(self.data).union(other.data)
        # print('union out card: ', out.card)
        label = f'({self.label})_U_({other.label})' 
        
        ret = HllSet(out, _children = (self.label, other.label), _op='+', label=label)
        
        return ret
    
    def intersect(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        
        out = Hll(self.data.ex).union(self.data).intersect(other.data)
        
        label = f'({self.label})_&_({other.label})' 
        
        ret = HllSet(out, _children = (self.label, other.label), _op='*', label=label)
        
        return ret
    
    def equal(self, other) -> bool:
        return self.data.equal(other.data)
    
    def dependence(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        return self.data.dependence(other.data)
        
    def tolerance(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        return self.data.tolerance(other.data)  

    def _append(self, strings):
        Y = Hll(self.data.ex, strings=strings)
        Y_set = HllSet(Y)
        U = self.union(Y_set)
        
        self.delta = self._delta(self.data, U.data)  
        self.grad = self._grad(self.delta, U.delta)
        self.data = U.data
        self.card = self.data.card
        # print('self appended: ', self.card, self.delta, self.grad)

        return self

    def update(self, strings):
        Y = Hll(self.data.ex, strings=strings)
        Y_set = HllSet(Y)
        
        self.delta = self._delta(self.data, Y_set.data)  
        self.grad = self._grad(self.delta, Y_set.delta)
        self.data = Y_set.data
        self.card = self.data.card
        # print('self updated: ', self.card, self.delta, self.grad)

        return self
    
    def _delta(self, hll1, hll2):
        X = hll1.union(hll2)
        D = X.card - hll2.card 
        R_card = hll1.card + hll2.card - X.card
        R = R_card if R_card > 0 else 0
        N = X.card - hll1.card  

        return [D, R, N]

    def _grad(self, v1, v2):
        # Difference between the two vectors
        return  distance.euclidean(v1, v2)
    