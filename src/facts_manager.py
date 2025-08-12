
import random
from copy import copy
from typing import Any, Dict, List, Tuple



class FactsManager:


    def __init__(self, app):

        self._app = app
        self._user = app.user

        self._all_facts: Dict[int, Dict[str, Any]]
        self._retained: List[Dict[str, Any]]
        self._mastered_threshold: int
        self._mastered: List[Dict[str, Any]]
        self._unmastered: List[Dict[str, Any]]
        self._answered: bool
        self._questions_answered: int = 0
        self._current_fact: Dict[str, Any]
        self._current_equation: Tuple[str, ...]
        self._current_solution: int
        self._current_working_list: List[Dict[str, Any]]

        self._set_all_facts()
        self._set_retained_facts()
        self._set_mastered_and_unmastered_facts()
        self.set_next()


    def _set_all_facts(self) -> None:

        self._all_facts = self._user.facts


    def _set_retained_facts(self) -> None:

        inc_nums = [k for k, v in self._user.inc_nums.items() if v]

        self._retained = []
        for v in copy(self._all_facts).values():
            if v['terms'][0] not in inc_nums:
                continue
            if v['terms'][1] not in inc_nums:
                continue
            if not self._user.inc_oprs[v['operator']]:
                continue
            self._retained.append(v)


    def _set_mastered_and_unmastered_facts(self) -> None:
        
        self._mastered = \
            [f for f in self._retained if self._is_mastered(f)]
        self._unmastered = \
            [f for f in self._retained if not self._is_mastered(f)]


    def set_next(self) -> None:

        if not self._unmastered:
            self._app._on_all_facts_mastered()
            return

        ratio = min(len(self._mastered) / len(self._unmastered), (1/3))
        if random.choices([True, False], weights=[ratio, 1], k=1)[0]:
            current_working_list = self._mastered
            next_fact = copy(random.choice(current_working_list))
        else:
            current_working_list = self._unmastered
            next_fact = copy(random.choice(current_working_list[:20]))

        equation = list(next_fact['equation'])
        new_equation = list(next_fact['equation'])
        new_solution = int(next_fact['equation'][-1])

        if self._user.inc_ptrns['mixed_unknowns']:
            idx = random.choices([0, 2, 4], weights=[0.25, 0.25, 0.5], k=1)[0]
            new_equation[idx] = '_'
            new_solution = int(equation[idx])

        if self._user.inc_ptrns['reversed']:
            if random.choice([True, False]):
                new_equation = list(new_equation[-2:][::-1]) + new_equation[:-2]

        self._answered = False
        self._current_fact = next_fact
        self._current_equation = tuple(new_equation)
        self._current_solution = new_solution
        self._current_working_list = current_working_list


    def process_submission(self, is_correct: bool) -> None:

        if not self._answered:
            self._answered = True
            self._questions_answered += 1
            self._update_mastery(is_correct)
         

    def _update_mastery(self, is_correct: bool) -> None:

        mastery = self._current_fact['mastery']
        mastery += is_correct
        mastery -= (not is_correct)
        mastery = max(0, min(mastery, self._mastered_threshold))

        self._user.facts[self._current_fact['id']]['mastery'] = mastery
        self._user.save_user_data()

        if self._is_mastered(self._current_fact):
            if self._current_working_list == self._unmastered:
                self._current_working_list.remove(self._current_fact)
                self._mastered.append(self._current_fact)
        if not self._is_mastered(self._current_fact):
            if self._current_working_list == self._mastered:
                self._current_working_list.remove(self._current_fact)
                self._unmastered.insert(0, self._current_fact)


    def _is_mastered(self, fact: Dict[str, Any]) -> bool:

        if hasattr(self, '_mastered_threshold'):
            return fact['mastery'] >= self._mastered_threshold
        
        if not self._user.inc_timers:
            self._mastered_threshold = 1
        else:                
            threshold = len(self._user.timer_vals)
            if self._user.inc_untimed:
                threshold += 1
            self._mastered_threshold = threshold
        return fact['mastery'] >= self._mastered_threshold


    @property
    def equation(self) -> Tuple[str, ...]:

        return self._current_equation
    

    @property
    def solution(self) -> int:
        
        return self._current_solution


    @property
    def percent_completed(self) -> float:

        return self._questions_answered / self._user.num_facts


    @property
    def percent_mastered(self) -> float:

        return len(self._mastered) / len(self._retained)
        

    @property
    def timer_duration(self) -> int:
        
        if not self._user.inc_timers:
            return 0
        
        times = self._user.timer_vals
        if self._user.inc_untimed:
            times = [0] + times  

        try:
            return times[self._current_fact['mastery']]
        except:
            return 0
