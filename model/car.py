# -*-coding:Utf-8 -*


class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __str__(self):
        return "{} {} {}".format(self.brand, self.model, self.year)