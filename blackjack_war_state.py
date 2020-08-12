class BlackjackWarState:
    def CreateStateDict(self,numOfPlayers,deck):  
        if numOfPlayers == 2:
            stateDict = {'eliminated':[0,0],
                         'turn':[0], #binary
                         'dealer':[0], #binary
                         'hand totals':[0,0],
                         'card counts':[26,26]}
            playerList = [[0],[1]]
        
        elif numOfPlayers == 4:
            stateDict = {'eliminated':[0,0,0,0],
                         'turn':[0,0], #binary
                         'dealer':[0,0], #binary
                         'hand totals':[0,0,0,0],
                         'card counts':[13,13,13,13]} 
            playerList = [[0,0],[0,1],[1,0],[1,1]]
        
        cardStateList = [0 for _ in range(int(numOfPlayers/2)+2)]
        cardDict = {}

        for card in deck.cards:
            cardDict.update({card.abbrev:cardStateList.copy()})

        stateDict.update({'card state':cardDict,
                          'player list':playerList})
        return stateDict
    
    def UpdateState(self,stateDict,player=None,dealer=None,updateEliminated=False,updateTurn=False,updateHandTotals=False,
                    updateCardCounts=False,updateCardState=False,winner=None):
        pList = stateDict['player list']
        
        if updateEliminated == True:
            if player.eliminated == True:
                stateDict['eliminated'][player.index] = 1
            #self.PrintStateDict(stateDict,1)

        if updateTurn == True:
            stateDict['turn'] = pList[player.index]
            #self.PrintStateDict(stateDict,2)
        
        if dealer is not None:
            stateDict['dealer'] = pList[dealer.index]
            #self.PrintStateDict(stateDict,3)

        if updateHandTotals == True:
            stateDict['hand totals'][player.index] = player.handTotal
            #self.PrintStateDict(stateDict,4)

        if updateCardCounts == True:
            stateDict['card counts'][player.index] = player.size
            #self.PrintStateDict(stateDict,5)

        if updateCardState == True:      
            for card in player.inPlay.cards:
                stateDict['card state'][card.abbrev][0] = 1 # Marks whether cards location is known
                for i in range(len(pList[player.index])): # Assigns card to player
                    stateDict['card state'][card.abbrev][i+1] = pList[player.index][i]
                stateDict['card state'][card.abbrev][len(pList[player.index])+1] = 1 # Marks as in play
            #self.PrintStateDict(stateDict,6)

        if winner is not None:
            for card in stateDict['card state'].keys():
                if stateDict['card state'][card][len(pList[winner.index])+1] == 1: # Gives in play cards to winner
                    for i in range(len(pList[winner.index])):
                        stateDict['card state'][card][i+1] = pList[winner.index][i]
                    stateDict['card state'][card][len(pList[winner.index])+1] = 0 # Removes cards from being in play
            
            if len(stateDict['hand totals']) == 2: # Resets handTotal after there's a round winner
                stateDict['hand totals'] = [0,0]
            elif len(stateDict['hand totals']) == 4:
                stateDict['hand totals'] = [0,0,0,0]
            #self.PrintStateDict(stateDict,7)
        return stateDict       

    def PrintStateDict(self,stateDict,num):
        print(num)
        for key in stateDict.keys():
            print(key+':',stateDict[key],'\n')

    def OutputState(self,stateDict):
        state = [] # state size: 2 player = 164; 4 player = 224
        for key in stateDict.keys():
            if key == 'player list':
                continue
            elif key != 'card state':
                for val in stateDict[key]:
                    state.append(val)
            else:
                for card in stateDict[key].keys():
                    for val in stateDict[key][card]:
                        state.append(val)
        #print(state)
        return state
