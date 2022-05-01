import os
from big2_rl.evaluation.simulation import evaluate
from big2_rl.deep_mc.settings_parser_arguments import parser
from big2_rl.env.parse_game_settings import parse_settings

if __name__ == '__main__':
    # define which agents to place in which positions.
    # If we want we can replace south with random, others with DMC trained for instance, and evaluate performance
    parser.add_argument('--south', type=str, default='random')
    parser.add_argument('--east', type=str, default='random')
    parser.add_argument('--north', type=str, default='random')
    parser.add_argument('--west', type=str, default='random')

    parser.add_argument('--train_opponent', type=str, help='opponent during training')
    parser.add_argument('--eval_opponent', type=str, default='random', help='opponent during evaluation')
    parser.add_argument('--frames_trained', type=str, help='number of frames trained')

    parser.add_argument('--eval_data', type=str, default='eval_data.pkl')
    parser.add_argument('--num_workers', type=int, default=5)
    parser.add_argument('--gpu_device', type=str, default='')

    args = parser.parse_args()

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device

    if args.train_opponent == args.eval_opponent:
        raise ValueError('train_opponent and eval_opponent cannot be the same')

    agent_path = ''
    opponent = ''
    if args.train_opponent == 'ppo':
        agent_path = f'big2rl_checkpoints/big2rl/_weights_{args.frames_trained}.ckpt' # edit the number here
        # opponent = 'big2rl_checkpoints/prior-test/model.tar'
    elif args.train_opponent == 'prior':
        agent_path = f'big2rl_checkpoints/prior-test/_weights_{args.frames_trained}.ckpt' # edit the number here
    elif args.train_opponent == 'random':
        agent_path = f'big2rl_checkpoints/random/_weights_{args.frames_trained}.ckpt' # edit the number here
        opponent = 'big2rl_checkpoints/prior-test/model.tar'
    else:
        raise ValueError('Training opponent not specified')

    if args.eval_opponent == 'ppo':
        opponent = 'ppo'
    elif args.eval_opponent == 'prior':
        # pass path if it's prior DMC agent
        opponent_frames_trained = 1017600
        opponent = f'big2rl_checkpoints/prior-test/_weights_{opponent_frames_trained}.ckpt'
        # opponent = 'big2rl_checkpoints/prior-test/model.tar'
    elif args.eval_opponent == 'random':
        opponent = 'random'


    args.south = agent_path
    args.east = opponent
    args.north = opponent
    args.west = opponent

    print(f'Agent using {agent_path}, opponent using ')


    #args.south = 'big2rl_checkpoints/prior-test/model.tar'
    #args.south = 'big2rl_checkpoints/big2rl/model.tar'
    #args.south = 'ppo'
    #args.east = 'big2rl_checkpoints/big2rl/model.tar'
    #args.north = 'big2rl_checkpoints/big2rl/model.tar'
    #args.west = 'big2rl_checkpoints/big2rl/model.tar'
    #args.east = 'ppo'
    #args.north = 'ppo'
    #args.west = 'ppo'
    # if we make 4 PPOs play against each other, since policy is deterministic, so position will have EV 0

    print(args.eval_data)

    evaluate(args.south, args.east, args.north, args.west, args.eval_data, args.num_workers)
