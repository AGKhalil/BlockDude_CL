import sys
import os

subdir_path = os.path.dirname(os.path.realpath(__file__)) + '/block_dude'
sys.path.insert(0, subdir_path)

import pygame
from player import Player
from component import Component
import numpy as np
import gym
from gym import error, utils
from gym.utils import seeding
from gym.spaces import Discrete, Box
from gym.envs.classic_control import rendering


class BlockDude(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self):

        pygame.init()

        self.play_on = True
        self.carry = False
        self.carried_bloc = -1

        self.screen_width = 432
        self.screen_height = 288

        # pygame.display.set_caption("Block Dude")
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        self.vel = 24

        self.x_player_init = [24]
        self.y_player_init = [264 - self.vel]
        # self.x_blocks_init = [264, 144, 120, 144]
        # self.y_blocks_init = [264 - 24] * 3 + [216]
        self.x_blocks_init = []
        self.y_blocks_init = []

        self.player = Player(self.screen, self.x_player_init,
                             self.y_player_init, self.vel, self.vel)

        self.brick_bottom_x = [
            i * self.vel for i in range(int(self.screen_width / self.vel))]
        self.brick_bottom_y = [self.screen_height -
                               self.vel for i in range(len(self.brick_bottom_x))]

        # self.brick_bottom_x += [192, 168, 192]
        # self.brick_bottom_y += [264 - self.vel,
        #                         264 - self.vel, 264 - 2 * self.vel]
        # self.brick_bottom_x += [192]
        # self.brick_bottom_y += [264 - self.vel]

        self.bricks = Component(
            self.screen, 'BD_sprites/Brick.png', self.brick_bottom_x, self.brick_bottom_y)

        self.blocks = Component(
            self.screen, 'BD_sprites/Block.png', self.x_blocks_init, self.y_blocks_init)

        # self.door = Component(
        #     self.screen, 'BD_sprites/Door.png', [408], [240])
        self.door = Component(
            self.screen, 'BD_sprites/Door.png', [96], [240])

        # self.redraw()
        self.initial_obs = self.get_state()

        self.discrete_actions = [0, 1, 2, 3]
        self.action_space = Discrete(len(self.discrete_actions))
        self.action = np.random.choice(self.discrete_actions)
        self.observation_space = Box(low=0, high=255, shape=(
            self.screen_height, self.screen_width, 3), dtype=np.uint8)
        self.n_step = 0
        self.max_steps = 200
        self.viewer = None

    def redraw(self):

        self.screen.fill((255, 255, 255))

        self.player.draw()
        self.bricks.draw()
        self.blocks.draw()
        self.door.draw()

        pygame.display.update()

    def state(self):
        canvas = np.zeros((self.screen_width, self.screen_height, 3))

    def reset(self):
        self.player.set_position(self.x_player_init, self.y_player_init)
        self.player.set_direction('LEFT')
        self.blocks.set_position(self.x_blocks_init, self.y_blocks_init)
        self.carry = False
        self.carried_bloc = -1
        self.action = -1
        self.n_step = 0

        self.redraw()

        observation = self.get_state()

        return observation

    def gravity(self, agent, index=0):

        bricks_list = []
        blocks_list = []
        high_brick, high_block = [], []
        for i in range(len(self.bricks.x)):
            if self.bricks.x[i] == agent.x[index]:
                if self.bricks.y[i] > agent.y[index]:
                    bricks_list.append(i)

        for i in range(len(self.blocks.x)):
            if self.blocks.x[i] == agent.x[index]:
                if self.blocks.y[i] > agent.y[index]:
                    blocks_list.append(i)

        if bricks_list:
            min_ind = bricks_list[
                np.argmin([self.bricks.y[i] for i in bricks_list])]
            high_brick = [self.bricks.x[min_ind], self.bricks.y[min_ind]]

        if blocks_list:
            min_ind = blocks_list[
                np.argmin([self.blocks.y[i] for i in blocks_list])]
            high_block = [self.blocks.x[min_ind], self.blocks.y[min_ind]]

        if (high_brick and not high_block):
            agent.y[index] = high_brick[1] - self.vel
        elif (high_block and not high_brick):
            agent.y[index] = high_block[1] - self.vel
        elif high_brick and high_brick:
            if high_brick[1] < high_block[1]:
                agent.y[index] = high_brick[1] - self.vel
            elif high_brick[1] > high_block[1]:
                agent.y[index] = high_block[1] - self.vel

    def step(self, action):

        self.n_step += 1

        self.play_on = False

        brick_dir_left = self.bricks.is_component(
            self.player.x[0] - self.vel, self.player.y[0])

        block_dir_left = self.blocks.is_component(
            self.player.x[0] - self.vel, self.player.y[0])

        brick_dir_right = self.bricks.is_component(
            self.player.x[0] + self.vel, self.player.y[0])

        block_dir_right = self.blocks.is_component(
            self.player.x[0] + self.vel, self.player.y[0])

        brick_up_left = self.bricks.is_component(
            self.player.x[0] - self.vel, self.player.y[0] - self.vel)

        block_up_left = self.blocks.is_component(
            self.player.x[0] - self.vel, self.player.y[0] - self.vel)

        brick_up_right = self.bricks.is_component(
            self.player.x[0] + self.vel, self.player.y[0] - self.vel)

        block_up_right = self.blocks.is_component(
            self.player.x[0] + self.vel, self.player.y[0] - self.vel)

        # if player moves left
        if action == 0 and self.player.x[0] - self.vel >= 0:
            self.player.set_direction('LEFT')
            if not (brick_dir_left[0] or block_dir_left[0]):
                self.player.x[0] -= self.vel

        # if player moves right
        elif action == 1 and self.player.x[0] < self.screen_width - self.player.width:
            self.player.set_direction('RIGHT')
            if not (brick_dir_right[0] or block_dir_right[0]):
                self.player.x[0] += self.vel

        # if player moves up
        elif action == 2 and self.player.y[0] - self.vel > 0:
            if self.player.get_direction() == 'LEFT' and (brick_dir_left[0] or block_dir_left[0]) and not (brick_up_left[0] or block_up_left[0]):
                self.player.y[0] -= self.vel
                self.player.x[0] -= self.vel
            elif self.player.get_direction() == 'RIGHT' and (brick_dir_right[0] or block_dir_right[0]) and not (brick_up_right[0] or block_up_right[0]):
                self.player.y[0] -= self.vel
                self.player.x[0] += self.vel

        # if player picks or drops block
        elif action == 3:
            if not self.carry:
                if self.player.get_direction() == 'LEFT' and block_dir_left[0] and not brick_up_left[0] and not block_up_left[0]:
                    self.carried_bloc = block_dir_left[1]
                    self.carry = True
                elif self.player.get_direction() == 'RIGHT' and block_dir_right[0] and not brick_up_right[0] and not block_up_right[0]:
                    self.carried_bloc = block_dir_right[1]
                    self.carry = True
            elif self.carry:
                self.carry = False
                if self.player.get_direction() == 'LEFT' and brick_dir_left[0] and not brick_up_left[0] and not block_dir_left[0] and not block_up_left[0]:
                    self.blocks.x[self.carried_bloc] = self.bricks.x[
                        brick_dir_left[1]]
                    self.blocks.y[self.carried_bloc] = self.bricks.y[
                        brick_dir_left[1]] - self.vel
                elif self.player.get_direction() == 'LEFT' and block_dir_left[0] and not block_up_left[0] and not brick_dir_left[0] and not brick_up_left[0]:
                    self.blocks.x[self.carried_bloc] = self.blocks.x[
                        block_dir_left[1]]
                    self.blocks.y[self.carried_bloc] = self.blocks.y[
                        block_dir_left[1]] - self.vel
                elif self.player.get_direction() == 'RIGHT' and brick_dir_right[0] and not brick_up_right[0] and not block_dir_right[0] and not block_up_right[0]:
                    self.blocks.x[self.carried_bloc] = self.bricks.x[
                        brick_dir_right[1]]
                    self.blocks.y[self.carried_bloc] = self.bricks.y[
                        brick_dir_right[1]] - self.vel
                elif self.player.get_direction() == 'RIGHT' and block_dir_right[0] and not block_up_right[0] and not brick_dir_right[0] and not brick_up_right[0]:
                    self.blocks.x[self.carried_bloc] = self.blocks.x[
                        block_dir_right[1]]
                    self.blocks.y[self.carried_bloc] = self.blocks.y[
                        block_dir_right[1]] - self.vel
                elif self.player.get_direction() == 'RIGHT' and not brick_dir_right[0] and not block_dir_right[0] and not brick_up_right[0] and not block_up_right[0]:
                    self.blocks.x[
                        self.carried_bloc] = self.player.x[0] + self.vel
                    self.blocks.y[self.carried_bloc] = self.player.y[0]
                elif self.player.get_direction() == 'LEFT' and not brick_dir_left[0] and not block_dir_left[0] and not brick_up_left[0] and not block_up_left[0]:
                    self.blocks.x[
                        self.carried_bloc] = self.player.x[0] - self.vel
                    self.blocks.y[self.carried_bloc] = self.player.y[0]
                else:
                    self.carry = True

        # pull player down (gravity)
        if not action == 2:
            self.gravity(self.player)

        # pull block down, on player or using gravity
        if self.blocks.x:
            if self.carry:
                self.blocks.x[self.carried_bloc] = self.player.x[0]
                self.blocks.y[self.carried_bloc] = self.player.y[
                    0] - self.vel
            else:
                self.gravity(self.blocks, self.carried_bloc)

        self.redraw()
        info = {}
        observation = self.get_state()

        if self.door.is_door(self.player.x, self.player.y):
            done = True
            reward = 50.0
            self.reset()
        elif self.n_step > self.max_steps:
            done = True
            reward = -1.0
            self.reset()
        else:
            done = False
            reward = -1.0

        return observation, reward, done, info

    def sample_action(self):
        return np.random.choice(self.discrete_actions)

    def play(self):
        running = True

        while running:
            pygame.time.delay(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.keys = pygame.key.get_pressed()
                num_keys = 0
                for key in self.keys:
                    num_keys += 1 if key == 1 else 0

                if event.type == pygame.KEYDOWN and num_keys == 1 and self.play_on:
                    if self.keys[pygame.K_q]:
                        running = False
                        self.reset()
                    elif self.keys[pygame.K_r]:
                        new_ob = self.reset()
                    elif self.keys[pygame.K_LEFT]:
                        self.action = 0
                    elif self.keys[pygame.K_RIGHT]:
                        self.action = 1
                    elif self.keys[pygame.K_UP]:
                        self.action = 2
                    elif self.keys[pygame.K_DOWN]:
                        self.action = 3

                    if self.action != -1:
                        observation, reward, done, _ = self.step(
                            self.action)

                elif event.type == pygame.KEYUP:
                    if not (self.keys[pygame.K_LEFT] and self.keys[pygame.K_RIGHT] and self.keys[pygame.K_UP] and self.keys[pygame.K_DOWN]):
                        self.play_on = True

                self.redraw()

    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state

    def render(self, mode='human', close=False):
        img = self.get_state()
        if mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        elif mode == 'rgb_array':
            return img

# if __name__ == "__main__":
#     block_dude = BlockDude()
#     block_dude.play()
