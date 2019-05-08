from gym.envs.registration import register

register(
    id='BlockDude-v0',
    entry_point='gym_blockdude.envs:BlockDude',
)
register(
    id='BlockDude-Medium-v0',
    entry_point='gym_blockdude.envs:BlockDudeMed',
)
register(
    id='BlockDude-Hard-v0',
    entry_point='gym_blockdude.envs:BlockDudeHArd',
)
register(
    id='BlockDude-ExtraHard-v0',
    entry_point='gym_blockdude.envs:BlockDudeExtraHard',
)