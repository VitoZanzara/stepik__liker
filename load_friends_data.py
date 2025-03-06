import yaml
from pathlib import Path

def load_friends_data(user_file='friends_list.yml') -> dict:
    if Path(user_file).is_file():
        with open(user_file, encoding='utf-8') as f:
            user_like = yaml.safe_load(f)
        return user_like
    return {}


if __name__ == '__main__':
    friends_list = load_friends_data()
    print(friends_list)