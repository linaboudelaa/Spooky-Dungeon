try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    class Keyboard:
        def __init__(self):
            self.right = False
            self.left = False 
            self.z = False

        def keyDown(self, key):
            if key == simplegui.KEY_MAP['right']:
                self.right = True
            if key == simplegui.KEY_MAP['left']:
                self.left = True
            if key == simplegui.KEY_MAP['z']:
                self.z = True

        def keyUp(self, key):
            if key == simplegui.KEY_MAP['right']:
                self.right = False
            if key == simplegui.KEY_MAP['left']:
                self.left = False
            if key == simplegui.KEY_MAP['z']:
                self.z = False