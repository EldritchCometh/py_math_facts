
import os
import math
import pickle
import random
from typing import List
from src.facts_maker import FactsMaker, MathFactDC


class MathFacts:


    def __init__(self, settings):

        self._settings = settings
        self._user = settings['user']
        self._num_facts = settings['num_probs']

        filter = lambda c: c.isalpha() or c.isdigit() or c == '_'
        self._user = ''.join([c for c in self._user if filter(c)]).lower()

        parent_directory = os.path.dirname(os.path.abspath(__file__))
        self._data_path = os.path.join(parent_directory, '../app_data')
        self._user_path = os.path.join(self._data_path, f'{self._user}.pkl')

        self._all_facts: List[MathFactDC] = self._load_data()
        self._retained_facts: List[MathFactDC] = self._get_retained_facts()
        self._session_facts: List[MathFactDC] = self._get_session_facts()
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
        
        num_completed = self._num_facts - len(self._session_facts) - 1
        return num_completed / self._num_facts


    @property
    def percent_mastered(self) -> float:

        mastered = sum(1 for p in self._retained_facts if p.mastered)
        return mastered / len(self._retained_facts)


    @property
    def timer_duration(self) -> int:
        
        try:
            times = [0] + self._settings['times']
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

        threshold = 1 + len(self._settings['times'])

        mastery = self._current_fact.mastery
        mastery += answered_correctly
        mastery -= (not answered_correctly)
        mastery = max(0, min(threshold, mastery))
        
        self._current_fact.mastery = mastery
        self._current_fact.mastered = (mastery == threshold)
        
        self._mastery_updated_flag = True
        self._save_data()


    def _get_session_facts(self) -> List[MathFactDC]:

        mastered = [p for p in self._retained_facts if p.mastered]
        n = min(len(mastered), math.floor(self._num_facts * 1/3))
        session_facts = random.sample(mastered, n)

        unmastered = [p for p in self._retained_facts if not p.mastered]
        unmastered.sort(key=lambda p: p.difficulty)
        session_facts.extend(unmastered[:self._num_facts-len(session_facts)])

        return session_facts


    def _get_retained_facts(self) -> List[MathFactDC]:
    
        sieved = lambda p: any(x in self._settings['exclude'] for x in p.terms)
        return [p for p in self._all_facts if not sieved(p)]


    def _load_data(self) -> List[MathFactDC]:
        
        if not os.path.exists(self._user_path):
            return FactsMaker().math_facts
        
        with open(self._user_path, 'rb') as file:
            return pickle.load(file)


    def _save_data(self) -> None:

        os.makedirs(self._data_path, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(self._all_facts, f)


