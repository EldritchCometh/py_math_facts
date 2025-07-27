
import math
import random
from typing import List

from src.facts_maker import MathFactDC, FactsMaker
from src.user_manager import UserManager




class MathFacts:


    def __init__(self, settings):

        self._ud = UserData(settings['user'])

        self._all_facts: List[MathFactDC] = self._get_all_facts()
        self._retained_facts = self._filter_by_settings(self._all_facts)
        self._session_facts = self._get_session_facts(self._retained_facts)
        self._current_fact: MathFactDC; self.set_next()

        self._mastery_updated_flag = False


    @property
    def equation(self) -> List[str]:

        return self._current_fact.equation


    @property
    def solution(self) -> int:
        
        return self._current_fact.solution
    

    @property
    def mastery(self) -> int:

        return self._current_fact.mastery
        

    @property
    def percent_completed(self) -> int:

        num_facts = self._ud.num_facts
        num_completed = num_facts - len(self._session_facts) - 1
        return num_completed / num_facts


    @property
    def percent_mastered(self) -> float:

        mastered = sum(1 for p in self._retained_facts if p.mastered)
        return mastered / len(self._retained_facts)


    @property
    def timer_duration(self) -> int:
        
        try:
            times = [0] + self._ud.times
            return times[self.mastery]
        except:
            return 0
        

    @property
    def remaining(self) -> int:
        
        return len(self._session_facts)


    def set_next(self) -> None:
        
        self._current_fact = random.choice(self._session_facts)
        self._session_facts.remove(self._current_fact)
        self._mastery_updated_flag = False


    def update_mastery(self, answered_correctly: bool) -> None:

        if self._mastery_updated_flag:
            return

        threshold = 1 + len(self._ud.times)

        mastery = self._current_fact.mastery
        mastery += answered_correctly
        mastery -= (not answered_correctly)
        mastery = max(0, min(threshold, mastery))
        
        self._current_fact.mastery = mastery
        self._current_fact.mastered = (mastery == threshold)
        
        self._mastery_updated_flag = True
        self._ud.save_data(self._all_facts, )


    def _get_session_facts(self, retained_facts) -> List[MathFactDC]:

        num_facts = self._ud.num_facts

        mastered = [p for p in retained_facts if p.mastered]
        n = min(len(mastered), math.floor(num_facts * 1/3))
        session_facts = random.sample(mastered, n)

        unmastered = [p for p in retained_facts if not p.mastered]
        unmastered.sort(key=lambda p: p.difficulty)
        session_facts.extend(unmastered[:num_facts-len(session_facts)])

        return session_facts


    def _filter_by_settings(self, all_facts):

        sieved = lambda p: any(x in self._ud.exclude for x in p.terms)
        return [p for p in all_facts if not sieved(p)]


    def _get_all_facts(self) -> List[MathFactDC]:

        if self._ud.user_exists():
            return self._ud.get_facts()
        else:
            return FactsMaker().math_facts