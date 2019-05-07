from gym.envs.registration import register

register(
    id='BlockDude-v0',
    entry_point='gym_blockdude.envs:BlockDude',
)