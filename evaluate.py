import os
from big2_rl.evaluation.simulation import evaluate
from big2_rl.deep_mc.settings_parser_arguments import parser

if __name__ == '__main__':
    # define which agents to place in which positions.
    # If we want we can replace south with random, others with DMC trained for instance, and evaluate performance
    parser.add_argument('--south', type=str, default='random')
    parser.add_argument('--east', type=str, default='random')
    parser.add_argument('--north', type=str, default='random')
    parser.add_argument('--west', type=str, default='random')

    parser.add_argument('--eval_data', type=str, default='eval_data.pkl')
    parser.add_argument('--num_workers', type=int, default=5)
    parser.add_argument('--gpu_device', type=str, default='')
    parser.add_argument('--model_s', default='', help='Model architecture to use for south')
    parser.add_argument('--model_e', default='', help='Model architecture to use for east')
    parser.add_argument('--model_n', default='', help='Model architecture to use for north')
    parser.add_argument('--model_w', default='', help='Model architecture to use for west')

    args = parser.parse_args()

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_device

    # TODO remove
    # args.south = 'big2rl_checkpoints/prior-test/_weights_2451200.ckpt'  # should be .ckpt, can't be the tar file
    args.south = 'baselines/prior-model.tar'
    #args.south = 'big2rl_checkpoints/prior-test/model.tar'
    #args.south = 'big2rl_checkpoints/big2rl/model.tar'
    #args.south = 'ppo'
    #args.east = 'big2rl_checkpoints/big2rl/model.tar'
    #args.north = 'big2rl_checkpoints/big2rl/model.tar'
    #args.west = 'big2rl_checkpoints/big2rl/model.tar'
    #args.east = 'baselines/prior-model.tar'
    #args.north = 'baselines/prior-model.tar'
    #args.west = 'baselines/prior-model.tar'
    args.model_s = ''  # standard for now
    model_type = {'SOUTH': args.model_s, 'NORTH': args.model_n, 'EAST':args.model_e, 'WEST': args.model_w}
    args.east = 'ppo'
    args.north = 'ppo'
    args.west = 'ppo'
    # if we make 4 PPOs play against each other, since policy is deterministic, so position will have EV 0

    evaluate(args.south, args.east, args.north, args.west,
             args.eval_data,
             args.num_workers, model_type)
