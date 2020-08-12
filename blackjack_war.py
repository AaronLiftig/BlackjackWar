import pydealer
import random
from blackjack_war_state import BlackjackWarState
from blackjack_war_ai import BlackjackWarAI

class BlackjackWarGame(BlackjackWarState,BlackjackWarAI):
    def __init__(self,numOfPlayers=None,humanPlayerNum=-1,numOfGames=1,ask=True):
        cardValues = {'Ace':11,'King':10,'Queen':10,'Jack':10,'10':10,
                      '9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}

        resultList = []
        deck = pydealer.Deck()

        if ask not in (True,False):
            Exception('The ask parameter is a boolean value (True or False).')
        
        if not (isinstance(numOfGames,int) and numOfGames > 0):
            Exception('The numOfGames parameter must be a positive integer')

        if ask == True:
            while numOfPlayers not in (2,4):
                numOfPlayers = int(input('Would you like to play with 2 or 4 players? Enter 2 or 4 and press enter.\n'))
            while (not isinstance(humanPlayerNum,int))|(humanPlayerNum > numOfPlayers)|(humanPlayerNum < 0):
                humanPlayerNum = int(input('How many human players are there? Enter an integer.\n'))

            print('Human players are assigned first (e.g., If there are three human players, they will be players 1, 2, and 3.')
            print('The computer players currently hit on 16 and stay on 17 unless behind.','\n'*2)

            while True:
                stateDict = self.CreateStateDict(numOfPlayers,deck)
                winner = self.PlayGame(numOfPlayers,humanPlayerNum,cardValues,stateDict)
                resultList.append(winner.name)

                playAgain = None
                while playAgain not in ('y','n'):
                    playAgain = input('Would you like to play again? Enter y or n.\n').lower()
                if playAgain == 'n':
                    break
        else:
            for game in range(numOfGames):
                stateDict = self.CreateStateDict(numOfPlayers,deck)
                winner = self.PlayGame(numOfPlayers,humanPlayerNum,cardValues,stateDict)
                resultList.append(winner.name)

        print('The final score was:')
        for val in set(resultList):
            print(val+':',resultList.count(val))

    def PlayGame(self,numOfPlayers,humanPlayerNum,cardValues,stateDict): # Plays full game
        deck = pydealer.Deck()
        deck.shuffle()
        playerList = self.DealCards(deck,numOfPlayers)
        
        winnerStack = pydealer.Stack()

        self.CheckHumanNum(numOfPlayers,humanPlayerNum) # Added AI
        playerList = self.assignAI(playerList,numOfPlayers,humanPlayerNum)

        dealer = self.PickRandomDealer(playerList)
        stateDict = self.UpdateState(stateDict,dealer=dealer)
        playerList = self.CreateDealerList(playerList,dealer,numOfPlayers)
        while True: # Plays one round
            bustsList = []
            blackjackList = []
            
            allBust,playerList,blackjackList,bustsList,winnerStack,numOfPlayers = self.PlayRound(playerList,blackjackList,
                                                                                                 bustsList,dealer,
                                                                                                 numOfPlayers,winnerStack,
                                                                                                 cardValues,stateDict)
            playerList,blackjackList,bustsList,winnerStack = self.CheckRoundWinner(allBust,playerList,dealer,blackjackList,
                                                                                   bustsList,winnerStack,cardValues,
                                                                                   stateDict)
            
            self.PrintHandSizes(playerList)
            for player in playerList:
                stateDict = self.UpdateState(stateDict,player=player,updateCardCounts=True)
                player,winnerStack,stateDict = self.CheckIfEliminated(player,winnerStack,stateDict)
            playerList,dealer,numOfPlayers = self.GetNextDealer(playerList,numOfPlayers)
            stateDict = self.UpdateState(stateDict,dealer=dealer)
            playersRemaining = self.DeleteEliminated(playerList)
            if not isinstance(playersRemaining,list):
                return playersRemaining
            if any(player.human for player in playerList):
                input('Press enter to continue to next round.')
                print('######################################','\n'*2)
            print(dealer.name + ' is the next dealer.','\n')

    def DealCards(self,deck,numOfPlayers): # Just splits deck to deal, as cards are shuffled. Visual can deal one at a time.
        if numOfPlayers not in (2,4):
            raise Exception('numOfPlayers must be 2 or 4')
        if numOfPlayers == 2:
            Player1 = pydealer.Stack()
            Player1.add(deck.deal(26))
            Player2 = pydealer.Stack()
            Player2.add(deck.deal(26))
            playerList = [Player1,Player2]
            playerNamesList = ['Player 1','Player 2']
            playerNum = 0
            for player,nameString in zip(playerList,playerNamesList):
                player.name = nameString
                player.eliminated = False
                player.index = playerNum
                playerNum += 1
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
            playerNum = 0
            for player,nameString in zip(playerList,playerNames):
                player.name = nameString
                player.eliminated = False
                player.index = playerNum
                playerNum += 1
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
    
    def CreateDealerList(self,playerList,dealer,numOfPlayers): # So deleting players doesn't mess up finding next dealer
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

    def PlayRound(self,playerList,blackjackList,bustsList,dealer,numOfPlayers,winnerStack,cardValues,stateDict):
        numOfPlayers = len(playerList)
        playerList = self.StartHand(playerList,dealer,blackjackList,bustsList,numOfPlayers,winnerStack,cardValues,stateDict)
        for playerIndex in range(1,numOfPlayers+1):
            if len(bustsList)==numOfPlayers-1:
                return True,playerList,blackjackList,bustsList,winnerStack,numOfPlayers
            playerIndex %= numOfPlayers
            player = playerList[playerIndex]
            if player.eliminated == True:
                continue
            stateDict = self.UpdateState(stateDict,player=player,updateTurn=True)
            while player.result == 'continue':
                player,playerList,blackjackList,bustsList = self.GetChoice(player,playerList,dealer,blackjackList,bustsList,
                                                                           winnerStack,cardValues,stateDict)
                if player.eliminated == True:
                    break
        return False,playerList,blackjackList,bustsList,winnerStack,numOfPlayers

    def StartHand(self,playerList,dealer,blackjackList,bustsList,numOfPlayers,winnerStack,cardValues,stateDict):
        for playerIndex in range(1,numOfPlayers+1):
            playerIndex %= numOfPlayers
            player = playerList[playerIndex]
            player.inPlay = pydealer.Stack()
            player,winnerStack,stateDict = self.CheckIfEliminated(player,winnerStack,stateDict)
            if player.eliminated == True:
                continue
            player.inPlay.add(player.deal(2))
            stateDict = self.UpdateState(stateDict,player=player,updateCardState=True)
            
            print('##########')
            print(player.name + ' is showing...')
            print(player.inPlay,'\n')
            player,blackjackList,bustsList = self.CheckTotal(player,blackjackList,bustsList,cardValues)
            stateDict = self.UpdateState(stateDict,player=player,updateHandTotals=True,updateCardState=True)
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
                if player.handTotal < 21:
                    player.result == 'continue'
                elif player.handTotal == 21:
                    print(player.name + ' has blackjack!','\n')
                    player.result = 'blackjack'
                    blackjackList.append(player)
                elif player.handTotal > 21:
                    print(player.name + ' has ' + str(player.handTotal) + ' and has busted.','\n')
                    player.result = 'bust'
                    bustsList.append(player)      
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
        
    def GetChoice(self,player,playerList,dealer,blackjackList,bustsList,winnerStack,cardValues,stateDict):
        print('#####')
        print('It is ' + player.name +'\'s turn.')
        print(player.name + ' is showing a total of '+ str(player.handTotal) + '.')
        # TODO Create a dealer Stay-On-17 rule for all players 
        if player.human == False:
            state = self.OutputState(stateDict)
            player = self.GameAI(player,playerList,state)
            if player.result == 'hit':
                player,blackjackList,bustsList,winnerStack = self.GetHit(player,blackjackList,bustsList,winnerStack,
                                                                         cardValues,stateDict)
        elif player.human == True:
            choice = None
            while choice not in ('h','s'):
                choice = input('Would ' + player.name + ' like to hit? Enter h for hit or s for stay.\n')
            if choice.lower() == 'h':
                player,blackjackList,bustsList,winnerStack = self.GetHit(player,blackjackList,bustsList,winnerStack,
                                                                         cardValues,stateDict)        
            elif choice.lower() == 's':
                player.result = 'stay'
        return player,playerList,blackjackList,bustsList

    def GetHit(self,player,blackjackList,bustsList,winnerStack,cardValues,stateDict):
        player,winnerStack,stateDict = self.CheckIfEliminated(player,winnerStack,stateDict)
        if player.eliminated==True:
            print(player.name + ' has been eliminated.','\n'*2)
            return winnerStack
        hit = player.deal(1)
        print(player.name + ' gets a(n)',hit,'\n')
        player.inPlay.add(hit)
        player,blackjackList,bustsList = self.CheckTotal(player,blackjackList,bustsList,cardValues)
        stateDict = self.UpdateState(stateDict,player=player,updateHandTotals=True,updateCardState=True)
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

    def CheckRoundWinner(self,allBust,playerList,dealer,blackjackList,bustsList,winnerStack,cardValues,stateDict):
        if allBust == False:
            if len(blackjackList)==0:
                notBustList = [player for player in playerList if player not in bustsList]
                if len(notBustList)==1:
                    print('##########')
                    print(notBustList[0].name + ' has won this round.','\n')
                    playerList,winnerStack = self.TakeLoserCards(notBustList[0],playerList,winnerStack,stateDict)
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
                        playerList,winnerStack = self.TakeLoserCards(tempList[0],playerList,winnerStack,stateDict)
                    else:
                        playerList,winnerStack = self.WarTiebreak(playerList,tempList,winnerStack,cardValues,stateDict)
            elif len(blackjackList)==1:
                print('##########')
                print(blackjackList[0].name + ' has won this round.','\n')
                playerList,winnerStack = self.TakeLoserCards(blackjackList[0],playerList,winnerStack,stateDict)
            else:
                playerList,winnerStack = self.WarTiebreak(playerList,blackjackList,winnerStack,cardValues,stateDict)
        elif allBust == True:
            print('##########')
            print('The dealer has won by default.','\n')
            playerList,winnerStack = self.TakeLoserCards(dealer,playerList,winnerStack,stateDict)
        return playerList,blackjackList,bustsList,winnerStack

    def TakeLoserCards(self,winner,playerList,winnerStack,stateDict):
        stateDict = self.UpdateState(stateDict,winner=winner)
        for player in playerList:
            winnerStack.add(player.inPlay.empty(return_cards=True))
        print(winner.name + ' has won',winnerStack.size,'cards.','\n'*2)
        winner.add(winnerStack.empty(return_cards=True),end='bottom')
        winner.shuffle()
        return playerList,winnerStack

    def WarTiebreak(self,playerList,tiebreakList,winnerStack,cardValues,stateDict):
        print('##########')
        print('There is a tiebreak, as more than one player has',tiebreakList[0].handTotal)
        newTiebreakList = []
        for player in tiebreakList:
            player,winnerStack,stateDict = self.CheckIfEliminated(player,winnerStack,stateDict)
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
            playerList,winnerStack = self.TakeLoserCards(newTiebreakList[0],playerList,winnerStack,stateDict)
        else:
            playerList,winnerStack = self.WarTiebreak(playerList,newTiebreakList,winnerStack,cardValues,stateDict)
        return playerList,winnerStack

    def CheckIfEliminated(self,player,winnerStack,stateDict):	
        if player.size == 0:	
            player.eliminated = True
            stateDict = self.UpdateState(stateDict,player=player,updateEliminated=True)	
            print(player.name + ' has been eliminated.','\n')
            winnerStack.add(player.empty(return_cards=True))
            winnerStack.add(player.inPlay.empty(return_cards=True))
        return player,winnerStack,stateDict	

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

    
# BlackjackWarGame(numOfPlayers=None,humanPlayerNum=-1,numOfGames=1,ask=True)
# If ask == True: players will be prompted for numOfPlayers and humanPlayerNum and will be asked to play again.
BlackjackWarGame(numOfPlayers=4,humanPlayerNum=0,numOfGames=1,ask=False)
