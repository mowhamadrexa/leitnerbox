from datetime import datetime

class Leitner:

    start_date = datetime.now()

    def __init__(self, id, q, a):
        self.date_of_create = datetime.now()
        self.id = id
        self.q = q
        self.a = a
        self.level = 0

    def level_up(self):
        if self.level + 1 <= 5:
            self.level += 1
        return self.level

    def level_down(self):
        if self.level - 1 >= 1:
            self.level -= 1
        return self.level

    def question(self):
        return self.q

    def answer(self):
        return self.a

    def check(self, answer):
        if answer == self.a:
            return True
        return False

    def commit(self):
        pass

    @classmethod
    def level_turn(cls):
        levels = [1]
        now = datetime.now()
        delta = now - cls.start_date

        if  delta.days % 2 == 0:
            levels.append(2)

        if delta.days % 7 == 0:
            levels.append(3)

        if delta.days % 14 == 0:
            levels.append(4)

        return levels

    def turn(self):
        levels = Leitner.level_turn()
        if self.level in levels:
            return True
        return False

    @classmethod
    def with_model(cls, model):
        q = model.q
        a = model.a
        id = model.id
        level = model.level
        date_of_create = model.date_of_create
        return cls()