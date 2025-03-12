from vector import Vector
from background import Background
import random

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

animation1 = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Idle.png")
animation2 = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/Run.png")

SHEET_HEIGHT = 128
ANIMATION_PROPERTIES = { "idle" : {"width" : 768, "columns" : 6},
                        "run" : {"width" : 896, "columns" : 7}}


class Clock:
    def __init__(self):
        self.time = 0
        
    def tick(self):
        self.time += 1
    
    def transition(self, frame_duration):
        return self.time % frame_duration == 0
    
class Sprites:    
    def __init__(self):
        self.animations = {"idle" : animation1, "run" : animation2 }
        self.frames = ANIMATION_PROPERTIES
        self.current_animation = "idle"

        self.current_animation_properties()
        self.frame_index = 0

    def current_animation_properties(self):
        properties = self.frames[self.current_animation]
        self.image_width = properties["width"]
        self.columns = properties["columns"]
        self.frame_width = self.image_width / self.columns

    def animation(self, animation_name):
        self.current_animation = animation_name
        self.current_animation_properties()
        self.frame_index = 0

    def update(self):
        self.frame_index = (self.frame_index + 1) % self.columns

    def draw(self, canvas):
        source_center = (self.frame_index * self.frame_width + self.frame_width/2, SHEET_HEIGHT/2)
        source_size = (self.frame_width, SHEET_HEIGHT)
        dest_center = (300, 200)
        dest_size = (self.frame_width, SHEET_HEIGHT)

        canvas.draw_image(
            self.animations[self.current_animation],
            source_center,
            source_size,
            dest_center,
            dest_size
        )


sprite = Sprites()
clock = Clock()
frame_duration = 5
background = Background()

def draw(canvas):
    clock.tick()
    background.draw()
    if clock.transition(frame_duration):
        sprite.update()
    sprite.draw(canvas)


frame = simplegui.create_frame("Sprite animation", 600, 400)
frame.set_draw_handler(draw)
frame.set_canvas_background("Darkblue")

frame.start()