import random
import csv


filename = "../results/data.csv"

number = [1,2,3,4]
shape = ["circle","square","triangle","star"]
color = ["blue","green","red","yellow"]
winning_streak = 0

logger = []

class Card:
    def __init__(self,number,shape,color):
        self.number = number
        self.shape = shape
        self.color = color
        
            
class Stack():
    def __init__(self,list_of_cards,pos):
        self.list_of_cards = list_of_cards
        self.pos = pos
        
    def get(self,new_card):
        self.list_of_cards.append(new_card)
    
    def give(self):
        return self.list_of_cards.pop()
    
    def render(self):
        print(self.list_of_cards[-1].shape,self.list_of_cards[-1].number,self.list_of_cards[-1].color)
        

def construct_deck(number,shape,color):
    deck = []
    for i in number:
        for y in shape:
            for x in color:
                card = Card(i,y,x)
                deck.append(card)
    return deck
 

stimulus_card = [
    Card(1, "triangle", "red"),
    Card(2, "star", "green"),
    Card(3, "square", "yellow"),
    Card(4, "circle", "blue")
]
               
                
# Deck
deck = construct_deck(number,shape,color)
deck_active = deck.copy()
random.shuffle(deck_active)

#Rules
rule = ['number','shape','color']
active_rule = random.choice(rule)

#Make stacks
stack_hand = Stack(deck_active,1)
stack_1 = Stack([stimulus_card[0]], 2)
stack_2 = Stack([stimulus_card[1]], 3)
stack_3 = Stack([stimulus_card[2]], 4)
stack_4 = Stack([stimulus_card[3]], 5)
d_stack1= Stack([],6)
d_stack2= Stack([],7)
d_stack3= Stack([],8)
d_stack4= Stack([],9)

stim = [stack_1,stack_2,stack_3,stack_4]
discard = [d_stack1,d_stack2,d_stack3,d_stack4]


def feedback(active_rule,choice):
    return getattr(stimulus_card[choice], active_rule) == getattr(stack_hand.list_of_cards[-1], active_rule)

def update_streak(win,choice):
    global winning_streak
    global logger
    if win:
         winning_streak += 1
         used_rule = matched_rule(choice)
         logger.append((1,used_rule,active_rule,winning_streak))
         print(f"Streak:{winning_streak}\n")
         return winning_streak
    else:
         winning_streak = 0
         used_rule = matched_rule(choice)
         logger.append((0,used_rule,active_rule,winning_streak))
         print(f"Streak:{winning_streak}\n")
         return winning_streak

def change_rule():
    global winning_streak
    global active_rule
    new_rule = []
    if winning_streak == 5:
        new_rule = random.choice(rule)
        while new_rule == active_rule:
            new_rule = random.choice(rule)
        active_rule = new_rule
        winning_streak = 0

def user_input():
    while True:
        try:
            c = int(input("Type 1, 2, 3, or 4 to choose where to group your card: "))
            if c in [1, 2, 3, 4]:
                return c - 1
            else:
                print("Please enter a valid choice (1, 2, 3, or 4).")
        except ValueError:
            print("Please enter a valid choice (1, 2, 3, or 4).")
            

             
def place_card(choice):
    discard[choice].get(stack_hand.give())

def visuals():
    print("----HAND----")
    stack_hand.render()
    print("##############")
    for stack in stim:
                stack.render()
     
   
def matched_rule(choice):
    matched = ""
    if stack_hand.list_of_cards[-1].color == stimulus_card[choice].color:
        matched += "color"
    if stack_hand.list_of_cards[-1].shape == stimulus_card[choice].shape:
        matched += "shape"
    if stack_hand.list_of_cards[-1].number == stimulus_card[choice].number:
        matched += "number"
    
    return matched if matched else "NONE"


def save_results(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


#GameLoop
while deck_active:
    visuals()
    choice = user_input()
    win = feedback(active_rule,choice)
    update_streak(win,choice)
    place_card(choice)
    change_rule()
    print("____________________________________________________________________")

print("Game Over")

save_results(logger,filename)

 
