import json
from pathlib import Path
import os
import random as r

curr_file_path = Path(__file__).parent.absolute()
countries_data_file_path = os.path.join(curr_file_path, './countries.json')
class Country:

    def __init__(self,* ,iso, name, population):
        self.iso = iso.upper()
        self.name = name
        self.population = population

    def __str__(self):
        return f'({self.iso}) {self.name}'





def load_countries():
    with open(countries_data_file_path) as file:
        data = json.load(file)
    countries = dict()
    for iso_code, item in data.items():
        country = Country(iso=iso_code,**item)
        countries[iso_code.upper()] = country
    return countries

class Countries:

    def __init__(self):
        self.data = load_countries()

    def __getitem__(self, country_code):
        if not isinstance(country_code, str):
            raise TypeError('Country id must be string type')
        if len(country_code) != 2:
            raise ValueError('Country code myst contain 2 chars')
        country_code = country_code.upper()
        return self.data[country_code]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        self.i = 0
        self._keys  = list(self.data.keys())
        return self

    def __next__(self):
        try:
            key = self._keys[self.i]
            item = self.data[key]
            self.i += 1
            return item
        except IndexError:
            raise StopIteration


    def get_ramdom(self):
        keys = list(self.data.keys())
        random_key = r.choice(keys)
        return self[random_key]

countries = Countries()

if __name__ == '__main__':

    c = countries.get_ramdom()
    print(c)



