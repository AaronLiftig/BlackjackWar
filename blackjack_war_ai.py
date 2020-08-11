class BlackjackWarAI:    
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

    def GameAI(self,player,playerList,state):
        tempList = playerList.copy()
        tempList.remove(player)
        if all(player.handTotal >= other.handTotal for other in tempList):
            print('stay\n')
            player.result = 'stay'
        else:
            if player.handTotal <= 16:
                if player.size >= 1:
                    print('hit\n')
                    player.result = 'hit'
                else:
                    print('stay\n')
                    player.result = 'stay'
            elif player.handTotal > 16:
                print('stay\n')
                player.result = 'stay'
        return player
