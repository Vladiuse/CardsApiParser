import json
from pathlib import Path
import os
import random as r

curr_file_path = Path(__file__).parent.absolute()
countries_data_file_path = os.path.join(curr_file_path, './countries.json')


class Country:

    def __init__(self, *, iso, ru_name, population, parse_population_conf, languages):
        self.iso = iso.upper()
        self.name = ru_name
        self.population = population
        self.parse_population_conf = parse_population_conf
        self.languages = [self._dict_to_langs_class(item) for item in languages]

    def __str__(self):
        return f'({self.iso}) {self.name}'

    @staticmethod
    def _dict_to_langs_class(dict):
        lang = Language(**dict)
        return lang

    def get_random_lang(self):
        population = [lang.iso for lang in self.languages]
        weights = [lang.weight for lang in self.languages]
        lang_iso = r.choices(population=population, weights=weights)[0]
        for lang in self.languages:
            if lang.iso == lang_iso:
                return lang
        raise ValueError('Язык не выбран')

def load_countries():
    with open(countries_data_file_path, encoding='utf-8') as file:
        data = json.load(file)
    countries = dict()
    for iso_code, item in data.items():
        country = Country(iso=iso_code, **item)
        countries[iso_code.upper()] = country
    return countries

class Language:

    def __init__(self,*, name, iso, weight, keys_deep):
        self.name = name
        self.iso = iso
        self.weight = weight
        self.keys_deep = keys_deep

    def __repr__(self):
        return f'{self.name} ({self.iso})'

    def __str__(self):
        return self.iso.lower()


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
        self._keys = list(self.data.keys())
        return self

    def __next__(self):
        try:
            key = self._keys[self.i]
            item = self.data[key]
            self.i += 1
            return item
        except IndexError:
            raise StopIteration

    def get_random(self):
        """Получить рандомную страну с учетом весового коофициента"""
        countries_iso = [c.iso for c in self]
        parse_population_conf = [c.parse_population_conf for c in self]
        random_country_code = r.choices(population=countries_iso, weights=parse_population_conf, k=1)[0]
        return self[random_country_code]


countries = Countries()

if __name__ == '__main__':
    us = countries['ID']
    results = {}
    for i in range(100):
        lang = us.get_random_lang()
        try:
            results[str(lang)] += 1
        except KeyError:
            results[str(lang)] = 1
    print(results)
