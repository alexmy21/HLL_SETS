from HLL import HyperLogLog

class Hll(HyperLogLog):
    def __init__(self, ex = 13, strings = None):
        super().__init__(ex)
        self.ex = ex
        self.card = 0
        if strings is not None:
            for s in strings:
                self.add(bytes(s, 'utf-8'))
            self.card = round(self.cardinality())
        

    def _append(self, strings):
        for s in strings:
            try:
                self.add(bytes(s, 'utf-8'))
            except:
                print(f"Failed to add {bytes(s, 'utf-8')}")
            
        self.card = round(self.cardinality())

    def update(self, strings):
        self.registers = [0] * self.size()
        for s in strings:
            try:
                self.add(bytes(s, 'utf-8'))
            except:
                print(f"Failed to add {bytes(s, 'utf-8')}")
            
        self.card = round(self.cardinality())
        
    def union(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        
        out = Hll(self.ex)
        for i in range(self.size() - 1):
            val1 = self.registers()[i]
            val2 = other.registers()[i]            
            out.set_register(i, max(val1, val2))
        out.card = round(out.cardinality())

        return out
    
    def intersect(self, other):
        if other is None and self.ex != other.ex:
            raise ValueError('Exponents do not match.')
        
        out = Hll(self.ex)
        for i in range(self.size() - 1):
            val1 = self.registers()[i]
            val2 = other.registers()[i]            
            out.set_register(i, min(val1, val2))
        out.card = (self.card + other.card) - (self.union(other).card) 
        return out
    
    
    def equal(self, other) -> bool:
        return all(self.registers()[i] == other.registers()[i] for i in range(self.size() - 1))
        
    def dependence(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        return (
            (self.intersect(other)).card / self.card
        )
        
    def tolerance(self, other):
        if other is None and self.data.ex != other.data.ex:
            raise ValueError('Exponents do not match.')
        return (
            (self.intersect(other)).card / self.union(other).card
        )
        
class ZHll(Hll):
    def __init__(self, ex = 13):
        super().__init__(ex)
        self.ex = ex
        self.registers = [0] * self.size()
        self.delta = (0, 0, 0)
        self.grad = 0
        self.card = 0
