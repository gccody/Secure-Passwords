import random
import string
import json
import hashlib
from getpass import getpass
from user import User


def create_salt() -> str:
    length = random.randint(20, 50)
    s = ''.join([random.choice(string.ascii_letters+string.digits+string.punctuation) for _ in range(length)])
    return s


def get_users() -> list[User]:
    with open('users.json', 'r', encoding='utf-8') as f:
        data = [User(d['username'], d['email'], d['password'], d['salt'])for d in json.loads(f.read())]
        return data


def save_config(users: list[User]):
    json_data = [user.to_json() for user in users]

    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)


def register(users: list[User], username: str, email: str, password: str) -> User | None:
    salt = create_salt()
    password = encrypt(password, salt)
    user = User(username, email, password, salt)
    if user in users: return
    return user


def login(users: list[User], email: str, password: str) -> User | None:
    for user in users:
        if (not (user.email == email)): continue
        full_pass = encrypt(password, user.salt)
        if full_pass == user.password: return user
        return
    return

def encrypt(password: str, salt: str) -> str:
    return hashlib.sha512((password+salt).encode()).hexdigest()


def get_secure_password(email: str, password: str):
    email = email.split('@')[0]


def main() -> None:
    users = get_users()
    user: User | None = None
    res: bool | None = None
    while res is None:
        try:
            res = bool(int(input("1) Register \n2) Login \nEnter 1 or 2 for register or login: "))-1)
        except ValueError:
            print("\n\nInvalid Input please only input 1 or 2")
    print()
    if not res:
        print("REGISTER:")
        while user is None:
            email = str(input("Enter Email: "))
            password = str(getpass("Enter Password: "))
            username = str(input("Enter Username: "))
            user = register(users, username, email, password)
            if user is None: print("Username or Email already exists! Try again!", end="\n\n")

        users.append(user)
        save_config(users)
        print("Success!")
    else:
        print("LOGIN:")
        email = str(input("Enter Email: "))
        password = str(getpass("Enter Password: "))
        user = login(users, email, password)
        if user is None: print("Invalid Credentials")
        else: print(f"Success! Hello {user.username}!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\nGoodbye :( <3")