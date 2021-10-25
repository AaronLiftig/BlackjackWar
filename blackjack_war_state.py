class BlackjackWarState:
    def create_state_dict(self,number_of_players,deck):  
        if number_of_players == 2:
            state_dict = {'eliminated':[0,0],
                         'turn':[0], #binary
                         'dealer':[0], #binary
                         'hand totals':[0,0],
                         'card counts':[26,26]}
            player_reference = [[0],[1]]
        elif number_of_players == 4:
            state_dict = {'eliminated':[0,0,0,0],
                         'turn':[0,0], #binary
                         'dealer':[0,0], #binary
                         'hand totals':[0,0,0,0],
                         'card counts':[13,13,13,13]} 
            player_reference = [[0,0],[0,1],[1,0],[1,1]]
        
        card_state_list = [0 for _ in range(int(number_of_players/2)+2)]
        card_dict = {}

        for card in deck.cards:
            card_dict.update({card.abbrev:card_state_list.copy()})
        state_dict.update({'card state':card_dict,
                          'player list':player_reference})
        return state_dict

    def update_eliminated(self,state_dict,player,print_state=False):
        if player.eliminated == True:
            state_dict['eliminated'][player.index] = 1
        if print_state:
            self.print_state_dict(state_dict,1)
        return state_dict

    def update_turn(self,state_dict,player,print_state=False):
        player_reference = state_dict['player list']
        state_dict['turn'] = player_reference[player.index]
        if print_state:
            self.print_state_dict(state_dict,2)
        return state_dict
    
    def update_dealer(self,state_dict,dealer,print_state=False):
        player_reference = state_dict['player list']
        state_dict['dealer'] = player_reference[dealer.index]
        if print_state:
            self.print_state_dict(state_dict,3)
        return state_dict

    def update_hand_totals(self,state_dict,player,print_state=False):
        state_dict['hand totals'][player.index] = player.hand_total
        if print_state:
            self.print_state_dict(state_dict,4)
        return state_dict

    def update_card_counts(self,state_dict,player,print_state=False):
        state_dict['card counts'][player.index] = player.size
        if print_state:
            self.print_state_dict(state_dict,5)
        return state_dict

    def update_card_state(self,state_dict,player,print_state=False): 
        player_reference = state_dict['player list']     
        for card in player.in_play.cards:
            self.mark_card_location_known(card,state_dict)
            for i in range(len(player_reference[player.index])):
                self.assign_card_to_player(i,card,state_dict,player,player_reference)
            self.mark_card_as_in_play(card,state_dict,player,player_reference)
        if print_state:
            self.print_state_dict(state_dict,6)
        return state_dict

    def mark_card_location_known(self,card,state_dict):
        state_dict['card state'][card.abbrev][0] = 1

    def assign_card_to_player(self,i,card,state_dict,player,player_reference):
        state_dict['card state'][card.abbrev][i+1] = player_reference[player.index][i]

    def mark_card_as_in_play(self,card,state_dict,player,player_reference):
        state_dict['card state'][card.abbrev][len(player_reference[player.index])+1] = 1

    def update_winner(self,state_dict,winner,print_state=False):
        player_reference = state_dict['player list']
        for card in state_dict['card state'].keys():
            if self.card_is_in_play(card,state_dict,winner,player_reference): 
                self.give_card_to_winner(card,state_dict,winner,player_reference)
                self.mark_card_as_out_of_play(card,state_dict,winner,player_reference) 
        self.reset_hand_totals(state_dict)
        if print_state:
            self.print_state_dict(state_dict,7)
        return state_dict

    def card_is_in_play(self,card,state_dict,winner,player_reference):
        return state_dict['card state'][card][len(player_reference[winner.index])+1] == 1

    def mark_card_as_out_of_play(self,card,state_dict,winner,player_reference):
        state_dict['card state'][card][len(player_reference[winner.index])+1] = 0

    def give_card_to_winner(self,card,state_dict,winner,player_reference):
        for i in range(len(player_reference[winner.index])):
            state_dict['card state'][card][i+1] = player_reference[winner.index][i]

    def reset_hand_totals(self,state_dict):
        if len(state_dict['hand totals']) == 2: 
            state_dict['hand totals'] = [0,0]
        elif len(state_dict['hand totals']) == 4:
            state_dict['hand totals'] = [0,0,0,0]

    def print_state_dict(self,state_dict,num):
        print(num)
        for key in state_dict.keys():
            print(key+':',state_dict[key],'\n')

    def output_state(self,state_dict):
        state = [] # state size: 2 player = 164; 4 player = 224
        for key in state_dict.keys():
            if key == 'player list':
                continue
            elif key != 'card state':
                for val in state_dict[key]:
                    state.append(val)
            else:
                for card in state_dict[key].keys():
                    for val in state_dict[key][card]:
                        state.append(val)
        return state