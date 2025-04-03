from vector import Vector
from keyboard import Keyboard
from clock import Clock

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    
class Sprites:    
    def __init__(self):
        self.sprite_url = {"idle" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Knight_1/Idle.png",
                           "run" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Knight_1/Run.png",
                           "attack1" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Knight_1/Attack_1.png",
                           "death" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Knight_1/Dead.png",
                           "protect" : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Knight_1/Protect.png"
                           }

        self.sheet_height = 128
        self.animation_properties = { "idle" : {"width" : 512, "columns" : 4},
                                    "run" : {"width" : 896, "columns" : 7},
                                    "attack1" : {"width" : 640, "columns" : 5},
                                    "death" : {"width" : 768, "columns" : 6},
                                    "protect" : {"width" : 128, "columns" : 1}
                                    }
        
        self.hearts = {
            "full" : simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/hearts/full_heart.png"),
            "half" : simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/hearts/half_heart.png"),
            "empty" : simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/hearts/empty_heart.png")
        }
        self.heart_size = (64, 64)
        
        self.you_died_image = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/you_died.png")
        self.you_died_image_size = (360, 78)

        self.animations = {key : simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"
        
        self.pos = Vector(700, 210)
        self.vel = Vector(0, 0)
        self.blocked = False

        self.hp = 8
        self.attacking = False
        self.dealt_damage = False
        self.attack_cooldown = 0

        self.dead = False
        self.death_started = False
        self.fully_dead = False
        self.death_timer = 30
        self.death_animation_speed = 10

        self.shield_up = False

        self.animation_count = 0
        self.animation_speed = 5

        self.clock = Clock()

        self.current_animation_properties()
        self.frame_index = 0

    def current_animation_properties(self):
        properties = self.frames[self.current_animation]
        self.image_width = properties["width"]
        self.columns = properties["columns"]
        self.frame_width = self.image_width / self.columns

    def animation(self, animation_name):
        if self.dead and self.current_animation == "death":
            return
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_animation_properties()
            self.frame_index = 0


    def update(self):
        self.clock.tick()           
        
        if self.fully_dead:
            return

        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.death_started = False
        
        if self.dead:
            if not self.death_started:
                self.animation("death")
                self.frame_index = 0
                self.animation_count = 0
                self.death_started = True
            self.animation_count += 1
            if self.animation_count >= self.death_animation_speed:
                self.animation_count = 0
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    if self.death_timer > 0:
                        self.death_timer -= 1
                    else: 
                        self.fully_dead = True
            return


        if self.attacking:
            if self.frame_index < self.columns - 1:
                self.frame_index += 1
            else:
                self.attacking = False
                self.attack_cooldown = 20
                self.dealt_damage =False
                self.animation("idle")
            return
        
        if self.blocked:   
            if self.vel.x < 0:
                self.vel.x = 0

        self.pos.add(self.vel)
        
        if self.current_animation == "run":
            self.frame_index = (self.frame_index + 1) % self.columns
        elif self.current_animation == "idle":
            self.frame_index = (self.frame_index + 1) % self.columns

        self.vel = Vector(0, 0)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        
    def draw(self, canvas):
        if self.fully_dead:
            return

        source_center = (self.frame_index * self.frame_width + self.frame_width/2, self.sheet_height/2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width*1.8, self.sheet_height*1.7)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )

        hp = self.hp
        for i in range(4):
            if hp >= 2:
                heart_type = "full"
            elif hp == 1:
                heart_type = "half"
            else:
                heart_type = "empty"

            heart_img = self.hearts[heart_type]
            x = 768 - (i * (self.heart_size[0] + 5)) - 25
            y = 5 + self.heart_size[1] // 2

            canvas.draw_image(
                heart_img,
                (self.heart_size[0] / 2, self.heart_size[1] / 2),
                self.heart_size,
                (x, y),
                self.heart_size
            )

            hp -= 2
        