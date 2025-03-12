try:
    import simplegui
except ModuleNotFoundError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Background:
    def __init__(self) :
        self.room_urls = {
            1 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/castle.png",
            2 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/deadforest.png",
            3 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/terrace.png",
            4 : "https://www.cs.rhul.ac.uk/home/zmac645/cs1822/throneroom.png"
        }
        self.rooms = {key : simplegui.load_image(url) for key, url in self.room_urls.items()}
        self.current_room = 1
    
    def draw(self, canvas):
        canvas.draw_image(self.rooms[self.current_room], (3840/2, 2160/2), (3840, 2160), (768/2, 432/2), (768, 432))

    def set_room(self, room_number):
        self.current_room = room_number

room = Background()

def draw(canvas):
    room.draw(canvas)

frame = simplegui.create_frame(" Background ", 768, 432)
frame.set_draw_handler(draw)

frame.start ()