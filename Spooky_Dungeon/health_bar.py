try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class BossHealthBar:
    def _init__(self):
        self.image = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac645/cs1822/boss_bar.png")
        self.total_frames = 12
        self.frame_height = 50
        self.frame_width = 500
        self.hp = 12

    def update(self, hp):
        self.hp = (0, self.total_frames)

    def draw(self, canvas):
        if self.hp <= 0:
            return
        
        source_center = (self.frame_width / 2, self.frame_height * (self.hp - 1) + self.frame_height / 2)
        source_size = (self.frame_width, self.frame_height)
        dest_center = (768 // 2, 432 - 15)
        dest_size = (self.frame_width, self.frame_height)

        canvas.draw_image(
            self.image,
            source_center,
            source_size,
            dest_center,
            dest_size
        )