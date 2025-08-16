
import hashlib
import math
from pathlib import Path
import string
from typing import List



def sha256_hash(password) -> str:
    
    encoded = password.encode()
    return hashlib.sha256(encoded).hexdigest()



def basic_password_check(password: str) -> bool:

    scaler = 0
    if any(c in string.ascii_lowercase for c in password): scaler += 26
    if any(c in string.ascii_uppercase for c in password): scaler += 26
    if any(c in string.digits for c in password): scaler += 10
    if any(c in string.punctuation for c in password): scaler += 32
    return len(set(password)) * scaler > 200



def shannon_password_check(password) -> bool:
    
    char_count = len(password)
    freq = {}
    for char in password:
        freq[char] = freq.get(char, 0) + 1
    entropy_per_char = 0
    for count in freq.values():
        prob = count / char_count
        entropy_per_char -= prob * math.log2(prob)
    total_entropy = entropy_per_char * char_count
    return total_entropy > 20



def get_saved_users() -> List[str]:

    parent_dir = Path(__file__).resolve().parents[1]
    save_dir = Path.joinpath(parent_dir, 'data')

    if not save_dir.exists():
        return []

    return [f.stem for f in save_dir.glob('*.pkl') if f.is_file()]