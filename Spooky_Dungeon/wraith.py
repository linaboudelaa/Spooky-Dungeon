from vector import Vector
from keyboard import Keyboard
from Sprites import Sprites
from clock import Clock
import random

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Wraith:
    def __init__(self, player):
        self.sprite_url = {
            "idle": "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/wraith3/idle.png",
            "walk": "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/wraith3/moving.png",
            "magic1": "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/wraith3/attack.png",
            "magic2": "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/wraith3/casting_spell.png"
        }

        self.sheet_height = 895
        self.animation_properties = {
            "idle": {"width": 497, "height": 895, "rows": 3, "columns": 4},
            "walk": {"width": 497, "height": 895, "rows": 3, "columns": 4},
            "magic1": {"width": 497, "height": 895, "rows": 3, "columns": 4},
            "magic2": {"width": 497, "height": 895, "rows": 4, "columns": 5}
        }

        self.animations = {key: simplegui.load_image(url) for key, url in self.sprite_url.items()}
        self.frames = self.animation_properties
        self.current_animation = "idle"

        self.pos = Vector(500, 200)
        self.vel = Vector(0, 0)
        self.player = player

        self.attacking = False
        self.attack_cooldown = 200

        self.frame_index = 0
        self.clock = Clock()

        self.current_animation_properties()

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
        wraith_pos = self.pos.x

        distance = player_pos - wraith_pos

        if abs(distance) > 300:
            direction = distance / abs(distance)
            self.vel = Vector(direction * 1.5, 0)
            self.animation("walk")
        else:
            self.vel = Vector(0, 0)
            self.animation("idle")

    def update(self):
        self.clock.tick()

        # Chase player
        self.chase_player()

        # Reduce attack cooldown when in range
        if abs(self.player.pos.x - self.pos.x) <= 300:
            self.attack_cooldown -= 1

        # Attack if cooldown is over
        if self.attack_cooldown <= 0 and not self.attacking:
            self.attacking = True
            self.attack_cooldown = 200
            attack = random.choice(["magic1", "magic2"])
            self.animation(attack)

        # Attack animation handling
        if self.attacking:
            if self.clock.transition(10):  # Slower magic animations
                if self.frame_index < self.columns - 1:
                    self.frame_index += 1
                else:
                    self.attacking = False  # End attack
                    self.animation("idle")
            return  # Stop further updates while attacking

        # Normal walking/idling animations
        if self.clock.transition(5):
            self.frame_index = (self.frame_index + 1) % self.columns

        # Move the Wraith
        self.pos.add(self.vel)

    def draw(self, canvas):
        source_center = (self.frame_index * self.frame_width + self.frame_width / 2, self.sheet_height / 2)
        source_size = (self.frame_width, self.sheet_height)
        dest_center = self.pos.get_p()
        dest_size = (self.frame_width * 1.3, self.sheet_height * 1.3)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )