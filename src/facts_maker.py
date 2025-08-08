
from copy import deepcopy as copy
from operator import add, mul, sub, truediv
from typing import Dict



class FactsMaker():


    def __init__(self):

        self._facts = []
        terms = [(k, i) for k in range(13) for i in range(k + 1)]
        
        self._append_addition_facts(terms)
        self._append_subtraction_facts(terms)
        self._append_multiplication_facts(terms)
        self._append_division_facts(terms)
        
        self._dict = {i: {**v, 'id': i} for i, v in enumerate(self._facts)}


    def _append_addition_facts(self, terms):

        for (t1, t2) in terms:
            r = add(t1, t2)
            eq = (str(t1), '+', str(t2), '=', str(int(r)))
            self._facts.append({
                'equation': eq,
                'terms': [t1, t2],
                'operator': 'add',
                'mastery': 0 })


    def _append_subtraction_facts(self, terms):

        for (t1, t2) in terms:
            r = sub(t1, t2)
            eq = (str(t1), '-', str(t2), '=', str(int(r)))
            self._facts.append({
                'equation': eq,
                'terms': [t1, t2],
                'operator': 'sub',
                'mastery': 0 })
            
    
    def _append_multiplication_facts(self, terms):

        for (t1, t2) in terms:
            r = mul(t1, t2)
            eq = (str(t1), '*', str(t2), '=', str(int(r)))
            self._facts.append({
                'equation': eq,
                'terms': [t1, t2],
                'operator': 'mul',
                'mastery': 0 })


    def _append_division_facts(self, terms):
        
        for (t1, t2) in terms:
            if t2 == 0:
                continue
            r = truediv(t1, t2)
            if not r.is_integer():
                continue
            eq = (str(t1), '/', str(t2), '=', str(int(r)))
            self._facts.append({
                'equation': eq,
                'terms': [t1, t2],
                'operator': 'div',
                'mastery': 0})


    def get_facts(self) -> Dict[int, Dict]:

        return copy(self._dict)


# for i, mf in enumerate(self._facts):
#     threshold = len(self._facts) / 99
#     difficulty = int(round(i / threshold))
#     mf['difficulty'] = difficulty
#     mf['mastery'] = 0
#     mf['mastered'] = False
