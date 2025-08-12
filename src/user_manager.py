
import os
import pickle
from pathlib import Path
from typing import List, Dict, Any
from .facts_maker import FactsMaker



class UserManager:


    def __init__(self):

        self.user_name: str
        self.inc_nums: dict
        self.inc_oprs: dict
        self.inc_ptrns: dict
        self.num_facts: int
        self.inc_timers: bool
        self.inc_untimed: bool
        self.timer_vals: List[int]
        self.facts: Dict[int, Dict[str, Any]]
        self.user_loaded: bool = False

        self._save_dir: Path
        self._user_path: Path


    def create_new_user(self, user: str) -> None:

        self.user_name = user
        self.inc_nums = {k: True for k in range(13)}
        self.inc_oprs = {'add': True, 'sub': True, 'mul': True, 'div': True}
        self.inc_ptrns = {'reversed': True, 'mixed_unknowns': True}
        self.num_facts = 25
        self.inc_timers = True
        self.inc_untimed = True
        self.timer_vals = [9, 6, 3]
        self.facts = FactsMaker().get_facts()
        self.user_loaded = True

        self.save_user_data()


    def load_saved_user(self, user: str) -> None:

        self._set_path_attributes(user)
        if not self._user_path.exists():
            raise FileNotFoundError(
                f"user does not exist at {self._user_path}")
        with open(self._user_path, 'rb') as file:
            user_data = pickle.load(file)

        self.user_name = user_data['user_name']
        self.inc_nums = user_data['inc_nums']
        self.inc_oprs = user_data['inc_oprs']
        self.inc_ptrns = user_data['inc_ptrns']
        self.num_facts = user_data['num_facts']
        self.inc_timers = user_data['inc_timers']
        self.inc_untimed = user_data['inc_untimed']
        self.timer_vals = user_data['timer_vals']
        self.facts = user_data['facts']
        self.user_loaded = True


    def save_user_data(self) -> None:

        self._set_path_attributes(self.user_name)
        if not self.user_loaded:
            raise ValueError("no user loaded, cannot save")

        user_data = {
            'user_name': self.user_name,
            'inc_nums': self.inc_nums,
            'inc_oprs': self.inc_oprs,
            'inc_ptrns': self.inc_ptrns,
            'num_facts': self.num_facts,
            'inc_timers': self.inc_timers,
            'inc_untimed': self.inc_untimed,
            'timer_vals': self.timer_vals,
            'facts': self.facts }

        os.makedirs(self._save_dir, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(user_data, f)


    def _set_path_attributes(self, user_name: str) -> None:

        parent_dir = Path(__file__).resolve().parents[1]
        self._save_dir = Path.joinpath(parent_dir, 'data')
        self._user_path = Path.joinpath(self._save_dir, f'{user_name}.pkl')


    def delete_current_user(self) -> None:

        if not self.user_loaded:
            raise ValueError("no user loaded, cannot delete")

        os.remove(self._user_path)


    @staticmethod
    def get_saved_users() -> List[str]:

        parent_dir = Path(__file__).resolve().parents[1]
        save_dir = Path.joinpath(parent_dir, 'data')

        if not save_dir.exists():
            return []

        return [f.stem for f in save_dir.glob('*.pkl') if f.is_file()]