
from operator import add, sub, mul, truediv
from itertools import product
from typing import List, Dict, Any
from copy import deepcopy



class FactsMaker:


    def __init__(self):

        math_facts = []
        terms = self._get_all_term_combos()
        math_facts.extend(self._make_opr_facts(terms, '+'))
        math_facts.extend(self._make_opr_facts(terms, '-'))
        math_facts.extend(self._make_opr_facts(terms, '*'))
        math_facts.extend(self._make_opr_facts(terms, '/'))
        math_facts = self._insert_backward_equations(math_facts)
        math_facts = self._insert_unknowns_in_equations(math_facts)
        math_facts = self._affect_final_touches(math_facts)

        self.math_facts = math_facts


    def _get_all_term_combos(self):

        terms = set()
        for a, b in product(range(13), repeat=2):
            terms.add((a, b))
            terms.add((b, a))
        terms = sorted(terms, key=lambda x: (min(x), max(x)))
        
        return list(terms)
    

    def _make_opr_facts(self, terms, op):

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
            math_fact = {
                'equation': eq,
                'terms': [t1, t2],
                'operator': op }
            pd.append(math_fact)

        return pd
    
    
    def _insert_backward_equations(self, math_facts: List[Dict[str, Any]]):

        mfs = []
        for mf in math_facts:
            mfs.append(mf)
            eq = mf['equation']
            mfc = deepcopy(mf)
            mfc['equation'] = [eq[-1], '='] + eq[:3]
            mfs.append(mfc)
        
        return mfs
    

    def _insert_unknowns_in_equations(self, math_facts: List[Dict[str, Any]]):
        
        mfs = []
        for mf, i in product(math_facts, [0, 2, 4]):
            mfc = deepcopy(mf)
            solution = mfc['equation'][i]
            mfc['equation'][i] = '_'
            mfc['solution'] = solution
            mfs.append(mfc)

        return mfs
    

    def _affect_final_touches(self, math_facts: List[Dict[str, Any]]):

        mfs = []
        for i, mf in enumerate(math_facts):
            mf['equation'] = tuple(mf['equation'])
            threshold = len(math_facts) / 99
            difficulty = int(round(i / threshold))
            mf['difficulty'] = difficulty
            mfs.append(mf)

        return mfs
