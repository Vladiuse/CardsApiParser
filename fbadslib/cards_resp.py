from pprint import pprint
import json
from exeptions import *

def fb_responce_to_dict(text):
    pos = text.index('{')
    text = text[pos:]
    data = json.loads(text)
    return data



class FbCardsRes:

    def __init__(self, data):
        self.data = data
        self._is_cards_exists()
        self.cards = self._get_cards()

    def _is_cards_exists(self):
        if self.data['payload']:
            return True
        with open('./logs/empty_res.json', 'w') as file:
            file.write(str(self.data))
        raise EmptyAdsLibResponse(self.data)

    def show_tokens(self):

        print('forwardCursor', self.forward_cursor if len(self.forward_cursor) < 33 else self.forward_cursor[:33]+'...')
        print('collationToken', self.collation_token)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        self.i = 0
        return self

    def get_group_links(self):
        links = []
        for card in self:
            if card.fb_group_url:
                links.append(card.fb_group_url)
        return links

    def __next__(self):
        try:
            item = self.cards[self.i]
            self.i += 1
            return item
        except IndexError:
            raise StopIteration

    @property
    def forward_cursor(self):
        cursor = self.data['payload']['forwardCursor']
        if not cursor:
            raise LibEnds
        return cursor

    @property
    def collation_token(self):
        return self.data['payload']['collationToken']

    def _get_cards(self):
        cards = []
        for card_data in self.data['payload']['results']:
            card = Card(card_data)
            cards.append(card)
        return cards

class Card:

    def __init__(self, data: dict):
        self.data = data[0]


    def __str__(self):
        return f'{self.group_id} {self.page_name}'

    @property
    def page_name(self):
        return self.data['pageName']

    @property
    def group_id(self):
        return self.data['pageID']
    @property
    def ad_archive_id(self):
        return self.data['adArchiveID']


    @property
    def fb_group_url(self):
        return self.data['snapshot']['page_profile_uri']



if __name__ == '__main__':
    with open('../z_work/x.json') as file:
        text = file.read()
        data = fb_responce_to_dict(text)

    print(data.keys())

    cards = FbCardsRes(data)
    print(len(data['payload']['results']))
    # print(len(cards))
    # print(cards.forward_cursor, cards.collation_token)
    # for card in cards:
    #     pprint(card.data)
    #     break

