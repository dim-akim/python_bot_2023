class Human:
    """Представление человека"""
    def __init__(self, name, sex='М'):
        self.name = name
        self.sex = sex
        self.is_married = False
        self.spouse = None

    def says_hello(self):
        print(f'{self.name} приветствует тебя!')

    def marry(self, other):
        if self.is_married:
            print(f'{self.name} уже в браке!')
            # return
        else:
            self.is_married = True
            self.spouse = other  # Атрибут надо создавать при инициализации
            other.is_married = True
            other.spouse = self
            print(f'Поздравляем молодоженов: {person1.name} и {person2.name}!')
            # можно объединить с атрибутом is_married


class Male(Human):
    def __init__(self, name):
        super().__init__(name)


class Female(Human):
    def __init__(self, name):
        super().__init__(name, sex='Ж')


if __name__ == '__main__':
    person1 = Male('Гоша')
    person2 = Female('Маша')
    person3 = Male('Влад')

    person1.marry(person2)
    person1.marry(person3)
