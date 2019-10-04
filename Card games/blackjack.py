import random
class card:
    def __init__(self,suit,number):
        self.suit = suit
        self.number = number

    def score(self):
        if self.number == "A":
            return [11,1]
        elif self.number == "J" or self.number == "Q" or self.number == "K":
            return 10
        else:
            return int(self.number)

    def printCard(self):
        return " "+self.number + self.suit + " "

class cardDeck:
    backside = "█"
    def shuffle(self):
        self.cardNumber = 0
        random.shuffle(self.deck)

    def getCard(self):
        card = self.deck[self.cardNumber]
        self.cardNumber += 1
        return card


    def __init__(self):
        self.deck = []
        for suit in ["♦","♣","♥","♠"]:
            for number in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]:
                self.deck.append(card(suit,number))
deck = cardDeck()
deck.shuffle()

def printBoard(players,dealer):
    min = 6
    for player in players:
        min = max(len(player[0]),min) #For pretty printing, a parser is needed to check the max length of a name.
    if len(dealer) == 0:
        cards =" " *7 + "Cards" + " " *8
    else:
        cards = "    " * (5 - len(dealer))
        for card in dealer[::-1]:
            cards = card.printCard() + cards
    min+=1
    print("="*(min+20+14))
    string = "Dealer" + " "*(min-6) + "||" + cards + "||" + " Bet"
    print(string)
    print(" "*min + "||" + "  " * 10 +"||")
    for player in players:
        if len(player[1]) == 0:
            cards = "  " * 10
        else:
            cards = "    " * (5 - len(player[1]))
            for card in player[1][::-1]:
                cards = card.printCard() + cards
        string = player[0] + " " * (min-len(player[0]))+"||" + cards + "|| "+str(player[2])
        print(string)
    print("=" * (min + 20 + 14))

def betting(players):
    round = []
    for player in players:
        bet = input(player[0] + ", please enter your bet. Current balance: " + str(player[1])+"\n")
        player[1] -= int(bet)
        round.append([player[0],[],bet])
    return round

def scoreCalc(cards):
    totals = [0]
    for card in cards:
        if isinstance(card.score(),list):
            temp = totals[-1] + 11
            for i in range(len(totals)):
                totals[i] += 1
            totals.append(temp)
        else:
            for i in range(len(totals)):
                totals[i] += card.score()
    max = 0
    for total in totals:
        if total<=21 and total > max:
            max = total
    if(max == 0): return min(totals)
    return max

def endOfRound(round,dealerScore,players):
    for i in range(len(round)):
        score = scoreCalc(round[i][1])
        if score > dealerScore and score <= 21:
            bet = round[i][2]
            players[i][1] + bet * 2
            print("Congratulations "+round[i][0] + " you won " + str(bet*2) + " this round!")
        elif score == dealerScore:
            bet = round[i][2]
            players[i][1] += bet
    return players



def blackJackRound(round):
    dealer = [deck.getCard()]
    hidden = deck.getCard()
    for player in round:
        player[1].append(deck.getCard())
        player[1].append(deck.getCard())
    printBoard(round,dealer)
    input()
    for player in round:
        while( True ):
            score = scoreCalc(player[1])
            if (score == 21):
                print(player[0] + ", you got blackjack!")
                input()
                break
            elif (score > 21):
                print(player[0] + ", you busted with a score of "+str(score)+"!")
                input()
                break
            else:
                print(player[0] + ", with a score of " + str(score))
            prompt = input("\n1) Would you like a Card or\n2) Stay with your cards\n")
            if(prompt == "2"): break
            elif(prompt != "1"): continue
            player[1].append(deck.getCard())
            printBoard(round,dealer)
    dealer.append(hidden)
    score = scoreCalc(dealer)
    while (score < 17):
        dealer.append(deck.getCard())
        score = scoreCalc(dealer)
        if (score > 21):
            print("Dealer busted! Congratulations to the winners!")
            break
        printBoard(round,dealer)
    if (score == 21):
        print("Dealer got blackjack!")
    elif (score >= 17):
        print("Dealer stays with a score of " + str(score))
    input()
    return [round,score]

def blackJackMain(players):
    round = betting(players)
    outcome = blackJackRound(round)
    players = endOfRound(outcome[0],outcome[1],players)
    while( True ):
        prompt = input("Wanna play another round?\n1)Yes\n2)No")
        if prompt == "1": blackJackMain(players)
        elif prompt == "2": break

def blackjackStart(numPlayers,balance):
    players = []
    for i in range(1,numPlayers+1):
        name = input("Please give me the name of the " + str(i) + ". player\n")
        players.append([name,balance])
    blackJackMain(players)
blackjackStart(2,1000)