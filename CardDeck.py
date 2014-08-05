import random

class Card:
    def __init__(self,name,cardtype):
        self.name = name
        self.cardtype = cardtype
    
    def get_cardtype(self):
        return self.cardtype
    
    def get_name(self):
        return self.name
    


class CardDeck:
    
    all_card_info = ([('Dagger', 'weapon'), ('Rope', 'weapon'), ('Lead Pipe', 'weapon'), ('Candlestick', 'weapon'), ('Revolver', 'weapon'), ('Wrench', 'weapon'),
                 ('Col. Mustard', 'character'), ('Prof. Plum', 'character'), ('Miss. Scarlett', 'character'), ('Mr. Green', 'character'), ('Mrs. Peacock', 'character'), ('Mrs. White', 'character'),
                 ('Kitchen', 'room'), ('Dining Room', 'room'), ('Lounge', 'room'), ('Hall', 'room'), ('Study', 'room'), ('Library', 'room'), ('Billard Room', 'room'), ('Conservatory', 'room'), ('Ball Room', 'room')
                 ])
    
    def __init__(self):
        self.cards = [Card(card_info[0],card_info[1]) for card_info in self.all_card_info]
    
    def get_random_card(self,cardtype):
        notFound = True
        while notFound:
            card = random.choice(self.cards)
            if card.get_cardtype() == cardtype:
                return card
    
    def get_cardlist(self,cardtype=None):
        if cardtype != None:
            card_list = [x[0] for x in self.all_card_info if x[1] == cardtype]
        else:
            card_list = [x[0] for x in self.all_card_info]
        return card_list
    
    def get_card(self,name,cardtype):
        requested_card = None
        for card in self.cards:
            if card.get_name() == name and card.get_cardtype() == cardtype:
                requested_card = card
                break
        return requested_card