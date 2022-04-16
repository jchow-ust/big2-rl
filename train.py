import os

from big2_rl.deep_mc import train, parser
from big2_rl.env.parse_game_settings import parse_game_settings

if __name__ == '__main__':
    # General Settings
    parser.add_argument('--xpid', default='big2rl',
                        help='Experiment id (default: big2rl)')
    parser.add_argument('--save_interval', default=10, type=int,
                        help='Time interval (in minutes) at which to save the model')
    parser.add_argument('--opponent_agent', default='random', type=str,
                        help='Type of opponent agent to be placed in other 3 positions \
                        which model will be tested again. Values = {prior, ppo}')

    # Training settings
    parser.add_argument('--actor_device_cpu', action='store_true',
                        help='Use CPU as actor device')
    parser.add_argument('--gpu_devices', default='0', type=str,
                        help='Which GPUs to be used for training')
    parser.add_argument('--num_actor_devices', default=1, type=int,
                        help='The number of devices used for simulation')
    parser.add_argument('--num_actors', default=5, type=int,
                        help='The number of actors for each simulation device')
    parser.add_argument('--training_device', default='0', type=str,
                        help='The index of the GPU used for training models. `cpu` means using cpu')
    parser.add_argument('--load_model', action='store_true',
                        help='Load an existing model')
    parser.add_argument('--disable_checkpoint', action='store_true',
                        help='Disable saving checkpoint')
    parser.add_argument('--savedir', default='big2rl_checkpoints',
                        help='Root dir where experiment data will be saved')

    # Hyperparameters
    parser.add_argument('--total_frames', default=100000000000, type=int,
                        help='Total environment frames to train for')
    parser.add_argument('--exp_epsilon', default=0.01, type=float,
                        help='The probability for exploration')
    parser.add_argument('--batch_size', default=32, type=int,
                        help='Learner batch size')
    parser.add_argument('--unroll_length', default=100, type=int,
                        help='The unroll length (time dimension)')
    parser.add_argument('--num_buffers', default=50, type=int,
                        help='Number of shared-memory buffers for a given actor device')
    parser.add_argument('--num_threads', default=4, type=int,
                        help='Number learner threads')
    parser.add_argument('--max_grad_norm', default=40., type=float,
                        help='Max norm of gradients')

    # Optimizer settings
    parser.add_argument('--learning_rate', default=0.0001, type=float,
                        help='Learning rate')
    parser.add_argument('--alpha', default=0.99, type=float,
                        help='RMSProp smoothing constant')
    parser.add_argument('--momentum', default=0, type=float,
                        help='RMSProp momentum')
    parser.add_argument('--epsilon', default=1e-5, type=float,
                        help='RMSProp epsilon')

    flags = parser.parse_args()

    # (re-)initialise game settings for training
    parse_game_settings(flags)

    os.environ["CUDA_VISIBLE_DEVICES"] = flags.gpu_devices
    train(flags)
