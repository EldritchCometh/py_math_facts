
from copy import deepcopy as copy
from itertools import product
import math
from operator import add, mul, sub, truediv
import random
from typing import Any, Dict, List, Tuple
import time



class FactsManager:


    def __init__(self, user):

        
        self._user = user
        self._mastered_threshold = self._get_mastered_threshold()
        self._all_facts: Dict[int, Dict[str, Any]] = user.data['facts']
        self._retained_facts: List[Dict[str, Any]] = self._get_retained_facts()
        self._session_facts: List[Dict[str, Any]] = self._get_session_facts()
        self._current_fact: Dict[str, Any]; self.set_next()
        self._current_equation: Tuple[str, ...]
        self._current_soltion: int
        self._answered: bool = False
        

    def _get_mastered_threshold(self) -> int:

        if not self._user.data['settings']['inc_timers']:
            return 1
        
        threshold = len(self._user.data['settings']['timers'])
        if self._user.data['settings']['inc_untimed']:
            threshold += 1
        return threshold        


    def _get_retained_facts(self):

        settings = self._user.data['settings']
        inc_nums = [k for k, v in settings['inc_nums'].items() if v]
        inc_oprs = settings['inc_oprs']

        retained_facts = []
        for v in copy(self._all_facts).values():
            if v['terms'][0] not in inc_nums:
                continue
            if v['terms'][1] not in inc_nums:
                continue
            if not inc_oprs[v['operator']]:
                continue
            v['mastered'] = v['mastery'] >= self._mastered_threshold
            retained_facts.append(v)

        return retained_facts


    def _get_session_facts(self):

        num_facts = self._user.data['settings']['num_facts']

        mastered = [p for p in self._retained_facts if p['mastered']]
        n = min(len(mastered), math.floor(num_facts * 1/3))
        session_facts = random.sample(mastered, n)

        unmastered = [p for p in self._retained_facts if not p['mastered']]
        session_facts.extend(unmastered[:num_facts-len(session_facts)])

        return session_facts


    def set_next(self):

        self._current_fact = random.choice(self._session_facts)
        self._session_facts.remove(self._current_fact)
        start_equation = list(copy(self._current_fact['equation']))
        new_equation = list(copy(self._current_fact['equation']))
        new_solution = self._current_fact['equation'][-1]

        if self._user.data['settings']['inc_ptrns']['mixed_unknowns']:
            idx = random.choices([0, 2, 4], weights=[0.25, 0.25, 0.5], k=1)[0]
            new_equation[idx] = '_'
            new_solution = start_equation[idx]

        if self._user.data['settings']['inc_ptrns']['reversed']:
            if random.choice([True, False]):
                new_equation = list(new_equation[-2:][::-1]) + new_equation[:-2]

        self._answered = False
        self._current_equation = tuple(new_equation)
        self._current_solution = int(new_solution)


    def update_mastery(self, answered_correctly: bool) -> None:

        if self._answered:
            return
        self._answered = True

        mastery = self._current_fact['mastery']
        mastery += answered_correctly
        mastery -= (not answered_correctly)
        mastery = max(0, min(mastery, self._mastered_threshold))
        
        self._current_fact['mastery'] = mastery
        if self._current_fact['mastery'] == self._mastered_threshold:
            self._current_fact['mastered'] = True
       
        self._all_facts[self._current_fact['id']]['mastery'] = mastery
        self._user.save_new_facts(self._all_facts)
  

    @property
    def percent_mastered(self) -> float:

        count = sum(1 for f in self._retained_facts if f['mastered'])
        return count / len(self._retained_facts)
        

    @property
    def equation(self) -> Tuple[str, ...]:

        return self._current_equation
    

    @property
    def solution(self) -> int:
        
        return self._current_solution


    @property
    def remaining(self) -> int:
        
        return len(self._session_facts)


    @property
    def percent_completed(self) -> float:

        num_facts = self._user.data['settings']['num_facts']
        num_completed = num_facts - (len(self._session_facts) + 1)
        return num_completed / num_facts
    

    @property
    def timer_duration(self) -> int:
        
        if not self._user.data['settings']['inc_timers']:
            return 0
        
        times = self._user.data['settings']['timers']
        if self._user.data['settings']['inc_untimed']:
            times = [0] + times  

        try:
            return times[self._current_fact['mastery']]
        except:
            return 0


    # def get_facts(self):

    #     if not hasattr(self, '_facts'):
    #         self._create_facts()

    #     self._all_facts = self._filter_by_settings(self._facts)
    #     self._retained_facts = [MathFactDC(**f) for f in self._all_facts]
    #     self._session_facts = self._get_session_facts(self._retained_facts)

    #     if not self._session_facts:
    #         raise ValueError("No facts available for the current settings.")

    #     self.set_next()
    #     return self._retained_facts





    # @property
    # def solution(self) -> int:
        
    #     return self._current_fact.solution
    

    # @property
    # def mastery(self) -> int:

    #     return self._current_fact.mastery
        

    # @property
    # def percent_completed(self) -> int:

    #     num_facts = self._ud.num_facts
    #     num_completed = num_facts - len(self._session_facts) - 1
    #     return num_completed / num_facts


    # @property
    # def percent_mastered(self) -> float:

    #     mastered = sum(1 for p in self._retained_facts if p.mastered)
    #     return mastered / len(self._retained_facts)



        




    # def set_next(self) -> None:
        
    #     self._current_fact = random.choice(self._session_facts)
    #     self._session_facts.remove(self._current_fact)
    #     self._mastery_updated_flag = False








    # def _filter_by_settings(self, all_facts):

    #     sieved = lambda p: any(x in self._ud.exclude for x in p.terms)
    #     return [p for p in all_facts if not sieved(p)]


    # def _get_all_facts(self) -> List[MathFactDC]:

    #     if self._ud.user_exists():
    #         return self._ud.get_facts()
    #     else:
    #         return FactsMaker().math_facts