import pygame
from pygame import *
import random


class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 813
        self.SCREEN_HEIGHT = 750

        self.ZOMBIE_WIDTH = 85
        self.ZOMBIE_HEIGHT = 80

        self.FPS = 60

        self.PLAYER_SCORE = 0
        self.PLAYER_MISSES = 0

        # initialize the UI
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Whack A Zombie")
        self.background = pygame.image.load("assets/zombie-map.jpg")
        self.zombiehit = pygame.image.load("assets/zombieheadhit.png")
        self.zombie_sheet = pygame.image.load("assets/zombieee.png")
        self.zombies = []
        self.zombies.append(self.zombie_sheet.subsurface(
            227, 24, 93, 90))  # frame 1
        self.zombies.append(self.zombie_sheet.subsurface(
            112, 24, 102, 90))  # frame 2
        self.zombies.append(
            self.zombie_sheet.subsurface(7, 24, 93, 90))  # frame 3

        # positions of the holes in the background
        self.hole_positions = []
        self.hole_positions.append((635, 54))
        self.hole_positions.append((427, 180))
        self.hole_positions.append((427, 305))
        self.hole_positions.append((533, 430))
        self.hole_positions.append((320, 554))
        self.hole_positions.append((637, 554))

    # function to check if the player hit the zombie head successfully
    def is_zombie_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        return (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.ZOMBIE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.ZOMBIE_HEIGHT)

    def update(self):
        # score
        score_string = "SCORE: " + str(self.PLAYER_SCORE)
        score_text = pygame.font.Font(None, 50).render(
            score_string, True, (0, 0, 0))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 8 * 1
        score_text_pos.centery = 50
        self.screen.blit(score_text, score_text_pos)

        # misses
        misses_string = "MISSES: " + str(self.PLAYER_MISSES)
        misses_text = pygame.font.Font(None, 50).render(
            misses_string, True, (0, 0, 0))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 8 * 1
        misses_text_pos.centery = 100
        self.screen.blit(misses_text, misses_text_pos)

    def start(self):
        # Initialize the map and scores and misses
        self.screen.blit(self.background, (0, 0))
        self.update()

        run = True
        hole_index = random.randint(0, 4)
        cycle_time = 0
        frame_num = 0
        interval = 0.5  # interval between frames
        hitable = False # users can only hit when the zombie appear completely
        first_hit = True # to prevent users hit the same head more than one time and score them

        # Sound effects
        self.sound = Sound()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == MOUSEBUTTONDOWN and event.button == 1:  # left mouse button
                    self.sound.playHitSound()
                    if self.is_zombie_hit(mouse.get_pos(), self.hole_positions[hole_index]) and first_hit and hitable:
                        self.sound.playZombiePainSound()
                        first_hit = False
                        self.PLAYER_SCORE += 1
                        self.screen.blit(self.background, (0, 0))
                        self.screen.blit(
                            self.zombiehit, (self.hole_positions[hole_index][0] - 15, self.hole_positions[hole_index][1]))
                        self.update()
                    else:
                        self.PLAYER_MISSES += 1
                        self.update()

            mil = pygame.time.Clock().tick(self.FPS)
            sec = mil / 1000.0
            cycle_time += sec

            if cycle_time >= interval:
                self.screen.blit(self.background, (0, 0))

                if (frame_num == 0):
                    hole_index = random.randint(0, 5)
                    self.screen.blit(
                        self.zombies[0], self.hole_positions[hole_index])
                    hitable = False
                    frame_num += 1
                    interval = 0.2
                elif (frame_num == 1):
                    self.screen.blit(
                        self.zombies[1], self.hole_positions[hole_index])
                    hitable = False
                    frame_num += 1
                    interval = 0.2
                else:
                    self.screen.blit(
                        self.zombies[2], self.hole_positions[hole_index])
                    hitable = True
                    frame_num = 0  # reset frame_num
                    interval = 0.5

                first_hit = True
                self.update()
                cycle_time = 0

            pygame.display.flip()  # used to flip to another buffer to display changes in the screen


class Sound:
    def __init__(self):
        self.MAIN_SONG = pygame.mixer.music.load("assets/backgroundsong.mp3")
        pygame.mixer.music.play(-1)  # play until manually stopped
        self.HIT_SOUND = pygame.mixer.Sound("assets/hitsound.mp3")
        self.ZOMBIE_PAIN_SONG = pygame.mixer.Sound("assets/zombiepain.mp3")

    def playHitSound(self):
        self.HIT_SOUND.play()

    def playZombiePainSound(self):
        self.ZOMBIE_PAIN_SONG.play()


# start the game
pygame.init()
# start the game loop
myGame = Game()
myGame.start()
# stop the game
pygame.quit()
