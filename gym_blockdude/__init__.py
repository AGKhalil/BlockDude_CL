from gym.envs.registration import register

register(
    id='blockdude-v0',
    entry_point='gym_blockdude.envs:BlockDudeEnv',
)