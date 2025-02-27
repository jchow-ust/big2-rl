from big2_rl.env.game import GameEnv, Position
from big2_rl.env.env import DummyAgent
from big2_rl.evaluation.simulation import load_models
from big2_rl.deep_mc.utils import string_to_hand, hand_to_string
import numpy as np


def play_against(args):
    """
    Loads models at their respective positions according to args, creates a random deal and initializes GameEnv
    Then allows player to play a game
    """
    card_play_model_path_dict = {'SOUTH': 'random',
                                 'EAST': args.east,
                                 'NORTH': args.north,
                                 'WEST': args.west}
    players = load_models(card_play_model_path_dict, 'standard')  # update missing argument here 19-07-2022
    oracle = players['EAST']
    env = GameEnv(players)
    env.players['SOUTH'] = DummyAgent(env.game_infoset)  # replace agent
    deck = [i for i in range(0, 52)]
    while True:
        # randomly deal cards
        print("Dealing new hand...")
        _deck = deck.copy()
        np.random.shuffle(_deck)
        card_play_data = {p.name: 0 for p in Position}
        for p in Position:
            card_play_data[p.name] = _deck[p.value * 13: (p.value + 1) * 13]
            card_play_data[p.name].sort()
        # initialise game environment with that deal
        env.card_play_init(card_play_data)
        print("Hand dealt!")
        for p in Position:  # set starting hand for PPO Agents
            if env.players[p.name].__class__.__name__ == 'PPOAgent':
                env.players[p.name].set_starting_hand(card_play_data[p.name])
        while env.game_over is not True:
            if env.acting_player_position == 'SOUTH':
                is_valid_move = False
                hand = env.game_infoset.player_hand_cards
                most_recent_moves = '| '
                opponent_cards_remaining = '| '
                for p in Position:
                    most_recent_moves += "{}: {} | ".format(p.name, hand_to_string(env.last_move_dict[p.name]))
                    opponent_cards_remaining += "{}: {} | ".format(p.name, env.game_infoset.num_cards_left_dict[p.name])
                while is_valid_move is False:
                    print("====================")
                    print("Most recent moves:")
                    print(most_recent_moves)
                    print("Number of cards remaining:")
                    print(opponent_cards_remaining)
                    print("Your hand: {}".format(hand_to_string(hand)))
                    move = input("Enter the move to make:\n")  # eg '3d,3h' for the pair (3 of diamonds, 3 of hearts)
                    try:
                        if move == 'rec':  # have agent recommend a move for us
                            if oracle.__class__.__name__ == 'PPOAgent':
                                # PPOAgent only supports top-1 move for now
                                rec_move = oracle.act(env.game_infoset, env.card_play_action_seq)
                                print("Recommended move: {}" .format(hand_to_string(rec_move)))
                            else:
                                rec_moves = oracle.recommend(env.game_infoset)
                                rec_moves_str = '| '
                                for action, value in rec_moves:
                                    if value == 'N/A':
                                        rec_moves_str += '{} - value {} | '.format(
                                            hand_to_string(env.game_infoset.legal_actions[action]), value)
                                    else:
                                        rec_moves_str += '{} - value {:.4f} | ' .format(
                                            hand_to_string(env.game_infoset.legal_actions[action]), value)
                                print("Recommended moves: {}" .format(rec_moves_str))
                            h_move = 'not a move lol'
                        else:  # convert move
                            h_move = string_to_hand(move)
                    except ValueError:  # can't convert to move
                        print("Invalid move.")

                    if h_move in env.game_infoset.legal_actions:
                        is_valid_move = True
                        players['SOUTH'].action = h_move
                    else:
                        if move != 'rec':
                            print("Can't beat last move.")
            else:
                pass
            env.step()  # invoke Agent.act()
        # once game ends, print amount won by each player
        scores = '| '
        totals = '| '
        for p in Position:
            scores += "{} won {} | " .format(p.name, env.player_reward_dict[p.name])
            totals += "{} has total {} | ".format(p.name, env.num_scores[p.name])
        print(scores)
        print(totals)
        env.reset()
