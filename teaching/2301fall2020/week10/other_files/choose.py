def choose(your_cards, your_hand):
    '''
    This is where you implement your strategy
    
    You can implement any strategy you want. You need to return True or False 
    based on your hand and your cards
    '''
    if your_hand < 17:
        return True
    if your_hand == 17 and len(your_cards) == 2:
        return True
    else:
        return False
