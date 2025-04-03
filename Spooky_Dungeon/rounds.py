import random
from enemies import orc_berserk, orc_warrior, skeleton_knight, skeleton_spear, chimere_crow, chimere_eagle, Boss
from Sprites import Sprites
from background import Background
from vector import Vector
from keyboard import Keyboard
from health_bar import BossHealthBar

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Round1:
    def __init__(self, player, background):
        self.player = player
        self.background = background

        self.round_end = False

        self.defeated_enemies = 0
        self.total_enemies = 0
        self.current_enemy = None
        self.max_enemies = 1
        self.background.set_room(1)

    def spawn_enemy(self):
        if self.total_enemies < self.max_enemies and self.current_enemy is None:
            enemy_type = random.choice([skeleton_knight, skeleton_spear])
            self.current_enemy = enemy_type(self.player)
            self.total_enemies += 1

    def update(self):
        if self.current_enemy:
            self.current_enemy.update()
            if self.current_enemy.fully_dead:
                self.defeated_enemies += 1
                self.current_enemy = None
        else:
            self.spawn_enemy()
            self.player.blocked =False

        if self.defeated_enemies >= self.max_enemies:
            self.round_end = True
        
    def draw(self, canvas):
        self.background.draw(canvas)
        if self.current_enemy:
            self.current_enemy.draw(canvas)

class Round2:
    def __init__(self, player, background):
        self.player = player
        self.background = background

        self.round_end = False

        self.defeated_enemies = 0
        self.total_enemies = 0
        self.current_enemy = None
        self.max_enemies = 1
        self.background.set_room(2)

    def spawn_enemy(self):
        if self.total_enemies < self.max_enemies and self.current_enemy is None:
            enemy_type = random.choice([orc_warrior, orc_berserk])
            self.current_enemy = enemy_type(self.player)
            self.total_enemies += 1

    def update(self):
        if self.current_enemy:
            self.current_enemy.update()
            if self.current_enemy.fully_dead:
                self.defeated_enemies += 1
                self.current_enemy = None
        else:
            self.spawn_enemy()
            self.player.blocked = False

        if self.defeated_enemies >= self.max_enemies:
            self.round_end = True
        
    def draw(self, canvas):
        self.background.draw(canvas)
        if self.current_enemy:
            self.current_enemy.draw(canvas)

class Round3:
    def __init__(self, player, background):
        self.player = player
        self.background = background

        self.round_end = False

        self.defeated_enemies = 0
        self.total_enemies = 0
        self.current_enemy = None
        self.max_enemies = 1
        self.background.set_room(3)

    def spawn_enemy(self):
        if self.total_enemies < self.max_enemies and self.current_enemy is None:
            enemy_type = random.choice([chimere_crow, chimere_eagle])
            self.current_enemy = enemy_type(self.player)
            self.total_enemies += 1

    def update(self):
        if self.current_enemy:
            self.current_enemy.update()
            if self.current_enemy.fully_dead:
                self.defeated_enemies += 1
                self.current_enemy = None
        else:
            self.spawn_enemy()
            self.player.blocked = False

        if self.defeated_enemies >= self.max_enemies:
            self.round_end = True
        
    def draw(self, canvas):
        self.background.draw(canvas)
        if self.current_enemy:
            self.current_enemy.draw(canvas)

class Round4:
    def __init__(self, player, background):
        self.player = player
        self.background = background

        self.boss = Boss(player)
        self.health_bar = BossHealthBar()

        self.boss_defeated = False
        self.background.set_room(4)

    def update(self):
        if not self.boss.fully_dead:
            self.boss.update()
            self.health_bar.update()
        else:
            self.boss_defeated = True
        
    def draw(self, canvas):
        self.background.draw(canvas)
        if not self.boss.fully_dead:
            self.boss.draw(canvas)
            self.health_bar.draw(canvas)