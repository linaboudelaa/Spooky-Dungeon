from vector import Vector
import random

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

count_iteration = 0

image = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/throneroom.png")


def draw(canvas):
    
    canvas.draw_image(image, (3840/2, 2160/2), (3840, 2160), (768/2, 432/2), (768, 432))     
    
frame = simplegui.create_frame(" Coulours ", 768, 432)
frame.set_draw_handler(draw)

frame.start ()