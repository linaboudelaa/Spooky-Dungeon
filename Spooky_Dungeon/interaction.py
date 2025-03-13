from vector import Vector
from keyboard import Keyboard
from Sprites import Sprites
from background import Background
from clock import Clock

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
    class Interaction:
        def __init__(self, sprite, keyboard):
            self.sprite = sprite
            self.keyboard = keyboard

        def update(self):
            if self.sprite.attacking:
                return
            
            moving = False

            if self.keyboard.z and not self.sprite.attacking and self.sprite.attack_cooldown == 0:
                self.sprite.attacking = True
                self.sprite.animation("attack1")
                return

            if self.keyboard.right:
                self.sprite.vel.add(Vector(2,0))
                self.sprite.animation("run")
                moving = True
            elif self.keyboard.left:
                self.sprite.vel.add(Vector(-2,0))
                self.sprite.animation("run")
                moving = True
        
            elif not moving:
                self.sprite.animation("idle")


kbd = Keyboard()
sprite = Sprites()
background = Background()

inter = Interaction(sprite, kbd)

clock = Clock()
frame_duration = 3



def draw(canvas):
    inter.update()
    background.draw(canvas)
    sprite.draw(canvas)

    clock.tick()
    if clock.transition(frame_duration):
        sprite.update()

frame = simplegui.create_frame("spooky dungeon", 768, 432)
frame.set_draw_handler(draw)

frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.start()