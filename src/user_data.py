
import os
import pickle
from typing import List
from pathlib import Path

from src.facts_maker import MathFactDC


class UserData:


    def __init__(self):

        self._user: str
        self.save_dir: Path
        self._user_path: Path


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


    def create_user(self, user: str):

        # Create a new user with the given username
        return


    def set_user(self, user: str):

        parent_dir = Path(__file__).resolve().parents[2]
        self.save_dir = Path.joinpath(parent_dir, 'app_data')
        self._user_path = Path.joinpath(self.save_dir, f'{self._user}.pkl')


    def user_exists(self) -> bool:

        return os.path.exists(self._user_path)


    def get_settings(self) -> dict:

        with open(self._user_path, 'rb') as file:
            return pickle.load(file)['settings']


    def get_facts(self) -> List[MathFactDC]:

        with open(self._user_path, 'rb') as file:
            return pickle.load(file)['facts']


    def save_data(self, settings: dict, facts: List[MathFactDC]):

        data = {
            'settings': settings,
            'facts': facts}

        os.makedirs(self.save_dir, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(data, f)


    @staticmethod
    def get_usernames() -> List[str]:

        # Example user list, replace with actual logic
        return ["user1", "user2", "user3"]