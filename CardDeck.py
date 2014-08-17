import random

class Card:
    def __init__(self,name,cardtype):
        self.name = name
        self.cardtype = cardtype
    
    def __str__(self):
        return "({0},{1})".format(self.name,self.cardtype)
    def __repr__(self):
        return "Card({0},{1})".format(self.name,self.cardtype)
    
    def get_cardtype(self):
        return self.cardtype
    
    def get_name(self):
        return self.name
    


class CardDeck:
    
    all_card_info = ([('Dagger', 'weapon'), ('Rope', 'weapon'), ('Lead Pipe', 'weapon'), ('Candlestick', 'weapon'), ('Revolver', 'weapon'), ('Wrench', 'weapon'),
                 ('Col. Mustard', 'character'), ('Prof. Plum', 'character'), ('Miss. Scarlett', 'character'), ('Mr. Green', 'character'), ('Mrs. Peacock', 'character'), ('Mrs. White', 'character'),
                 ('Kitchen', 'room'), ('Dining Room', 'room'), ('Lounge', 'room'), ('Hall', 'room'), ('Study', 'room'), ('Library', 'room'), ('Billiard Room', 'room'), ('Conservatory', 'room'), ('Ballroom', 'room')
                 ])
    
    def __init__(self):
        self.cards = [Card(card_info[0],card_info[1]) for card_info in self.all_card_info]
        self.null_card = Card("None","none")
    
    def get_random_card(self,cardtype=None,ignore=[]):
        notFound = True
        while notFound:
            card = random.choice([x for x in self.cards if x not in ignore])
            if not cardtype:
                return card
            elif card.get_cardtype() == cardtype:
                return card
    
    def length(self):
        return len(self.all_card_info)
    
    def get_cardlist(self,cardtype=None):
        if cardtype != None:
            card_list = [x[0] for x in self.all_card_info if x[1] == cardtype]
        else:
            card_list = [x[0] for x in self.all_card_info]
        return card_list
    
    def get_card(self,name,cardtype=None):
        requested_card = None
        for card in self.cards:
            if card.get_name().strip().lower() == name.strip().lower():
                requested_card = card
                break
        
        return requested_card
    
    def find_card(self,name):
        requested_card = ""
        for card in self.cards:
            if card.get_name().strip().lower() == name.strip().lower():
                requested_card = card.get_name()
                break
        return requested_card