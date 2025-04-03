try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Background:
    def __init__(self) :
        self.room_urls = {
            1 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/background/castle.png",
            2 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/background/deadforest.png",
            3 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/background/terrace.png",
            4 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/background/throneroom.png"
        }
        self.rooms = {key : simplegui.load_image(url) for key, url in self.room_urls.items()}
        self.current_room = 1
    
    def draw(self, canvas):
        canvas.draw_image(self.rooms[self.current_room], (3840/2, 2160/2), (3840, 2160), (768/2, 432/2), (768, 432))

    def set_room(self, room_number):
        self.current_room = room_number