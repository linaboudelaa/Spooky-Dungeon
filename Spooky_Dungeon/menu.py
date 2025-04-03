class Button:
    def __init__(self, position, radius, colour, velocity = Vector(0,0)):
        self.position = position
        self.radius = radius
        self.colour = colour
        self.velocity = velocity #set as default value
      
    #method to draw ball on canvas
    def draw(self, canvas):
        canvas.draw_circle(
                self.position.get_p(),
                self.radius,
                1,
                self.colour,
                self.colour)
    
    #method to check if click is inside the ball
    def check_click(self, mouse_pos, target_position, tolerance=20):
        if mouse_pos is None:
            return False
        
        distance_to_target = math.sqrt((self.position.x - target_position.x) ** 2 + (self.position.y - target_position.y) ** 2)
        
        if distance_to_target > tolerance:
            return False
        
        #calculate distance between button and click - using normal vectors
        distance = math.sqrt((self.position.x - mouse_pos.x) ** 2 + (self.position.y - mouse_pos.y) **2)
        return distance <= self.radius #click inside if distance is within radius
    
    
       
    def update(self):
        self.position.add(self.velocity)
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        
class Mouse:
    
    
    #store last mouse click position
    def __init__(self):
        self.mouse_pos = None #start with no click
    
    # update stored position when click happens
    def click_handler(self, position):
        self.mouse_pos = Vector(position[0], position[1]) #convert to vector
        
    #retrieve and reset the stored position
    def click_pos(self):
        pos = self.mouse_pos
        self.mouse_pos = None #reset after returning
        return pos
        
#connect Bs=[ll and Mouse classes
class Interaction:
    def __init__(self, button, mouse):
        #accept ball object and mouse object
        self.button = button
        self.mouse = mouse
        self.bg_image = simplegui.load_image("https://i.imgur.com/k0HXINw.png") #image1
        self.new_bg_image = simplegui.load_image("https://i.imgur.com/c6es2xV.png") #image2
        self.final_bg_image = simplegui.load_image("https://i.imgur.com/nWZ9iVX.png") #image3
        self.bg_state = 1  #1 is the original, 2 new and 3 final
            
        
    def draw_handler(self, canvas):
        canvas_width = WIDTH
        canvas_height = HEIGHT
        
     
        if self.bg_state == 1:
            bg_image = self.bg_image
        elif self.bg_state == 2:
            bg_image = self.new_bg_image
        else:
            bg_image = self.final_bg_image
        
        if bg_image.get_width() > 0 and bg_image.get_height() > 0:
            img_width = bg_image.get_width()
            img_height = bg_image.get_height()

            canvas.draw_image(
                bg_image,
                (img_width / 2, img_height / 2),
                (img_width, img_height),
                (canvas_width /2, canvas_height / 2),
                (canvas_width, canvas_height)
            )
        else:
            canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)],
                                 1, 'Black', 'Light Gray')
        
      
                
        click_position = self.mouse.click_pos()
        
        
        if click_position:
            tolerance = 50
            exit_tolerance = 10
            exit_position = Vector(617, 284)

            
            
            if self.is_within_tolerance(click_position, exit_position, exit_tolerance):
                exit()
                    
            if self.bg_state == 1:
                target_position = Vector(628, 195)
                if self.is_within_tolerance(click_position, target_position, tolerance):
                    self.bg_state = 2
                
                    
            elif self.bg_state == 2:
                target_positions = [Vector(197, 250), Vector(590, 245)]
                back_position = Vector(55, 455)
                for target_position in target_positions:
                    if self.is_within_tolerance(click_position, target_position, tolerance):
                        self.bg_state = 3
                        break
                if self.is_within_tolerance(click_position, back_position, tolerance):
                    self.bg_state = 1
            elif self.bg_state == 3:
                back_position = Vector(60, 470)
                if self.is_within_tolerance(click_position, back_position, tolerance):
                    self.bg_state = 2
                
               
                    
                    
    def is_within_tolerance(self, click_position, target_position, tolerance):
                
        distance = math.sqrt((click_position.x - target_position.x) ** 2 +
                             (click_position.y - target_position.y) ** 2)
        
        return distance <= tolerance
    



WIDTH, HEIGHT = 800, 500
first_button = Button(Vector(WIDTH // 2, HEIGHT // 2), 30, "Red", Vector(0,0))

#create mouse and interaction objects
mouse = Mouse() 
interaction = Interaction(first_button, mouse)
    
frame = simplegui.create_frame('Testing Click Button',WIDTH, HEIGHT)
frame.set_draw_handler(interaction.draw_handler)
frame.set_mouseclick_handler(mouse.click_handler)
frame.start()
    