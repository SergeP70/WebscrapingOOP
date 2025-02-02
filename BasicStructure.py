class User:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    def get_name(self):
        capital_name = str(self.name).upper()
        return capital_name

    def age(self, current_year):
        age = current_year - self.birth_year
        return age


if __name__ == '__main__':
    user = User(name='John', birth_year=1999)
    age = user.age(current_year=2023)
    name = user.get_name()
    print(f"{name} is {age} years old")
    user2 = User(name= 'Serge', birth_year=1970)
    age2 = user2.age(current_year=2025)
    name2 = user2.get_name()
    print(f"{name2} is {age2} years old")