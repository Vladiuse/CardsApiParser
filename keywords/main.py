import random as r
number_keywords = [str(i) for i in range(10)]
chars_keywords = ['!', '?', '%', '$']

def get_random_char_keyword():
    keywords = number_keywords + chars_keywords
    return r.choice(keywords)


def get_random_word_from_file() -> str:
    words = []
    with open('keywords.txt') as file:
        for line in file:
            word = line.strip()
            words.append(word)
    return r.choice(words)

if __name__ == '__main__':
    print(number_keywords + chars_keywords)
    print(number_keywords)