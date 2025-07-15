
import os
import pickle
from typing import List
from pathlib import Path
from src.utils.facts_maker import MathFactDC


class UserData:


    def __init__(self, user):
        
        filter = lambda c: c.isalpha() or c.isdigit() or c == '_'
        self._user = ''.join([c for c in user if filter(c)]).lower()

        parent_dir = Path(__file__).resolve().parents[2]
        self.save_dir = Path.joinpath(parent_dir, 'app_data')
        self._user_path = Path.joinpath(self.save_dir, f'{self._user}.pkl')


    @property
    def num_facts(self) -> int:

        # fill this in later
        return 20


    @property
    def times(self) -> List[int]:

        # fill this in later
        return []


    @property
    def exclude(self) -> List[str]:

        # fill this in later
        return [0]


    def user_exists(self) -> bool:

        return os.path.exists(self._user_path)
    

    def get_facts(self) -> List[MathFactDC]:

        with open(self._user_path, 'rb') as file:
            return pickle.load(file)


    def save_data(self, data: List[MathFactDC]):

        os.makedirs(self.save_dir, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(data, f)