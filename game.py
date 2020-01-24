import pydealer
import random

cardValues = {"Ace": 11,"King": 10,"Queen": 10,"Jack": 10,"10": 10,"9": 9,
                "8": 8,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2}

def BlackjackWarGame():
    #TODO While True:
    deck = pydealer.Deck()
    deck.shuffle()
    
    playersHandsList = dealCards(deck)
    dealer = pickRandomDealer(playersHandsList)

    while True:
        playersHandsList = playRound(playersHandsList,dealer)
        dealer = getNextPlayer(playersHandsList,dealer)

    #TODO



def dealCards(deck): # Just splits deck to deal, as cards are already shuffled.
    numOfPlayers = input('Are you playing with 2 or 4 players? Enter 2 or 4 and press enter.')
    if int(numOfPlayers) == 2:
        Player1 = pydealer.Stack()
        Player1.add(deck.deal(26))
        Player2 = pydealer.Stack()
        Player2.add(deck.deal(26))
        playersHandsList = [Player1,Player2]
        playerNames = ['Player 1','Player 2']
        for player,nameString in zip(playersHandsList,playerNames):
            player.name = nameString
            player.eliminated = False
            player.isDealer = False
        return playersHandsList
    elif int(numOfPlayers) == 4:
        Player1 = pydealer.Stack()
        Player1.add(deck.deal(13))
        Player2 = pydealer.Stack()
        Player2.add(deck.deal(13))
        Player3 = pydealer.Stack()
        Player3.add(deck.deal(13))
        Player4 = pydealer.Stack()
        Player4.add(deck.deal(13))
        playersHandsList = [Player1,Player2,Player3,Player4]
        playerNames = ['Player 1','Player 2','Player 3','Player 4']
        for player,nameString in zip(playersHandsList,playerNames):
            player.name = nameString
            player.eliminated = False
            player.isDealer = False
        return playersHandsList
    else:
        dealCards(deck)

def printHandSizes(playersHandsList): #TODO may not be necessary
    print('The current hand sizes are...','\n')
    for player in playersHandsList:      
        print(player.name + ': ',player.size)

def pickRandomDealer(playersHandsList):
    dealer = random.randint(0,len(playersHandsList)-1)
    print('dealer',dealer)
    playersHandsList[dealer].isDealer = True
    print(playersHandsList[dealer].name + ' is the dealer.','\n')
    return dealer

def playRound(playersHandsList,dealer):
    numOfPlayers = len(playersHandsList)
    playersHandsList = playCards(playersHandsList,dealer,numOfPlayers)
    for playerIndex in range((dealer+1)%numOfPlayers,(dealer+numOfPlayers+1)%numOfPlayers):
        player = playersHandsList[playerIndex]
        while player.result == 'continue':
            player.result = getChoice(player,currentTotal)
    #TODO

    return playersHandsList


def playCards(playersHandsList,dealer,numOfPlayers):
    for playerIndex in range((dealer+1),(dealer+numOfPlayers+1)):
        playerIndex = playerIndex % numOfPlayers
        print('pi',playerIndex)
        player = playersHandsList[playerIndex]
        player.inPlay = pydealer.Stack()
        player.inPlay.add(player.deal(2))

        if player.isDealer == False:
            print(player.name + ' is showing...')
            print(player.inPlay)
            player.result,player.total = checkTotal(player)
        elif player.isDealer == True:
            print(player.name + ', the dealer, is showing...')           
            print(player.inPlay.deal()[0])
            player.result,player.total = checkTotal(player)
    return playersHandsList      

def checkTotal(player):
    handTotal = getSum(player)
    if handTotal < 21:
        result = checkFor5Cards(player)
        return result, handTotal
    elif handTotal == 21:
        print(player.name + ' has blackjack!')
        return 'blackjack', handTotal
    elif handTotal > 21:
        checkForAce()
        print(player.name + ' has ' + handTotal + ' and has busted.')
        return 'bust', handTotal

def getSum(player,handTotal=0):
    for card in player.inPlay.cards:
        handTotal+=cardValues[card.value]
    print(player.name + ' has a total of',handTotal)
    return handTotal 

def checkFor5Cards(player):
    if player.size < 5:
        return 'continue'
    elif player.size == 5:
        print(player.name + ' has 5 cards. Blackjack!')
        return 'blackjack'

def checkForAce():
    pass

def getDealers2ndCard():
    pass

def checkForHandWinner():
    pass

def getNextPlayer(playersHandsList,previousPlayer):
    return (previousPlayer+1)%len(playersHandsList)

def getNextDealer(playersHandsList,previousDealer):

def getChoice(player,currentTotal):
    print(player.name + ' is showing ' + str(currentTotal)+'.')
    choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.')
    if choice.lower() == 'h':
        hit = player.deal(1)
        print(player.name + ' gets',hit)
        player.total = player.total += hit
        print('For a new total of',player.total)
        checkTotal
        return 'continue', 
    elif choice.lower() == 's':
        return 'stay', player.total

def warTiebreak():
    pass

def checkIfEliminated(player):
    if player.size == 0:
        player.eliminated = True
        print(player.name + ' has been eliminated.','\n')
    return player

def deleteEliminated(playersHandsList):
    for player in playersHandsList.copy():
        if player.eliminated == True:
            playersHandsList.remove(player)
    checkForGameWinner(playersHandsList)
    return playersHandsList

def checkForGameWinner(playersHandsList):
    if len(playersHandsList) == 1:
        print(playersHandsList[0].name + ' is the winner!','\n')
        return playAgain()

def playAgain():
    playNewGame = input('Would you like to play again? Enter y for yes or n for no.')
    if playNewGame.lower() == 'y':
        return
    elif playNewGame.lower() == 'n':
        exit()
    else:
        playAgain()

if __name__ == '__main__':
    BlackjackWarGame()
