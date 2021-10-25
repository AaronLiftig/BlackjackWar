import pydealer
from random import randint
from blackjack_war_state import BlackjackWarState
from blackjack_war_ai import BlackjackWarAI
from player import Player

class BlackjackWarGame(BlackjackWarState,BlackjackWarAI,Player):
    def __init__(self,number_of_players,number_of_humans,number_of_games=1):
        self.validate_number_of_games(number_of_games)
        self.validate_number_of_players(number_of_players)
        self.validate_number_of_humans(number_of_humans,number_of_players)

        print('This is like blackjack, but the winner')
        print('of a round wins the cards for that round.')
        print('The last player with cards remaining wins.')
        print()

        self.CARD_VALUES = {'Ace':11,'King':10,'Queen':10,'Jack':10,'10':10,
                            '9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}
        results_list = []
        self.number_of_humans = number_of_humans
        
        results_list = self.main_game_loop(number_of_games,number_of_players,results_list)

        print('The final score was:')
        for val in set(results_list):
            print(val+':',results_list.count(val))

    @staticmethod
    def validate_number_of_games(number_of_games):
        if not (isinstance(number_of_games,int) and number_of_games > 0):
            raise Exception('The number_of_games parameter must be a positive integer.')

    @staticmethod
    def validate_number_of_players(number_of_players):
        if number_of_players not in (2,4):
            raise Exception('The number_of_players parameter must be 2 or 4.')

    @staticmethod
    def validate_number_of_humans(number_of_humans,number_of_players):
        if (not isinstance(number_of_humans,int) 
            or number_of_humans > number_of_players 
            or number_of_humans < 0):
            raise Exception('The number_of_humans parameter must be an integer '                        'between 0 and number_of_players.')

    def main_game_loop(self,number_of_games,number_of_players,results_list):
        for game in range(1,number_of_games+1):
            if game % 50 == 0:
                print(game,'games played')
            self.number_of_players = number_of_players
            self.deck = pydealer.Deck()
            self.state_dict = self.create_state_dict(self.number_of_players,self.deck)
            winner = self.play_game()
            if not isinstance(winner,str):
                results_list.append(winner.name)
            else:
                self.print_if_human_playing(['All players were eliminated. No winner this round.'])
        return results_list

    def play_game(self):
        self.pregame_setup()
        while True:
            self.busts_list = []
            self.blackjack_list = []
            
            self.all_bust = self.play_round()
            
            for player in self.player_list:
                self.is_player_eliminated(player)
            winner = self.check_for_game_winner()
            if winner is not None:
                return winner

            self.check_round_winner()
            
            if self.is_there_a_human_player():
                self.print_hand_sizes()

            for player in self.player_list:
                self.state_dict = self.update_card_counts(self.state_dict,player)
                self.delete_eliminated(player)

            self.get_next_dealer()
            self.state_dict = self.update_dealer(self.state_dict,self.dealer)
            
            if self.is_there_a_human_player():
                input('Press enter to continue to next round.')
            self.print_if_human_playing(['######################################',
                                        self.dealer.name+' is the next dealer.'])

    def pregame_setup(self):
        self.deck.shuffle()
        self.player_list = self.deal_cards()
        self.winner_stack = pydealer.Stack()
        self.player_list = self.assign_ai(self.player_list,self.number_of_players,
                                            self.number_of_humans)
        self.dealer = self.pick_random_dealer()
        self.state_dict = self.update_dealer(self.state_dict,self.dealer)
        self.create_dealer_list()

    def deal_cards(self):
        if self.number_of_players == 2:
            player_list,player_names_list = self.two_player_setup()
        elif self.number_of_players == 4:
            player_list,player_names_list = self.four_player_setup()
        player_list = self.combine_setup_parts(player_list,player_names_list)
        return player_list

    def two_player_setup(self):
        player_1 = pydealer.Stack()
        player_1.add(self.deck.deal(26))
        player_2 = pydealer.Stack()
        player_2.add(self.deck.deal(26))
        player_list = [player_1,player_2]
        player_names_list = ['Player 1','Player 2']
        return player_list,player_names_list

    def four_player_setup(self):
        player_1 = pydealer.Stack()
        player_1.add(self.deck.deal(13))
        player_2 = pydealer.Stack()
        player_2.add(self.deck.deal(13))
        player_3 = pydealer.Stack()
        player_3.add(self.deck.deal(13))
        player_4 = pydealer.Stack()
        player_4.add(self.deck.deal(13))
        player_list = [player_1,player_2,player_3,player_4]
        player_names_list = ['Player 1','Player 2','Player 3','Player 4']
        return player_list,player_names_list

    def combine_setup_parts(self,player_list,player_names_list):
        for i, (player,name_string) in enumerate(zip(player_list,player_names_list)):
            player.name = name_string
            player.eliminated = False
            player.index = i
        return player_list

    def print_hand_sizes(self):
        print('The current hand sizes are now:')
        for player in self.player_list:      
            print(player.name + ':',player.size)
        print()

    def is_there_a_human_player(self):
        return any(player.is_human for player in self.player_list)

    def print_if_human_playing(self,statement_list):
        if self.is_there_a_human_player():
            for statement in statement_list:
                print(statement)
            print()

    def pick_random_dealer(self):
        dealer_index = randint(0,self.number_of_players-1)
        dealer = self.player_list[dealer_index]
        self.print_if_human_playing([dealer.name+' is the dealer to start.'])
        return dealer
    
    def create_dealer_list(self): # Makes finding next dealer easier
        temp_list = []
        counter=0
        for player in self.player_list:
            if player.name != self.dealer.name:
                counter+=1
            else:
                for player_index in range(counter,counter+self.number_of_players):
                    player_index %= self.number_of_players
                    temp_list.append(self.player_list[player_index])
                break
        self.player_list = temp_list

    def get_next_dealer(self):
        for player_index in range(1,self.number_of_players+1):
            player_index %= self.number_of_players
            player = self.player_list[player_index]
            if not player.eliminated:
                self.dealer = player
                self.create_dealer_list()
                return

    def play_round(self):
        self.start_hand()
        for player_index in range(1,self.number_of_players+1):
            if len(self.busts_list) == self.number_of_players-1:
                return True
            player_index %= self.number_of_players
            player = self.player_list[player_index]
            if player.eliminated:
                continue
            self.state_dict = self.update_turn(self.state_dict,player)
            while player.result == 'continue':
                player = self.get_choice(player)
                if player.eliminated:
                    break
        return False

    def start_hand(self):
        for player_index in range(1,self.number_of_players+1):
            player_index %= self.number_of_players
            player = self.player_list[player_index]
            player.in_play = pydealer.Stack()

            player,eliminated = self.is_player_eliminated(player)
            if eliminated:
                continue
                
            player.in_play.add(player.deal(2))
            self.print_if_human_playing(['##########',
                                        player.name+' is showing...',
                                        player.in_play])

            player = self.check_total(player)
            self.state_dict = self.update_hand_totals(self.state_dict,player)
            self.state_dict = self.update_card_state(self.state_dict,player)

    def check_total(self,player):
        player = self.get_sum(player)
        if player.hand_total < 21:
            player.result = self.check_for_5_cards(player)
        elif player.hand_total == 21:
            player = self.has_blackjack(player)
        else:
            player = self.over_21_sequence(player)
        return player

    def over_21_sequence(self,player):
        has_ace, player = self.check_for_ace(player)
        if not has_ace:
            self.player_busts(player)
        else:
            player = self.over_21_with_ace(player)
        return player

    def has_blackjack(self,player):
        self.print_if_human_playing([player.name+' has blackjack!'])
        player.result = 'blackjack'
        self.blackjack_list.append(player)
        return player

    def over_21_with_ace(self,player):
        if player.hand_total < 21:
            player.result = self.check_for_5_cards(player)
        elif player.hand_total == 21:
            self.print_if_human_playing([player.name+' has blackjack!'])
            player.result = 'blackjack'
            self.blackjack_list.append(player)
        elif player.hand_total > 21:
            self.player_bust(player)
        return player

    def player_busts(self,player):
        self.print_if_human_playing([player.name+' busted with '+str(player.hand_total)+'.'])
        player.result = 'bust'
        player.hand_total = 0
        self.busts_list.append(player)

    def get_sum(self,player,hand_total=0):
        for card in player.in_play.cards:
            hand_total += self.CARD_VALUES[card.value]
        player.hand_total = hand_total
        self.print_if_human_playing([player.name+' has '+str(player.hand_total)+'.'])
        return player

    def check_for_5_cards(self,player):
        if player.in_play.size < 5:
            return 'continue'
        elif player.in_play.size == 5:
            self.print_if_human_playing([player.name+' has 5 cards. Blackjack!'])
            self.blackjack_list.append(player)
            return 'blackjack'
        
    def get_choice(self,player):
        self.print_if_human_playing(['#####',
                                    'It is '+player.name +'\'s turn.',
                                    player.name+' is showing '+str(player.hand_total)+'.'])
        if not player.is_human:
            player = self.get_choice_if_not_human(player)
        else:
            player = self.get_choice_if_human(player)
        return player

    def get_choice_if_not_human(self,player):
        state = self.output_state(self.state_dict)
        player = self.game_ai(player,self.player_list,state)
        if player.result == 'hit':
            player = self.get_hit(player)
        return player

    def get_choice_if_human(self,player):
        print('The other hand sizes are',*[p.hand_total for p in self.player_list if p != player])
        print()
        choice = None
        while choice not in ('h','s'):
            choice = input('Would '+player.name+' like to hit? Enter h for hit or s for stay.\n')
        if choice == 'h':
            player = self.get_hit(player)        
        elif choice == 's':
            player.result = 'stay'
        return player

    def get_hit(self,player):
        player,eliminated = self.is_player_eliminated(player)
        if eliminated:
            return player
        hit_card = player.deal(1)
        self.print_if_human_playing([player.name+' gets a(n) '+hit_card[0].name])
        player.in_play.add(hit_card)
        player = self.check_total(player)
        self.state_dict = self.update_hand_totals(self.state_dict,player)
        self.state_dict = self.update_card_state(self.state_dict,player)
        return player

    def check_for_ace(self,player):
        ace_count=0
        for card in player.in_play.cards:
            if card.value=='Ace':
                ace_count,not_busted = self.deduct_ace(player,ace_count)
                if not_busted:
                    return True, player
        return False, player

    def deduct_ace(self,player,ace_count):
        player.hand_total-=10
        ace_count+=1
        if player.hand_total<=21:
            self.print_if_human_playing([player.name+' converted '+str(ace_count)+' ace(s) to 1.',
                                        'Now '+player.name+' has '+str(player.hand_total)+'.'])
            return ace_count,True
        return ace_count,False
            
    def check_round_winner(self):
        if not self.all_bust:
            self.get_winner_from_multiple_players()
        else:
            self.player_wins(self.dealer)

    def get_winner_from_multiple_players(self):
        if not self.blackjack_list:
            self.get_no_blackjacks_winner()
        elif len(self.blackjack_list) == 1:
            self.player_wins(self.blackjack_list[0])
        else:
            self.war_tiebreak(self.blackjack_list)

    def get_no_blackjacks_winner(self):
        not_bust_list = [player for player in self.player_list if player not in self.busts_list]
        if len(not_bust_list) == 1:
            self.player_wins(not_bust_list[0])
        else:
            self.multiple_players_not_busted(not_bust_list)

    def player_wins(self,player):
        self.print_if_human_playing(['##########',
                                    player.name+' has won this round.'])
        self.give_winner_stack(player)

    def multiple_players_not_busted(self,not_bust_list):
        tiebreak_list = []
        for player in not_bust_list:
            tiebreak_list = self.populate_tiebreak_list(player,tiebreak_list)
        if len(tiebreak_list) == 0:
            pass
        if len(tiebreak_list) == 1:
            self.player_wins(tiebreak_list[0])
        else:
            self.war_tiebreak(tiebreak_list)

    def populate_tiebreak_list(self,player,tiebreak_list):
        if not tiebreak_list:
            tiebreak_list.append(player)
        elif tiebreak_list[0].hand_total > player.hand_total:
            pass
        elif tiebreak_list[0].hand_total < player.hand_total:
            tiebreak_list = []
            tiebreak_list.append(player)
        elif tiebreak_list[0].hand_total == player.hand_total:
            tiebreak_list.append(player)
        return tiebreak_list

    def add_all_in_play_cards_to_winner_stack(self):
        for player in self.player_list:    
            self.winner_stack.add(player.in_play.empty(return_cards=True))
    
    def give_winner_stack(self,winner=None,all_eliminated=False):
        self.add_all_in_play_cards_to_winner_stack()
        if not all_eliminated:
            self.state_dict = self.update_winner(self.state_dict,winner)
            self.print_if_human_playing([winner.name+' has won '+str(self.winner_stack.size)+' cards.'])
            winner.add(self.winner_stack.empty(return_cards=True))
            winner.shuffle()
        else:
            for i, card in enumerate(self.winner_stack.cards):
                self.player_list[i % self.number_of_players].add(card)
                self.player_list[i % self.number_of_players].shuffle()

    def war_tiebreak(self,tiebreak_list,successive_tiebreaks=0):
        self.print_if_human_playing(['##########',
                                    'There is a tiebreak. '+str(len(tiebreak_list)),
                                    'players have '+str(tiebreak_list[0].hand_total)+'.'])
        new_tiebreak_list = []
        for player in tiebreak_list:
            player,eliminated = self.is_player_eliminated(player)
            if eliminated:
                continue
            player, new_tiebreak_list = self.new_tiebreak_list_process(player,new_tiebreak_list)
        if len(new_tiebreak_list) == 0:
            self.print_if_human_playing(['All players in tiebreak have been eliminated.'])
            self.give_winner_stack(all_eliminated=True)
        elif len(new_tiebreak_list) == 1:
            self.player_wins(new_tiebreak_list[0])
        else:
            self.war_tiebreak(new_tiebreak_list)

    def new_tiebreak_list_process(self,player,new_tiebreak_list):
        player.in_play.add(player.deal(1),end='bottom')
        player.hand_total = self.CARD_VALUES[player.in_play.cards[0].value]
        self.print_if_human_playing([player.name+' has drawn a '+player.in_play.cards[0].name])
        new_tiebreak_list = self.populate_tiebreak_list(player,new_tiebreak_list)
        return player, new_tiebreak_list
    
    def is_player_eliminated(self,player):	
        if player.size == 0:	
            player.eliminated = True
            self.state_dict = self.update_eliminated(self.state_dict,player)	
            self.print_if_human_playing([player.name+' has been eliminated.'])
            return player, True
        return player, False

    def delete_eliminated(self,player):
        if player.eliminated:	
            self.player_list.remove(player)
            self.number_of_players = len(self.player_list)	

    def check_for_game_winner(self):
        not_eliminated_list= [player for player in self.player_list if not player.eliminated]
        if len(not_eliminated_list) == 1:
            self.print_if_human_playing([self.not_eliminated_list[0].name+' is the winner!'])
            return not_eliminated_list[0]
        elif len(not_eliminated_list) == 0:
            return 'flag'
        else:
            return None



if __name__ == '__main__':
    BlackjackWarGame(number_of_players=4,number_of_humans=1,number_of_games=1)