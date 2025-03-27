from vector import Vector
from keyboard import Keyboard
from Sprites import Sprites
import random

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    
class orc_berserk:    
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Attack_1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Attack_2.png",
                           "attack3" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Attack_3.png"
                           }

        self.sheet_height = 96
        self.animation_properties = { "idle" : {"width" : 480, "columns" : 5},
                                    "run" : {"width" : 576, "columns" : 6},
                                    "attack1" : {"width" : 384, "columns" : 4},
                                    "attack2" : {"width" : 480, "columns" : 5},
                                    "attack3" : {"width" : 192, "columns" : 2}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.pos = Vector(200, 210)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        self.attack3_delay = 0
        self.do_attack3 = False

        self.animation_speed = 5
        self.animation_count = 0

        self.current_animation_properties()
        self.frame_index = 0

    def current_animation_properties(self):
        properties = self.frames[self.current_animation]
        self.image_width = properties["width"]
        self.columns = properties["columns"]
        self.frame_width = self.image_width / self.columns

    def animation(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_animation_properties()
            self.frame_index = 0

    def chase_player(self):
        player_pos = self.player.pos.x
        orc_pos = self.pos.x

        distance = player_pos - orc_pos

        if abs(distance) > 60:
            direction = distance / abs(distance)
            self.vel = Vector(direction*1, 0)
            self.animation("run")
        elif self.attack_cooldown == 0 and not self.attacking:
            self.vel = Vector(0, 0)
            self.attacking = True
            self.attack_stage = 1
            self.animation("attack1")
            

    def update(self):
        if self.attacking:
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0

                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.attack_stage == 1:
                        self.attack_stage = 2
                        self.animation("attack2")
                    elif self.attack_stage == 2:
                        self.attacking = False
                        self.attack_cooldown = 100
                        self.animation("idle")
                    elif self.attack_stage == 3:
                        self. attacking = False
                        self.attack_stage = 0
                        self.animation("idle")
            return
        
        if self.player.attacking and random.choice([True, False]) and not self.attacking:
            self.attacking = True
            self.attack_stage = 3
            self.animation("attack3")
            return    
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.pos.add(self.vel)

        self.animation_count += 1
        if self.animation_count >= self.animation_speed:
            self.animation_count = 0
            if self.current_animation == "run":
                self.frame_index = (self.frame_index + 1) % self.columns
            elif self.current_animation == "idle":
                self.frame_index = (self.frame_index + 1) % self.columns

        self.vel = Vector(0, 0)

        
    def draw(self, canvas):
        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.3, self.sheet_height*1.3)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )



class orc_shaman:    
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_shaman/Idle.png",
                           "walk" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_shaman/Walk.png",
                           "magic1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_shaman/Magic_1.png",
                           "magic2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_shaman/Magic_2.png"
                           }

        self.sheet_height = 96
        self.animation_properties = { "idle" : {"width" : 480, "columns" : 5},
                                    "walk" : {"width" : 672, "columns" : 7},
                                    "magic1" : {"width" : 768, "columns" : 8},
                                    "magic2" : {"width" : 576, "columns" : 6}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.pos = Vector(100, 210)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_cooldown = 200

        self.animation_speed = 5
        self.animation_count = 0

        self.current_animation_properties()
        self.frame_index = 0

    def current_animation_properties(self):
        properties = self.frames[self.current_animation]
        self.image_width = properties["width"]
        self.columns = properties["columns"]
        self.frame_width = self.image_width / self.columns

    def animation(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_animation_properties()
            self.frame_index = 0

    def chase_player(self):
        player_pos = self.player.pos.x
        orc_pos = self.pos.x

        distance = player_pos - orc_pos

        if abs(distance) > 300:
            direction = distance / abs(distance)
            self.vel = Vector((direction*1)-0.3, 0)
            self.animation("walk")
        else:
            self.vel = Vector(0, 0)
            self.animation("idle")            

    def update(self):
        
        self.chase_player()

        if abs(self.player.pos.x-self.pos.x) <= 300:
            self.attack_cooldown -= 1

        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_cooldown = 200
            attack = random.choice(["magic1", "magic2"])
            self.animation(attack)

        
        if self.attacking:
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    self.attacking = False
                    self.animation("idle")
            return

        self.pos.add(self.vel)

        self.animation_count += 1
        if self.animation_count >= self.animation_speed:
            self.animation_count = 0
        if self.current_animation == "idle":
            self.frame_index = (self.frame_index + 1) % self.columns
        elif self.current_animation == "run":
            self.frame_index = (self.frame_index + 1) % self.columns



    def draw(self, canvas):
        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.3, self.sheet_height*1.3)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )
