import pydealer
import random

class BlackjackWarGame:
    def __init__(self):
        self.cardValues = {"Ace": 11,"King": 10,"Queen": 10,"Jack": 10,"10": 10,"9": 9,
                            "8": 8,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2}

        self.playGame()
    
    def playGame(self):
        # TODO While True:
        # Plays full game
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        
        self.dealCards()
        
        self.pickRandomDealer()

        while True: # Plays one round
            self.playRound()
            self.printHandSizes()
            
            self.getNextDealer()

        #TODO

    def dealCards(self): # Just splits deck to deal, as cards are already shuffled.
        self.numOfPlayers = input('Are you playing with 2 or 4 players? Enter 2 or 4 and press enter.\n')
        if int(self.numOfPlayers) == 2:
            self.Player1 = pydealer.Stack()
            self.Player1.add(self.deck.deal(26))
            self.Player2 = pydealer.Stack()
            self.Player2.add(self.deck.deal(26))
            self.playersHandsList = [self.Player1,self.Player2]
            self.playerNamesList = ['Player 1','Player 2']
            for player,nameString in zip(self.playersHandsList,self.playerNamesList):
                player.name = nameString
                player.eliminated = False
                player.isDealer = False
        elif int(self.numOfPlayers) == 4:
            self.Player1 = pydealer.Stack()
            self.Player1.add(self.deck.deal(13))
            self.Player2 = pydealer.Stack()
            self.Player2.add(self.deck.deal(13))
            self.Player3 = pydealer.Stack()
            self.Player3.add(self.deck.deal(13))
            self.Player4 = pydealer.Stack()
            self.Player4.add(self.deck.deal(13))
            self.playersHandsList = [self.Player1,self.Player2,self.Player3,self.Player4]
            self.playerNames = ['Player 1','Player 2','Player 3','Player 4']
            for player,nameString in zip(self.playersHandsList,self.playerNames):
                player.name = nameString
                player.eliminated = False
                player.isDealer = False
        else:
            self.dealCards()

    def printHandSizes(self):
        print('The current hand sizes are now:')
        for player in self.playersHandsList:      
            print(player.name + ':',player.size)
        print('\n'*2)

    def pickRandomDealer(self):
        self.dealerIndex = random.randint(0,len(self.playersHandsList)-1)
        self.playersHandsList[self.dealerIndex].isDealer = True
        print(self.playersHandsList[self.dealerIndex].name + ' is the dealer to start.','\n')

    def playRound(self):
        self.numOfPlayers = len(self.playersHandsList)
        self.playCards()
        for playerIndex in range(self.dealerIndex+1,self.dealerIndex+1 + self.numOfPlayers):
            playerIndex %= self.numOfPlayers
            player = self.playersHandsList[playerIndex]
            if player.isDealer == True:
                print('It is the dealer\'s turn. The dealer\'s hidden card is a',player.inPlay[1])
                print(player.name + ' has a total of',player.handTotal,'\n'*2)
            while player.result == 'continue':
                self.getChoice(player)
        
        self.checkHandWinner()
        
        #TODO

    def playCards(self):
        for playerIndex in range(self.dealerIndex+1,self.dealerIndex+1 + self.numOfPlayers):
            Index = playerIndex % self.numOfPlayers
            player = self.playersHandsList[Index]
            player.inPlay = pydealer.Stack()
            player.inPlay.add(player.deal(2))
            if player.isDealer == False:
                print(player.name + ' is showing...')
                print(player.inPlay,'\n')
                self.checkTotal(player)
            elif player.isDealer == True:
                print(player.name + ', the dealer, is showing...')           
                print(player.inPlay[0],'\n')
                self.checkTotal(player)
                if player.result == 'continue':
                    print(player.name + ' has a total of',self.cardValues[player.inPlay[0].value],'\n'*2)    

    def checkTotal(self,player):
        self.getSum(player)
        if player.handTotal < 21:
            player.result = self.checkFor5Cards(player)
        elif player.handTotal == 21:
            print(player.name + ' has blackjack!','\n'*2)
            player.result = 'blackjack'
        elif player.handTotal > 21:
            self.checkForAce()
            print(player.name + ' has ' + str(player.handTotal) + ' and has busted.','\n'*2)
            player.result = 'bust'

    def getSum(self,player,handTotal=0): # TODO implement sum that adds last hit instead of counting hand each time
        for card in player.inPlay.cards:
            handTotal += self.cardValues[card.value]
        player.handTotal = handTotal
        if player.isDealer == False:
            print(player.name + ' has a total of',player.handTotal,'\n'*2)

    def checkFor5Cards(self,player):
        if player.inPlay.size < 5:
            return 'continue'
        elif player.inPlay.size == 5:
            print(player.name + ' has 5 cards. Blackjack!','\n'*2)
            return 'blackjack'

    def getChoice(self,player):
        print('It is ' + player.name +'\'s turn.')
        print(player.name + ' is showing a total of '+ str(player.handTotal) + '.')
        choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.')
        if choice.lower() == 'h':
            hit = player.deal(1)
            print(player.name + ' gets',hit)
            player.add(hit)
            self.checkTotal(player)
            print('For a new total of',player.handTotal)
        elif choice.lower() == 's':
            player.result = 'stay'


    def checkForAce(self):
        pass

    def getDealers2ndCard(self):
        pass

    def checkHandWinner(self):
        pass

    def getNextPlayer(self):
        return (previousPlayer+1)%len(self.playersHandsList)

    def getNextDealer(self):
        pass

    def warTiebreak(self):
        pass

    def divideWinnersCards(self):
        pass

    def checkIfEliminated(self,player):
        if player.size == 0:
            player.eliminated = True
            print(player.name + ' has been eliminated.','\n')
            self.playersHandsList.remove(player)
            self.checkForGameWinner()

    def checkForGameWinner(self):
        if len(self.playersHandsList) == 1:
            print(self.playersHandsList[0].name + ' is the winner!','\n')
            self.playAgain()

    def playAgain(self):
        playNewGame = input('Would you like to play again? Enter y for yes or n for no.')
        if playNewGame.lower() == 'y':
            pass
        elif playNewGame.lower() == 'n':
            exit()
        else:
            self.playAgain()


BlackjackWarGame()
