
import os
import pickle
from pathlib import Path
from typing import List

from src.facts_maker import FactsMaker


class UserManager:


    def __init__(self):

        self._ud: dict
        self._save_dir: Path
        self._user_path: Path


    def create_user(self, user: str):
        
        self._set_paths(user)

        settings = {
            'numbers': [True for _ in range(13)],
            'operators': {'add': True, 'sub': True, 'mul': True, 'div': True},
            'patterns': {'reversed': True, 'mixed_unknowns': True},
            'timers': [0, 8, 4] }

        self._ud = {
            'user': user,
            'settings': settings,
            'facts': FactsMaker().math_facts }
        
        self.save_user()


    def load_user(self, user: str):

        self._set_paths(user)

        with open(self._user_path, 'rb') as file:
            self._ud = pickle.load(file)

    
    def _set_paths(self, user: str):

        parent_dir = Path(__file__).resolve().parents[1]
        self._save_dir = Path.joinpath(parent_dir, 'app_data')
        self._user_path = Path.joinpath(self._save_dir, f'{user}.pkl')


    def save_user(self):

        os.makedirs(self._save_dir, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(self._ud, f)


    @property
    def user_name(self) -> str:

        if self._ud['user'] is None:
            raise Exception("call load_user_data() first")

        return self._ud['user']


    @property
    def settings(self) -> dict:

        if self._ud is None:
            raise Exception("call load_user_data() first")

        return self._ud['settings']


    @property
    def math_facts(self) -> List[dict]:
        
        if self._ud is None:
            raise Exception("call load_user_data() first")
        
        return self._ud['facts']
        

    @property
    def num_facts(self) -> int:

        # fill this in later
        return 20


    @property
    def times(self) -> List[int]:

        # fill this in later
        return []


    @property
    def exclude(self) -> List[int]:

        # fill this in later
        return [0]

    
    @staticmethod
    def get_usernames() -> List[str]:

        parent_dir = Path(__file__).resolve().parents[1]
        save_dir = Path.joinpath(parent_dir, 'app_data')

        if not save_dir.exists():
            return []

        return [f.stem for f in save_dir.glob('*.pkl') if f.is_file()]