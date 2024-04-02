import random as r
number_keywords = [str(i) for i in range(10)]
chars_keywords = ['!', '?', '%', '$']

def get_random_keyword():
    keywords = number_keywords + chars_keywords
    return r.choice(keywords)

if __name__ == '__main__':
    print(number_keywords + chars_keywords)
    print(number_keywords)