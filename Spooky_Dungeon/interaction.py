from vector import Vector
from keyboard import Keyboard
from Sprites import Sprites
from background import Background
from clock import Clock
from enemies import orc_berserk, orc_warrior, skeleton_knight, skeleton_spear, chimere_crow, chimere_eagle
from rounds import Round1, Round2, Round3, Round4

try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
    class Interaction:
        def __init__(self, sprite, round, keyboard):
            self.sprite = sprite
            self.round = round
            self.keyboard = keyboard

        def update(self):
            if self.sprite.fully_dead:
                return
            
            if self.sprite.attacking:
                return

            moving = False

            if self.keyboard.x:
                self.sprite.shield_up = True
                self.sprite.animation("protect")
            else:
                self.sprite.shield_up = False

                if self.keyboard.z and not self.sprite.attacking and self.sprite.attack_cooldown == 0:
                    self.sprite.attacking = True
                    self.sprite.animation("attack1")
                    return

                if self.keyboard.right:
                    self.sprite.vel.add(Vector(2.2,0))
                    self.sprite.animation("run")
                    moving = True
                if self.keyboard.left:
                    self.sprite.vel.add(Vector(-2.2,0))
                    self.sprite.animation("run")
                    moving = True
        
                if not moving:
                    self.sprite.animation("idle")

            
            self.round.update()


background = Background()
sprite = Sprites()
kbd = Keyboard()
inter = Interaction(sprite, None, kbd)

round_number = 1
current_round = Round1(sprite, background)
inter.round = current_round

clock = Clock()
frame_duration = 5



def draw(canvas):
    global current_round, round_number

    inter.update()
    current_round.draw(canvas)
    sprite.draw(canvas)

    clock.tick()

    current_round.update()

    if clock.transition(frame_duration):
        sprite.update()

    
    if current_round.round_end and sprite.pos.x < 0:
        round_number += 1

        if round_number == 2:
            current_round = Round2(sprite, background)
        elif round_number == 3:
            current_round = Round3(sprite, background)  
        elif round_number == 4:
            current_round == Round4(sprite, background)

        sprite.pos = Vector(700, 210)

frame = simplegui.create_frame("spooky dungeon", 768, 432)
frame.set_draw_handler(draw)

frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.start()