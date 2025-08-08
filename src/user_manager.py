
import os
import pickle
from pathlib import Path
from typing import List
from copy import deepcopy as copy

from src.facts_maker import FactsMaker


class UserManager:


    def __init__(self):

        #self._data: dict = {}

        self._inc_nums = {}
        self._inc_oprs = {}
        

        self._save_dir: Path
        self._user_path: Path
        self._user_loaded = False


    def create_user(self, user: str):

        settings = {
            'inc_nums': {k: True for k in range(13)},
            'inc_oprs': {'add': True, 'sub': True, 'mul': True, 'div': True},
            'inc_ptrns': {'reversed': True, 'mixed_unknowns': True},
            'num_facts': 25,
            'inc_timers': True,
            'inc_untimed': True,
            'timers': [8, 4] }
        self._data = {
            'user_name': user,
            'settings': settings,
            'facts': FactsMaker().get_facts() }
        
        self._save_user_data()
        self.load_saved_user(user)


    def _save_user_data(self):

        try:
            self._set_path_attributes(self._data['user_name'])
        except KeyError:
            raise ValueError("call create_user() or load_saved_user() first")

        os.makedirs(self._save_dir, exist_ok=True)
        with open(self._user_path, 'wb') as f:
            pickle.dump(self._data, f)


    def load_saved_user(self, user: str):

        self._set_path_attributes(user)
        if not self._user_path.exists():
            raise FileNotFoundError(f"User does not exist at {self._user_path}")
        with open(self._user_path, 'rb') as file:
            self._data = pickle.load(file)

        self._user_loaded = True


    def _set_path_attributes(self, user_name: str):

        parent_dir = Path(__file__).resolve().parents[1]
        self._save_dir = Path.joinpath(parent_dir, 'app_data')
        self._user_path = Path.joinpath(self._save_dir, f'{user_name}.pkl')


    def save_new_username(self, new_username: str):

        os.remove(self._user_path)
        self._data['user_name'] = new_username
        self._save_user_data()


    def save_new_settings(self, settings: dict):

        self._data['settings'] = copy(settings)
        self._save_user_data()


    def save_new_facts(self, facts: List[dict]):

        self._data['facts'] = copy(facts)
        self._save_user_data()


    def delete_user(self):

        os.remove(self._user_path)
        self._user_loaded = False
        self._data = {}


    @property
    def data(self):

        return copy(self._data)


    @staticmethod
    def get_saved_users() -> List[str]:

        parent_dir = Path(__file__).resolve().parents[1]
        save_dir = Path.joinpath(parent_dir, 'app_data')

        if not save_dir.exists():
            return []

        return [f.stem for f in save_dir.glob('*.pkl') if f.is_file()]
    

    @property
    def user_loaded(self) -> bool:

        return self._user_loaded


    @property
    def include_timers(self) -> bool:

        return self._data['settings']['inc_timers']
    

    # @property
    # def settings(self) -> dict:

    #     if self._ud is None:
    #         raise Exception("call load_data() first")

    #     return self._ud['settings']


    # @property
    # def math_facts(self) -> List[dict]:
        
    #     if self._ud is None:
    #         raise Exception("call load_data() first")
        
    #     return self._ud['facts']
        

    # @property
    # def num_facts(self) -> int:

    #     # fill this in later
    #     return 20


    # @property
    # def times(self) -> List[int]:

    #     # fill this in later
    #     return []


    # @property
    # def exclude(self) -> List[int]:

    #     # fill this in later
    #     return [0]

    
    

    # def _on_create_clicked(self):

    #     cbbox_val = self._combobox.get()

    #     errs = []
    #     if not cbbox_val[0].isalpha():
    #         errs.append("start with a letter")            
    #     if len(cbbox_val) < 3:
    #         errs.append("be at least three characters long")
    #     whitelist = string.ascii_letters + string.digits + '_'
    #     if not all(c in whitelist for c in cbbox_val):
    #         errs.append("contain only letters, digits, and underscores")
    #     if errs:
    #         message = "Username should:\n" + "\n".join(f"  - {err}" for err in errs)
    #         self.option_add("*Dialog.msg.font", self._small_font)
    #         self.option_add("*Dialog.msg.wrapLength", "0")
    #         messagebox.showinfo("Requirements", message)
    #         return
        
    #     self._user.create_user(cbbox_val)
    #     self._combobox['values'] = self._user.get_usernames()
    #     self._on_user_update()