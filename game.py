import pydealer
import random

class BlackjackWarGame:
    def __init__(self):
        self.cardValues = {"Ace":11,"King":10,"Queen":10,"Jack":10,"10":10,
                            "9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
        self.playGame()
    
    def playGame(self):
        # TODO While True: # To play another game
        # Plays full game
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.dealCards()
        self.pickRandomDealer()
        while True: # Plays one round
            self.bustsList = []
            self.blackjackList = []        
            skip = self.playRound()
            self.checkRoundWinner(skip)
            
            self.printHandSizes()
            self.getNextDealer()
            self.deleteEliminated() # TODO Find better way to eliminate player
            self.getRightDealerIndex()
            print(self.dealer.name + ' is the next dealer.','\n')

    def dealCards(self): # Just splits deck to deal, as cards are shuffled. Actual visual can deal one at a time.
        self.numOfPlayers = input('Are you playing with 2 or 4 players? Enter 2 or 4 and press enter.\n')
        if int(self.numOfPlayers) == 2:
            self.Player1 = pydealer.Stack()
            self.Player1.add(self.deck.deal(26))
            self.Player2 = pydealer.Stack()
            self.Player2.add(self.deck.deal(26))
            self.playerList = [self.Player1,self.Player2]
            self.playerNamesList = ['Player 1','Player 2']
            for player,nameString in zip(self.playerList,self.playerNamesList):
                player.name = nameString
                player.eliminated = False
        elif int(self.numOfPlayers) == 4:
            self.Player1 = pydealer.Stack()
            self.Player1.add(self.deck.deal(13))
            self.Player2 = pydealer.Stack()
            self.Player2.add(self.deck.deal(13))
            self.Player3 = pydealer.Stack()
            self.Player3.add(self.deck.deal(13))
            self.Player4 = pydealer.Stack()
            self.Player4.add(self.deck.deal(13))
            self.playerList = [self.Player1,self.Player2,self.Player3,self.Player4]
            self.playerNames = ['Player 1','Player 2','Player 3','Player 4']
            for player,nameString in zip(self.playerList,self.playerNames):
                player.name = nameString
                player.eliminated = False
        else:
            self.dealCards()

    def printHandSizes(self):
        print('The current hand sizes are now:')
        for player in self.playerList:      
            print(player.name + ':',player.size)
        print('\n'*2)

    def pickRandomDealer(self):
        self.dealerIndex = random.randint(0,len(self.playerList)-1)
        self.dealer = self.playerList[self.dealerIndex]
        print(self.dealer.name + ' is the dealer to start.','\n')
    
    def getNextDealer(self): # TODO
        self.dealerIndex+=1
        self.dealerIndex%=self.numOfPlayers
        if self.playerList[self.dealerIndex].eliminated==False:
            self.dealer=self.playerList[self.dealerIndex]
        else:
            self.getNextDealer()

    def getRightDealerIndex(self):
        if self.playerList[self.dealerIndex].name != self.dealer.name:
            self.dealerIndex+=1
            self.dealerIndex%=self.numOfPlayers
            self.getRightDealerIndex()

    def playRound(self):
        self.numOfPlayers = len(self.playerList)
        self.playCards()
        for playerIndex in range(self.dealerIndex+1,self.dealerIndex+1 + self.numOfPlayers):
            if len(self.bustsList)==self.numOfPlayers-1:
                return True
            playerIndex %= self.numOfPlayers
            player = self.playerList[playerIndex]
            if self.dealer.name == player.name:
                print('##########')
                print('It is the dealer\'s turn. The dealer\'s hidden card is a',player.inPlay[1])
                print('So they have:')
                print(player.inPlay,'\n')
                print(player.name + ' has a total of',player.handTotal)
                print('\n')
            while player.result == 'continue':
                self.getChoice(player)
        return False

    def playCards(self):
        for playerIndex in range(self.dealerIndex+1,self.dealerIndex+1 + self.numOfPlayers):
            indexVal = playerIndex % self.numOfPlayers
            player = self.playerList[indexVal]
            player.inPlay = pydealer.Stack()
            try:
                player.inPlay.add(player.deal(2))
            except:
                self.checkIfEliminated(player)
                continue
            if self.dealer.name != player.name:
                print('##########')
                print(player.name + ' is showing...')
                print(player.inPlay,'\n')
                self.checkTotal(player)
            elif self.dealer.name == player.name:
                print('##########')
                print(player.name + ', the dealer, is showing...')           
                print(player.inPlay[0],'\n')
                self.checkTotal(player)
                if player.result == 'continue':
                    print(player.name + ' is showing a total of',self.cardValues[player.inPlay[0].value],'\n')    

    def checkTotal(self,player):
        self.getSum(player)
        if player.handTotal < 21:
            player.result = self.checkFor5Cards(player)
        elif player.handTotal == 21:
            print(player.name + ' has blackjack!','\n')
            player.result = 'blackjack'
            self.blackjackList.append(player)
        elif player.handTotal > 21:
            self.checkForAce()
            print(player.name + ' has ' + str(player.handTotal) + ' and has busted.','\n')
            player.result = 'bust'
            self.bustsList.append(player)

    def getSum(self,player,handTotal=0): # TODO implement sum that adds last hit instead of counting whole hand
        for card in player.inPlay.cards:
            handTotal += self.cardValues[card.value]
        player.handTotal = handTotal
        if self.dealer.name != player.name:
            print(player.name + ' has a total of',player.handTotal,'\n')

    def checkFor5Cards(self,player):
        if player.inPlay.size < 5:
            return 'continue'
        elif player.inPlay.size == 5:
            print(player.name + ' has 5 cards. Blackjack!','\n')
            self.blackjackList.append(player)
            return 'blackjack'

    def getChoice(self,player):
        print('#####')
        print('It is ' + player.name +'\'s turn.')
        print(player.name + ' is showing a total of '+ str(player.handTotal) + '.')
        choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.\n')
        if choice.lower() == 'h':
            try:
                hit = player.deal(1)
                print(player.name + ' gets a(n)',hit)
                player.inPlay.add(hit)
                self.checkTotal(player)
            except:
                self.checkIfEliminated(player)
        elif choice.lower() == 's':
            player.result = 'stay'

    def checkForAce(self): # TODO Make ace count as 1 if player has one and busts
        pass

    def checkRoundWinner(self,skip):
        if skip == False:
            if len(self.blackjackList)==0:
                notBustList = [player for player in self.playerList if player not in self.bustsList]
                if len(notBustList)==1:
                    print('##########')
                    print(notBustList[0].name + ' has won this round.')
                    self.takeLoserCards(notBustList[0])
                else:
                    tempList = []
                    for player in notBustList:
                        if not tempList:
                            tempList.append(player)
                        elif tempList[0].handTotal>player.handTotal:
                            pass
                        elif tempList[0].handTotal<player.handTotal:
                            tempList = []
                            tempList.append(player)
                        elif tempList[0].handTotal==player.handTotal:
                            tempList.append(player)
                
                if len(tempList)==1:
                    print('##########')
                    print(tempList[0].name + ' has won this round.')
                    self.takeLoserCards(tempList[0])
                else:
                    self.warTiebreak(tempList)
            elif len(self.blackjackList)==1:
                print('##########')
                print(self.blackjackList[0].name + ' has won this round.')
                self.takeLoserCards(self.blackjackList[0])
            else:
                self.warTiebreak(self.blackjackList)
        elif skip == True:
            print('##########')
            print('The dealer has won by default.')
            self.takeLoserCards(self.dealer)

    def takeLoserCards(self,winner):
        winnerStack = pydealer.Stack()
        for player in self.playerList:
            winnerStack.add(player.inPlay.empty(return_cards=True))
        print(winner.name + ' has won',winnerStack.size,'cards.','\n'*2)
        winnerStack.shuffle()
        winner.add(winnerStack.empty(return_cards=True),end='bottom')

    def warTiebreak(self,tiebreakList): # TODO
        newTiebreakList = []
        for player in tiebreakList:
            try:
                player.inPlay.add(player.deal(1))
                player.handTotal = self.cardValues[player.inPlay.cards[0].value]
                print(player.name + ' has drawn a',player.inPlay.cards[0])
                if not newTiebreakList:
                    newTiebreakList.append(player)
                elif newTiebreakList[0].handTotal>player.handTotal:
                    pass
                elif newTiebreakList[0].handTotal<player.handTotal:
                    newTiebreakList = []
                    newTiebreakList.append(player)
                elif newTiebreakList[0].handTotal==player.handTotal:
                    newTiebreakList.append(player) 
            except:
                self.checkIfEliminated(player)
                tiebreakList.remove(player)
                continue
        if len(newTiebreakList)==1:
            print(tiebreakList[0].name + ' has won the tiebreak.')
            self.takeLoserCards(newTiebreakList[0])
        else:
            self.warTiebreak(newTiebreakList)

    def checkIfEliminated(self,player):	
        if player.size == 0:	
            player.eliminated = True	
            print(player.name + ' has been eliminated.','\n')		

    def deleteEliminated(self):	
        for player in self.playerList.copy():	
            if player.eliminated == True:	
                self.playerList.remove(player)	
        self.checkForGameWinner()

    def checkForGameWinner(self):
        if len(self.playerList) == 1:
            print(self.playerList[0].name + ' is the winner!','\n')
            exit()


BlackjackWarGame()
