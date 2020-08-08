import pydealer
import random

class BlackjackWarGame:
    def __init__(self,numOfPlayers,humanPlayerNum,numOfGames=1):
        cardValues = {"Ace":11,"King":10,"Queen":10,"Jack":10,"10":10,
                      "9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2}
        
        resultList = []

        for game in range(numOfGames):
            winner = self.PlayGame(numOfPlayers,humanPlayerNum,cardValues)
            resultList.append(winner.name)
        
        for val in set(resultList):
            print(val+':',resultList.count(val))

    def PlayGame(self,numOfPlayers,humanPlayerNum,cardValues): # Plays full game
        deck = pydealer.Deck()
        deck.shuffle()
        playerList = self.DealCards(deck,numOfPlayers)
        
        winnerStack = pydealer.Stack()

        self.CheckHumanNum(numOfPlayers,humanPlayerNum) # Added AI
        playerList = self.assignAI(playerList,numOfPlayers,humanPlayerNum)

        dealer = self.PickRandomDealer(playerList)
        playerList = self.CreateDealerList(playerList,dealer,numOfPlayers)
        while True: # Plays one round
            bustsList = []
            blackjackList = []
            
            allBust,playerList,blackjackList,bustsList,winnerStack,numOfPlayers = self.PlayRound(playerList,blackjackList,bustsList,dealer,
                                                                                                 numOfPlayers,winnerStack,cardValues)
            playerList,blackjackList,bustsList,winnerStack = self.CheckRoundWinner(allBust,playerList,dealer,blackjackList,bustsList,
                                                                                   winnerStack,cardValues)
            
            self.PrintHandSizes(playerList)
            for player in playerList:
                player,winnerStack = self.CheckIfEliminated(player,winnerStack)
            playerList,dealer,numOfPlayers = self.GetNextDealer(playerList,numOfPlayers)
            playersRemaining = self.DeleteEliminated(playerList)
            if not isinstance(playersRemaining,list):
                return playersRemaining
            if any(player.human for player in playerList):
                input('Press enter to continue to next round.')
                print('######################################','\n'*2)
            print(dealer.name + ' is the next dealer.','\n')

    def DealCards(self,deck,numOfPlayers): # Just splits deck to deal, as cards are shuffled. Actual visual can deal one at a time.
        if numOfPlayers not in (2,4):
            raise Exception('numOfPlayers must be 2 or 4')
        if numOfPlayers == 2:
            Player1 = pydealer.Stack()
            Player1.add(deck.deal(26))
            Player2 = pydealer.Stack()
            Player2.add(deck.deal(26))
            playerList = [Player1,Player2]
            playerNamesList = ['Player 1','Player 2']
            for player,nameString in zip(playerList,playerNamesList):
                player.name = nameString
                player.eliminated = False
        elif numOfPlayers == 4:
            Player1 = pydealer.Stack()
            Player1.add(deck.deal(13))
            Player2 = pydealer.Stack()
            Player2.add(deck.deal(13))
            Player3 = pydealer.Stack()
            Player3.add(deck.deal(13))
            Player4 = pydealer.Stack()
            Player4.add(deck.deal(13))
            playerList = [Player1,Player2,Player3,Player4]
            playerNames = ['Player 1','Player 2','Player 3','Player 4']
            for player,nameString in zip(playerList,playerNames):
                player.name = nameString
                player.eliminated = False
        return playerList

    def PrintHandSizes(self,playerList):
        print('The current hand sizes are now:')
        for player in playerList:      
            print(player.name + ':',player.size)
        print('\n'*2)

    def PickRandomDealer(self,playerList):
        dealerIndex = random.randint(0,len(playerList)-1)
        dealer = playerList[dealerIndex]
        print(dealer.name + ' is the dealer to start.','\n')
        return dealer
    
    def CreateDealerList(self,playerList,dealer,numOfPlayers): # Done so that deleting players doesn't mess up finding next dealer
        tempList = []
        counter=0
        for player in playerList:
            if player.name != dealer.name:
                counter+=1
            else:
                for playerIndex in range(counter,counter+len(playerList)):
                    playerIndex %= numOfPlayers
                    tempList.append(playerList[playerIndex])
        playerList = tempList
        return playerList

    def GetNextDealer(self,playerList,numOfPlayers):
        for playerIndex in range(1,numOfPlayers+1):
            playerIndex %= numOfPlayers
            player = playerList[playerIndex]
            if player.eliminated==False:
                dealer = player
                playerList = self.CreateDealerList(playerList,dealer,numOfPlayers)
                return playerList,dealer,numOfPlayers

    def PlayRound(self,playerList,blackjackList,bustsList,dealer,numOfPlayers,winnerStack,cardValues):
        numOfPlayers = len(playerList)
        playerList = self.StartHand(playerList,dealer,blackjackList,bustsList,numOfPlayers,winnerStack,cardValues)
        for playerIndex in range(1,numOfPlayers+1):
            if len(bustsList)==numOfPlayers-1:
                return True,playerList,blackjackList,bustsList,winnerStack,numOfPlayers
            playerIndex %= numOfPlayers
            player = playerList[playerIndex]
            if player.eliminated == True:
                continue
            while player.result == 'continue':
                player,playerList,blackjackList,bustsList = self.GetChoice(player,playerList,dealer,blackjackList,bustsList,winnerStack,
                                                                           cardValues)
                if player.eliminated == True:
                    break
        return False,playerList,blackjackList,bustsList,winnerStack,numOfPlayers

    def StartHand(self,playerList,dealer,blackjackList,bustsList,numOfPlayers,winnerStack,cardValues):
        for playerIndex in range(1,numOfPlayers+1):
            playerIndex %= numOfPlayers
            player = playerList[playerIndex]
            player.inPlay = pydealer.Stack()
            player,winnerStack = self.CheckIfEliminated(player,winnerStack)
            if player.eliminated == True:
                continue
            player.inPlay.add(player.deal(2))
            if dealer.name != player.name:
                print('##########')
                print(player.name + ' is showing...')
                print(player.inPlay,'\n')
                player,blackjackList,bustsList = self.CheckTotal(player,blackjackList,bustsList,cardValues)
            elif dealer.name == player.name:
                print('##########')
                print(player.name + ', the dealer, is showing...')           
                print(player.inPlay,'\n')
                player,blackjackList,bustsList = self.CheckTotal(player,blackjackList,bustsList,cardValues) 
        return playerList 

    def CheckTotal(self,player,blackjackList,bustsList,cardValues):
        player = self.GetSum(player,cardValues)
        if player.handTotal < 21:
            player.result,blackjackList = self.CheckFor5Cards(player,blackjackList)
        elif player.handTotal == 21:
            print(player.name + ' has blackjack!','\n')
            player.result = 'blackjack'
            blackjackList.append(player)
        elif player.handTotal > 21:
            ace,player = self.CheckForAce(player)
            if ace == False:
                print(player.name + ' has ' + str(player.handTotal) + ' and has busted.','\n')
                player.result = 'bust'
                bustsList.append(player)
            elif ace == True:
                player.result = 'continue'
        return player,blackjackList,bustsList

    def GetSum(self,player,cardValues,handTotal=0): # TODO implement sum that adds last hit instead of counting whole hand
        for card in player.inPlay.cards:
            handTotal += cardValues[card.value]
        player.handTotal = handTotal
        print(player.name + ' has a total of',player.handTotal,'\n')
        return player

    def CheckFor5Cards(self,player,blackjackList):
        if player.inPlay.size < 5:
            return 'continue',blackjackList
        elif player.inPlay.size == 5:
            print(player.name + ' has 5 cards. Blackjack!','\n')
            blackjackList.append(player)
            return 'blackjack',blackjackList
        
    def GetChoice(self,player,playerList,dealer,blackjackList,bustsList,winnerStack,cardValues):
        print('#####')
        print('It is ' + player.name +'\'s turn.')
        print(player.name + ' is showing a total of '+ str(player.handTotal) + '.')
        # TODO Create a dealer Stay-On-17 rule for all players 
        if player.human == False:
            player,playerList,blackjackList,bustsList,winnerStack = self.GameAI(player,playerList,dealer,blackjackList,bustsList,winnerStack,
                                                                                cardValues)
        elif player.human == True:
            choice = None
            while choice not in ('h','s'):
                choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.\n')
            if choice.lower() == 'h':
                player,blackjackList,bustsList,winnerStack = self.GetHit(player,blackjackList,bustsList,winnerStack,cardValues)        
            elif choice.lower() == 's':
                player.result = 'stay'
        return player,playerList,blackjackList,bustsList

    def GetHit(self,player,blackjackList,bustsList,winnerStack,cardValues):
        player,winnerStack = self.CheckIfEliminated(player,winnerStack)
        if player.eliminated==True:
            print(player.name + ' has been eliminated.','\n'*2)
            return winnerStack
        hit = player.deal(1)
        print(player.name + ' gets a(n)',hit,'\n')
        player.inPlay.add(hit)
        player,blackjackList,bustsList = self.CheckTotal(player,blackjackList,bustsList,cardValues)
        return player,blackjackList,bustsList,winnerStack

    def CheckForAce(self,player): # TODO Only count additional aces
        aceCount=0
        for card in player.inPlay.cards:
            if card.value=='Ace':
                player.handTotal-=10
                aceCount+=1
                if player.handTotal<=21:
                    print(player.name + ' converted',aceCount,'ace(s) to 1 instead of 11.')
                    print('Now ' + player.name + ' has a total of',player.handTotal,'\n')
                    return True,player
        return False,player

    def CheckRoundWinner(self,allBust,playerList,dealer,blackjackList,bustsList,winnerStack,cardValues):
        if allBust == False:
            if len(blackjackList)==0:
                notBustList = [player for player in playerList if player not in bustsList]
                if len(notBustList)==1:
                    print('##########')
                    print(notBustList[0].name + ' has won this round.','\n')
                    playerList,winnerStack = self.TakeLoserCards(notBustList[0],playerList,winnerStack)
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
                        print(tempList[0].name + ' has won this round.','\n')
                        playerList,winnerStack = self.TakeLoserCards(tempList[0],playerList,winnerStack)
                    else:
                        playerList,winnerStack = self.WarTiebreak(playerList,tempList,winnerStack,cardValues)
            elif len(blackjackList)==1:
                print('##########')
                print(blackjackList[0].name + ' has won this round.','\n')
                playerList,winnerStack = self.TakeLoserCards(blackjackList[0],playerList,winnerStack)
            else:
                playerList,winnerStack = self.WarTiebreak(playerList,blackjackList,winnerStack,cardValues)
        elif allBust == True:
            print('##########')
            print('The dealer has won by default.','\n')
            playerList,winnerStack = self.TakeLoserCards(dealer,playerList,winnerStack)
        return playerList,blackjackList,bustsList,winnerStack

    def TakeLoserCards(self,winner,playerList,winnerStack):
        for player in playerList:
            winnerStack.add(player.inPlay.empty(return_cards=True))
        print(winner.name + ' has won',winnerStack.size,'cards.','\n'*2)
        winner.add(winnerStack.empty(return_cards=True),end='bottom')
        winner.shuffle()
        return playerList,winnerStack

    def WarTiebreak(self,playerList,tiebreakList,winnerStack,cardValues):
        print('##########')
        print('There is a tiebreak, as more than one player has',tiebreakList[0].handTotal)
        newTiebreakList = []
        for player in tiebreakList:
            player,winnerStack = self.CheckIfEliminated(player,winnerStack)
            if player.eliminated==True:
                continue
            player.inPlay.add(player.deal(1),end='bottom')
            player.handTotal = cardValues[player.inPlay.cards[0].value]
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
            playerList,winnerStack = self.TakeLoserCards(newTiebreakList[0],playerList,winnerStack)
        else:
            playerList,winnerStack = self.WarTiebreak(playerList,newTiebreakList,winnerStack,cardValues)
        return playerList,winnerStack

    def CheckIfEliminated(self,player,winnerStack):	
        if player.size == 0:	
            player.eliminated = True	
            print(player.name + ' has been eliminated.','\n')
            winnerStack.add(player.empty(return_cards=True))
            winnerStack.add(player.inPlay.empty(return_cards=True))
        return player,winnerStack	

    def DeleteEliminated(self,playerList):	
        for player in playerList:
            if player.eliminated == True:
                playerList.remove(player)	
                winner = self.CheckForGameWinner(playerList)
                if winner is not None:
                    return winner
        return playerList

    def CheckForGameWinner(self,playerList):
        if len(playerList) == 1:
            print(playerList[0].name + ' is the winner!','\n')
            return playerList[0]
        return None

    # AI methods start here:
    
    def CheckHumanNum(self,numOfPlayers,humanPlayerNum):
        if (not isinstance(humanPlayerNum,int))|(humanPlayerNum > numOfPlayers)|(humanPlayerNum < 0):
            raise Exception('Enter correct humanPlayerNum')

    def assignAI(self,playerList,numOfPlayers,humanPlayerNum):
        for playerIndex in range(numOfPlayers):
            if playerIndex < humanPlayerNum:
                playerList[playerIndex].human = True
            else:
                playerList[playerIndex].human = False
        return playerList

    def GameAI(self,player,playerList,dealer,blackjackList,bustsList,winnerStack,cardValues):      
        if player.name != dealer.name:
            player,playerList,blackjackList,bustsList,winnerStack = self.DealerAI(player,playerList,blackjackList,bustsList,winnerStack,
                                                                                  cardValues) # TODO
        elif player.name == dealer.name:
            player,playerList,blackjackList,bustsList,winnerStack = self.DealerAI(player,playerList,blackjackList,bustsList,winnerStack,
                                                                                  cardValues)
        return player,playerList,blackjackList,bustsList,winnerStack

    def DealerAI(self,player,playerList,blackjackList,bustsList,winnerStack,cardValues):
        tempList = playerList.copy()
        tempList.remove(player)
        if all(player.handTotal >= other.handTotal for other in tempList):
            print('stay\n')
            player.result = 'stay'
        else:
            if player.handTotal <= 16:
                if player.size >= 1:
                    print('hit\n')
                    player,blackjackList,bustsList,winnerStack = self.GetHit(player,blackjackList,bustsList,winnerStack,cardValues) # TODO
                else:
                    print('stay\n')
                    player.result = 'stay'
            elif player.handTotal > 16:
                print('stay\n')
                player.result = 'stay'
        return player,playerList,blackjackList,bustsList,winnerStack

    def OutputState(self,playerList):
        for player in playerList:
            #name
            #size
            #handTotal
            #inPlay.cards
            #cards "known" accumulated inPlay.cards by winner
            #eliminated
            pass


BlackjackWarGame(4,0,1)
