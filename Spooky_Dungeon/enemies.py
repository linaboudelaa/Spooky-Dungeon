from vector import Vector
from keyboard import Keyboard
from Sprites import Sprites
from clock import Clock
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
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_berserk/Dead.png"
                           }

        self.sheet_height = 96
        self.animation_properties = { "idle" : {"width" : 480, "columns" : 5},
                                    "run" : {"width" : 576, "columns" : 6},
                                    "attack1" : {"width" : 384, "columns" : 4},
                                    "attack2" : {"width" : 480, "columns" : 5},
                                    "hurt" : {"width" : 192, "columns" : 2},
                                    "death" : {"width" : 384, "columns" : 4}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 230)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 3
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

        if abs(distance) > 45:
            direction = distance / abs(distance)
            self.vel = Vector(direction*1, 0)
            self.animation("run")
        elif self.attack_cooldown == 0 and not self.attacking:
            self.vel = Vector(0, 0)
            self.attacking = True
            self.attack_stage = 1
            self.animation("attack1")

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 60:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 50 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.4, self.sheet_height*1.4)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )

class orc_warrior:    
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Attack_1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Attack_2.png",
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/orc_warrior/Dead.png"
                           }

        self.sheet_height = 96
        self.animation_properties = { "idle" : {"width" : 480, "columns" : 5},
                                    "run" : {"width" : 576, "columns" : 6},
                                    "attack1" : {"width" : 384, "columns" : 4},
                                    "attack2" : {"width" : 384, "columns" : 4},
                                    "hurt" : {"width" : 192, "columns" : 2},
                                    "death" : {"width" : 384, "columns" : 4}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 230)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 3
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

        if abs(distance) > 45:
            direction = distance / abs(distance)
            self.vel = Vector(direction*1, 0)
            self.animation("run")
        elif self.attack_cooldown == 0 and not self.attacking:
            self.vel = Vector(0, 0)
            self.attacking = True
            self.attack_stage = 1
            self.animation("attack1")

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 60:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 50 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.4, self.sheet_height*1.4)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )

class skeleton_knight: 
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Attack_1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Attack_2.png",
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Warrior/Dead.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle" : {"width" : 896, "columns" : 7},
                                    "run" : {"width" : 1024, "columns" : 8},
                                    "attack1" : {"width" : 640, "columns" : 5},
                                    "attack2" : {"width" : 768, "columns" : 6},
                                    "hurt" : {"width" : 256, "columns" : 2},
                                    "death" : {"width" : 512, "columns" : 4}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 210)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 2
        self.hp_removed = False

        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 70:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 60 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        
        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.8, self.sheet_height*1.4)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )

class skeleton_spear: 
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Attack_1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Attack_2.png",
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Skeleton_Spearman/Dead.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle" : {"width" : 896, "columns" : 7},
                                    "run" : {"width" : 768, "columns" : 6},
                                    "attack1" : {"width" : 512, "columns" : 4},
                                    "attack2" : {"width" : 512, "columns" : 4},
                                    "hurt" : {"width" : 384, "columns" : 3},
                                    "death" : {"width" : 640, "columns" : 5}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 210)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 2
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 70:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 60 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.8, self.sheet_height*1.4)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )        

class chimere_crow:
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Attack_1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Attack_2.png",
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_crow/Dead.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle" : {"width" : 768, "columns" : 6},
                                    "run" : {"width" : 1024, "columns" : 8},
                                    "attack1" : {"width" : 768, "columns" : 6},
                                    "attack2" : {"width" : 512, "columns" : 4},
                                    "hurt" : {"width" : 384, "columns" : 3},
                                    "death" : {"width" : 768, "columns" : 6}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 220)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 4
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 70:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 60 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

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

