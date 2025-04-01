import simplegui
import math


class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
    
#button class, check
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
        self.new_bg_image = simplegui.load_image("https://i.imgur.com/0WDWGdl.png") #image2
        self.final_bg_image = simplegui.load_image("https://i.imgur.com/928ZLXD.png") #image3
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
            
            
            if self.bg_state == 1:
                target_position = Vector(628, 195)
                tolerance = 50
                if self.is_within_tolerance(click_position, target_position, tolerance):
                    self.bg_state = 2
                    
            elif self.bg_state == 2:
                target_position = Vector(197, 250)
                tolerance = 50
                if self.is_within_tolerance(click_position, target_position, tolerance):
                    self.bg_state = 3
                    
                    
                    
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
    
