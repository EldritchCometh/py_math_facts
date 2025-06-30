
from dataclasses import dataclass
from operator import add, sub, mul, truediv
from itertools import product
from typing import List, Dict
from copy import deepcopy
from dataclasses import dataclass
from typing import List



@dataclass
class MathFactDC:
    equation: List[str]
    operator: str = ''
    solution: int = 0
    difficulty: int = 0
    progress: int = 0
    mastered: bool = False



class FactsMaker:


    def __init__(self):

        biggest_terms = 10
        terms = self._get_all_term_combos(biggest_terms)

        math_facts = []
        math_facts.extend(self._make_opr_probs(terms, '+'))
        math_facts.extend(self._make_opr_probs(terms, '-'))
        math_facts.extend(self._make_opr_probs(terms, '*'))
        math_facts.extend(self._make_opr_probs(terms, '/'))
        math_facts = self._insert_backward_equations(math_facts)
        math_facts = self._insert_unknowns_in_equations(math_facts)
        self._affect_final_touches(math_facts)

        self.math_facts = math_facts


    def _get_all_term_combos(self, biggest_terms):

        terms = set()
        for a, b in product(range(biggest_terms+1), repeat=2):
            terms.add((a, b))
            terms.add((b, a))
        sorted_terms = sorted(terms, key=lambda x: (min(x), max(x)))
        
        return list(sorted_terms)
    

    def _make_opr_probs(self, terms, op):
        
        opr_map = {'+': add, '-': sub, '*': mul, '/': truediv}

        pd = []
        for t1, t2 in terms:
            try:
                r = float(opr_map[op](t1, t2))
            except:
                continue
            if r < 0 or not r.is_integer():
                continue
            r = int(r)
            eq = [str(t1), op, str(t2), '=', str(r)]
            mf = MathFactDC(equation=eq, operator=op)
            pd.append(mf)

        return pd
    
    
    def _insert_backward_equations(self, math_facts):

        pd = []
        for p in math_facts:
            pd.append(p)
            pc = deepcopy(p)
            eq = pc.equation
            pc.equation = [eq[-1], '='] + eq[:3]
            pd.append(pc)
        
        return pd
    

    def _insert_unknowns_in_equations(self, math_facts):

        pd = []
        for p, i in product(math_facts, [0, 2, 4]):
            if not isinstance(p, MathFactDC):
                raise TypeError("Expected MathFactDC")
            c = deepcopy(p)
            c.solution = int(c.equation[i])
            c.equation[i] = '_'
            pd.append(c)

        return pd
    

    def _affect_final_touches(self, math_facts):

        for i, p in enumerate(math_facts):
            p.equation = tuple(p.equation)
            threshold = len(math_facts) / 99
            difficulty = int(round(i / threshold))
            p.difficulty = difficulty