class chimere_eagle:
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Attack_2.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Attack_3.png",
                           "hurt" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Hurt.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/chimere_eagle/Dead.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle" : {"width" : 768, "columns" : 6},
                                    "run" : {"width" : 1024, "columns" : 8},
                                    "attack1" : {"width" : 768, "columns" : 6},
                                    "attack2" : {"width" : 512, "columns" : 4},
                                    "hurt" : {"width" : 384, "columns" : 3},
                                    "death" : {"width" : 768, "columns" : 6}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.position_x = random.randint(-20, 0)
        self.pos = Vector(self.position_x, 220)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        self.attack_stage = 0
        self.attack_cooldown = 0
        
        self.hurt = False
        self.hurt_timer = 10
        
        self.hp = 4
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

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

    def check_collision(self):
        if abs(self.pos.x - self.player.pos.x) <= 70:
            self.player.blocked = True
        else:
            self.player.blocked = False

    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def get_hit(self):
        if self.player.attacking and not self.player.dealt_damage and abs(self.pos.x - self.player.pos.x) <= 60 and not self.dead:
            self.hp -= 1
            self.player.dealt_damage = True
            self.hurt = True
            if self.hp <= 0:
                self.animation("death")
                self.dead = True
                self.death_started = False
            

    def update(self):
        self.clock.tick()
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return
        
        self.get_hit()
        self.hit()

        if self.hurt:
            self.animation("hurt")
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.hurt = False
                self.hurt_timer = 10
                self.animation("idle")
            return
        
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
                        self.hp_removed = False
                        self.animation("idle")
            return
        
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.chase_player()

        self.check_collision()
            
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
        if self.dead and self.death_timer == 0:
            return

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

class Boss:
    def __init__(self, player):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/walk.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/atk1.png",
                           "attack2" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/atk2.png",
                           "attack3" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/atk3.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss/death.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle": {"width": 1280, "columns": 4},
                                    "walk": {"width": 1220, "columns": 6},
                                    "attack1": {"width": 6400, "columns": 20},
                                    "attack2": {"width": 2560, "columns": 8},
                                    "attack3": {"width": 2880, "columns": 9},
                                    "death": {"width": 3840, "columns": 12}
                                    }

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.pos = Vector(20, 220)
        self.vel = Vector(0, 0)

        self.player = player

        self.attacking = False
        
        self.hp = 12
        self.hp_removed = False
        
        self.death_timer = 30
        self.dead = False
        self.death_started = False
        self.fully_dead = False

        self.clock = Clock()

        self.animation_speed = 4
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

    def get_hit(self):
        if not self.dead:
            self.hp -= 1
        if self.hp <= 0:
            self.dead = True
    
    def hit(self):
        if self.attacking and abs(self.pos.x - self.player.pos.x) <= 60 and not self.hp_removed and not self.player.dead and not self.player.shield_up:
            self.player.hp -= 1
            self.hp_removed = True
        if self.player.hp <= 0:
            self.player.dead = True
            self.player.death_started = False

    def update(self):
        self.clock.tick()

        if self.fully_dead:
            return
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                elif self.death_timer > 0:
                    self.death_timer -= 1
                else: 
                    self.fully_dead = True
            return
        
        distance =  abs(self.pos.x - self.player.pos.x)
        if distance > 400 and not self.attacking:
            self.attacking = True
            self.attack_stage = "attack1"
            self.animation("attack1")
        elif distance <= 400 and not self.attacking:
            self.attacking = True
            self.attack_stage = random.choice(["attack2", "attack3"])
            self.animation(self.attack_stage)
        
        if self.attacking:
            self.animation_count += 1
            if self.animation_count >= self.animation_speed:
                self.animation_count = 0

                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    self.attacking = False
                    self.hp_removed = False
                    self.frame_index = 0
                    self.animation("idle")
            self.hit()
            return

        self.animation_count += 1
        if self.animation_count >= self.animation_speed:
            self.animation_count = 0
            self.frame_index = (self.frame_index + 1) % self.columns

        
    def draw(self, canvas):
        if self.dead and self.death_timer <= 0:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*2.2, self.sheet_height*2.2)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )