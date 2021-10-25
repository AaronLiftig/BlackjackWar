class BlackjackWarAI:    
    def assign_ai(self,player_list,number_of_players,number_of_humans):
        for playerIndex in range(number_of_players):
            if playerIndex < number_of_humans:
                player_list[playerIndex].is_human = True
            else:
                player_list[playerIndex].is_human = False
        return player_list

    def game_ai(self,player,player_list,state):
        tempList = player_list.copy()
        tempList.remove(player)
        if all(player.hand_total >= other.hand_total for other in tempList):
            self.print_if_human_player_exists(player_list,'stay\n')
            player.result = 'stay'
        else:
            self.determine_ai_choice_if_not_winning(player,player_list)
        return player

    def determine_ai_choice_if_not_winning(self,player,player_list):
        if player.hand_total <= 16:
            if player.size >= 1:
                self.print_if_human_player_exists(player_list,'hit\n')
                player.result = 'hit'
            else:
                self.print_if_human_player_exists(player_list,'stay\n')
                player.result = 'stay'
        elif player.hand_total > 16:
            self.print_if_human_player_exists(player_list,'stay\n')
            player.result = 'stay'

    def print_if_human_player_exists(self,player_list,statement):
        if any(player.is_human for player in player_list):
            print(statement)

