import pydealer
import random


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
    dealer = random.randint(0,len(playersHandsList))
    playersHandsList[dealer].isDealer = True
    print(playersHandsList[dealer].name + ' is the dealer.','\n')
    return dealer

def playRound(playersHandsList,dealer):
    playCards(playersHandsList,dealer)

    playersHandsList = playCards(playersHandsList)

    for playerIndex in range((dealer+1)%numOfPlayers,(dealer+numOfPlayers)%numOfPlayers):
        while True:
            if player.total == 'continue':
                getHit(playerToPlay)
    #TODO

    return playersHandsList


def playCards(playersHandsList,dealer):
    numOfPlayers = len(playersHandsList)
    for playerIndex in range((dealer+1)%numOfPlayers,(dealer+numOfPlayers)%numOfPlayers):
        player = playersHandsList[playerIndex]
        player.inPlay = pydealer.Stack()
        player.inPlay.add(player.deal(2))

        if player.isDealer == False:
            print(player.name + ' is showing...')
            print(player.inPlay)
            player.total = checkTotal(player)
        elif player.isDealer == True:
            print(player.name + ' is showing...')           
            print(player.inPlay.deal()[0])
            player.total = checkTotal(player)
    return playersHandsList

def getSum():
    # TODO sum cards in stack
    pass       

def checkTotal(player):
    handTotal = player.inPlay.getSum()
    if handTotal < 21:
        result = checkFor5Cards(player)
        return result 
    elif handTotal == 21:
        print(player.name + ' has blackjack!')
        return 'blackjack'
    elif handTotal > 21:
        print(player.name + ' has ' + handTotal + ' and has busted.')
        return 'bust'

def checkFor5Cards(player):
    if player.size < 5:
        return 'continue'
    elif player.size == 5:
        print(player.name + ' has 5 cards. Blackjack!')
        return 'blackjack'

def checkForHandWinner():
    pass

def getNextPlayer(playersHandsList,previousPlayer):
    return (previousPlayer+1)%len(playersHandsList)

def getHit(player,currentTotal):
    print(player.name + ' is showing ' + str(currentTotal)+'.')
    choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.')
    if choice.lower() == 'h':
        hit = player.deal(1)
        #TODO
        pass
    elif choice.lower() == 's':
        #TODO
        pass

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
        playAgain()

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
