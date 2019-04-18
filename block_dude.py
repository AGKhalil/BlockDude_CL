import pygame
from player import Player
from box import Box
import numpy as np


class BlockDude:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Block Dude")

        self.play_on = True
        self.carry = False
        self.carried_bloc = -1

        self.screen_width = 432
        self.screen_height = 288

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        self.vel = 24

        self.player = Player(self.screen, [24], [264 - self.vel], self.vel, self.vel)
        self.brick_bottom_x = [
            i * self.vel for i in range(int(self.screen_width / self.vel))]
        self.brick_bottom_y = [self.screen_height -
                               self.vel for i in range(len(self.brick_bottom_x))]

        self.brick_bottom_x.append(192)
        self.brick_bottom_y.append(264 - self.vel)

        self.bricks = Box(
            self.screen, 'BD_sprites/Brick.png', self.brick_bottom_x, self.brick_bottom_y, self.vel, self.vel)

        self.blocks = Box(
            self.screen, 'BD_sprites/Block.png', [264, 168, 120], [264 - 24] * 3, self.vel, self.vel)

    def redraw(self):

        self.screen.fill((255, 255, 255))

        self.player.draw()
        self.bricks.draw()
        self.blocks.draw()

        pygame.display.update()

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

        if (high_brick and not high_block) or (high_brick[1] < high_block[1]):
            agent.y[index] = high_brick[1] - self.vel
        elif (high_block and not high_brick) or (high_brick[1] > high_block[1]):
            agent.y[index] = high_block[1] - self.vel

    def main(self):

        running = True

        while running:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            num_keys = 0
            for key in keys:
                num_keys += 1 if key == 1 else 0

            if event.type == pygame.KEYDOWN and num_keys == 1 and self.play_on:
                self.play_on = False

                brick_dir_left = self.bricks.is_box(
                    self.player.x[0] - self.vel, self.player.y[0])

                block_dir_left = self.blocks.is_box(
                    self.player.x[0] - self.vel, self.player.y[0])

                brick_dir_right = self.bricks.is_box(
                    self.player.x[0] + self.vel, self.player.y[0])

                block_dir_right = self.blocks.is_box(
                    self.player.x[0] + self.vel, self.player.y[0])

                brick_up_left = self.bricks.is_box(
                    self.player.x[0] - self.vel, self.player.y[0] - self.vel)

                block_up_left = self.blocks.is_box(
                    self.player.x[0] - self.vel, self.player.y[0] - self.vel)

                brick_up_right = self.bricks.is_box(
                    self.player.x[0] + self.vel, self.player.y[0] - self.vel)

                block_up_right = self.blocks.is_box(
                    self.player.x[0] + self.vel, self.player.y[0] - self.vel)

                # if player moves left
                if keys[pygame.K_LEFT] and self.player.x[0] - self.vel >= 0:
                    self.player.set_direction('LEFT')
                    if not (brick_dir_left[0] or block_dir_left[0]):
                        self.player.x[0] -= self.vel

                # if player moves right
                elif keys[pygame.K_RIGHT] and self.player.x[0] < self.screen_width - self.player.width:
                    self.player.set_direction('RIGHT')
                    if not (brick_dir_right[0] or block_dir_right[0]):
                        self.player.x[0] += self.vel

                # if player moves up
                elif keys[pygame.K_UP] and self.player.y[0] - self.vel > 0:
                    if self.player.get_direction() == 'LEFT' and (brick_dir_left[0] or block_dir_left[0]) and not (brick_up_left[0] or block_up_left[0]):
                        self.player.y[0] -= self.vel
                        self.player.x[0] -= self.vel
                    elif self.player.get_direction() == 'RIGHT' and (brick_dir_right[0] or block_dir_right[0]) and not (brick_up_right[0] or block_up_right[0]):
                        self.player.y[0] -= self.vel
                        self.player.x[0] += self.vel

                # if player picks or drops block
                elif keys[pygame.K_DOWN]:
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
                if not keys[pygame.K_UP]:
                    self.gravity(self.player)

                # pull block down, on player or using gravity
                if self.carry:
                    self.blocks.x[self.carried_bloc] = self.player.x[0]
                    self.blocks.y[self.carried_bloc] = self.player.y[
                        0] - self.vel
                else:
                    self.gravity(self.blocks, self.carried_bloc)

            elif event.type == pygame.KEYUP:
                if not (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and keys[pygame.K_UP] and keys[pygame.K_DOWN]):
                    self.play_on = True

            self.redraw()


if __name__ == "__main__":
    block_dude = BlockDude()
    block_dude.main()
