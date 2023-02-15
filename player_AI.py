import pygame
import random
import time
from Player import *

class PlayerAI:

    def __init__(self):
        self.player = Player((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        self.dna = []
        self.allele_count = 200
        self.create_dna_sequence()
        self.currentAllele = 0
        self.delay = 100_000_000
        self.next_act = time.time_ns() + self.delay
        self.vx = 0
        self.force_x = 5
        self.world_force_x = 0.5
        self.x_distance_covered = 0

    def set_dna(self,dna_sequence):
        self.dna=dna_sequence

    def create_dna_sequence(self):
        # 0 - junk DNA - 80%
        # 1 - jump - 6%
        # 2 - move left - 7%
        # 3 - move right - 7%
        for i in range(self.allele_count):
            choice = random.randint(1,100)
            if(choice <= 80): #junk
                self.dna.append(0)
            elif(choice <= 86): #jump
                self.dna.append(1)
            elif(choice <= 93): #move left
                self.dna.append(2)
            elif(choice <= 100): #move right
                self.dna.append(3)

    def get_score(self):
        return self.player.get_score()

    def is_done(self):
        return self.currentAllele == self.allele_count

    def get_current_allele(self):
        return self.currentAllele

    def reset(self):
        self.currentAllele = 0
        self.player.set_x(400)
        self.player.set_y(400)

    def act(self):
        #print(str(time.time_ns()))
        if self.next_act < time.time_ns() and self.currentAllele < self.allele_count:
            if self.dna[self.currentAllele] == 1:
                self.player.jump()
            elif self.dna[self.currentAllele] == 2:
                self.vx -= self.force_x
            elif self.dna[self.currentAllele] == 3:
                self.vx += self.force_x

            # add x-velocity to x-position
            self.player.set_x(self.player.get_x() + self.vx)

            # reduce x-velocity by some world constant (friction)
            if self.vx < 0:
                self.vx += self.world_force_x
            elif self.vx > 0:
                self.vx -= self.world_force_x

            self.next_act = time.time_ns() + self.delay
            self.currentAllele += 1
            #print(str(self.currentAllele) + ":" + str(self.dna[self.currentAllele]))

        self.x_distance_covered = self.player.get_x()
        return self.player.act()

    def draw(self, screen):
        self.player.draw(screen)

    def setMap(self, map):
        self.player.setMap(map)

    def get_score(self):
        return self.player.get_score()