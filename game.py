import pydealer
import random

class BlackjackWarGame:
    def __init__(self):
        self.cardValues = {"Ace":11,"King":10,"Queen":10,"Jack":10,"10":10,
                            "9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
        self.playGame()
    
    def playGame(self): # Plays full game
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.dealCards()
        self.pickRandomDealer()
        while True: # Plays one round
            self.bustsList = []
            self.blackjackList = []        
            for player in self.playerList: # TODO Find better way to implement aces equaling both 11 and 1
                player.usedAces=0
            allBust = self.playRound()
            self.checkRoundWinner(allBust)
            
            self.printHandSizes()
            self.getNextDealer()
            self.deleteEliminated() # TODO Find better way to eliminate player
            self.getDealerIndex()
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
    
    def getNextDealer(self):
        self.dealerIndex+=1
        self.dealerIndex%=self.numOfPlayers
        if self.playerList[self.dealerIndex].eliminated==False:
            self.dealer=self.playerList[self.dealerIndex]
        else:
            self.getNextDealer()

    def getDealerIndex(self):
        self.dealerIndex=0
        for player in self.playerList:
            if self.playerList[self.dealerIndex].name != self.dealer.name:
                self.dealerIndex+=1 
            else:
                return

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
            self.checkIfEliminated(player)
            if player.eliminated==True:
                print(player.name + ' has been eliminated.','\n'*2)
                continue
            player.inPlay.add(player.deal(2))
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
            ace = self.checkForAce(player)
            if ace == False:
                print(player.name + ' has ' + str(player.handTotal) + ' and has busted.','\n')
                player.result = 'bust'
                self.bustsList.append(player)
            elif ace == True:
                player.result = 'continue'

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
            self.checkIfEliminated(player)
            if player.eliminated==True:
                print(player.name + ' has been eliminated.','\n'*2)
                return
            hit = player.deal(1)
            print(player.name + ' gets a(n)',hit,'\n')
            player.inPlay.add(hit)
            self.checkTotal(player)        
        elif choice.lower() == 's':
            player.result = 'stay'

    def checkForAce(self,player): # TODO Only count additional aces
        aceCount=0
        for card in player.inPlay.cards:
            if card.value=='Ace':
                aceCount+=1
        if aceCount>player.usedAces:
            player.usedAces+=1
            for ace in range(player.usedAces):
                player.handTotal-=10
            print(player.name + 'converted',player.usedAces,'ace(s) to 1 instead of 11.')
            print('Now ' + player.name + ' has a total of',player.handTotal,'\n')
            return True
        else:
            return False

    def checkRoundWinner(self,allBust):
        if allBust == False:
            if len(self.blackjackList)==0:
                notBustList = [player for player in self.playerList if player not in self.bustsList]
                tempList = []
                if len(notBustList)==1:
                    print('##########')
                    print(notBustList[0].name + ' has won this round.','\n')
                    self.takeLoserCards(notBustList[0])
                else:
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
                if tempList:
                    if len(tempList)==1:
                        print('##########')
                        print(tempList[0].name + ' has won this round.','\n')
                        self.takeLoserCards(tempList[0])
                    else:
                        self.warTiebreak(tempList)
            elif len(self.blackjackList)==1:
                print('##########')
                print(self.blackjackList[0].name + ' has won this round.','\n')
                self.takeLoserCards(self.blackjackList[0])
            else:
                self.warTiebreak(self.blackjackList)
        elif allBust == True:
            print('##########')
            print('The dealer has won by default.','\n')
            self.takeLoserCards(self.dealer)

    def takeLoserCards(self,winner):
        winnerStack = pydealer.Stack()
        for player in self.playerList:
            winnerStack.add(player.inPlay.empty(return_cards=True))
        print(winner.name + ' has won',winnerStack.size,'cards.','\n'*2)
        winnerStack.shuffle()
        winner.add(winnerStack.empty(return_cards=True),end='bottom')

    def warTiebreak(self,tiebreakList):
        print('##########')
        print('There is a tiebreak, as more than one player has',tiebreakList[0].handTotal)
        newTiebreakList = []
        for player in tiebreakList:
            self.checkIfEliminated(player)
            if player.eliminated==True:
                print(player.name + ' has been eliminated.','\n'*2)
                tiebreakList.remove(player)
                continue
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
        if len(newTiebreakList)==1:
            print(newTiebreakList[0].name + ' has won the tiebreak.')
            self.takeLoserCards(newTiebreakList[0])
        else:
            self.warTiebreak(newTiebreakList)

    def checkIfEliminated(self,player):	
        if player.size == 0:	
            player.eliminated = True	
            print(player.name + ' has been eliminated.','\n')		

    def deleteEliminated(self):	
        for player in self.playerList.copy():	
            if player.eliminated==True:	
                self.playerList.remove(player)	
        self.checkForGameWinner()

    def checkForGameWinner(self):
        if len(self.playerList) == 1:
            print(self.playerList[0].name + ' is the winner!','\n')
            exit()


BlackjackWarGame()
