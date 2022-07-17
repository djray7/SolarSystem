import math
import arcade
import os
from datetime import datetime

relpath = lambda p: os.path.normpath(os.path.join(os.path.dirname(__file__), p))
# Global constants to use throughout the game
# Screen parameters
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200
# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

SOLAR_SYSTEM = 178619362920.544
# Distance form Sun (km)
MERCURY_DIST = 57900000
VENUS_DIST   = 108200000
EARTH_DIST   = 149600000
MARS_DIST    = 227900000
JUPITER_DIST = 778600000
SATURN_DIST  = 1433500000
URANUS_DIST  = 2872500000
NEPTUNE_DIST = 4495100000
PLUTO_DIST   = 5884500000
# Radius of planets (km)
SUN_RADIUS     = 432690
MERCURY_RADIUS = 2439.5
VENUS_RADIUS   = 6054
EARTH_RADIUS   = 6378
MARS_RADIUS    = 3396
JUPITER_RADIUS = 71492
SATURN_RADIUS  = 60268
URANUS_RADIUS  = 25559
NEPTUNE_RADIUS = 24764
PLUTO_RADIUS   = 7444 #this is not real

SCALE_PLANET = 0.007
SCALE_SYSTEM = 0.000001

#Sun to Mercury size(Sun radius) to distance(kil) ratio
SUN_MERCURY_RATIO = SUN_RADIUS / 67368000

# Distance Ratios to Earth

# Size Ratios to Sun(Kilometers)
SUN_SIZE = 200
MERCURY_SIZE = (1 / 277)* SUN_SIZE
VENUS_SIZE = (1 / 113) * SUN_SIZE
EARTH_SIZE = (1 / 108) * SUN_SIZE
MARS_SIZE = (1 / 208) * SUN_SIZE
JUPITER_SIZE = (1 / 9.7) * SUN_SIZE
SATURN_SIZE = (1 / 11.4) * SUN_SIZE
URANUS_SIZE = (1 / 26.8) * SUN_SIZE
NEPTUNE_SIZE = (1 / 27.7) * SUN_SIZE
PLUTO_SIZE = (1 / 585) * SUN_SIZE

MERCURY_D = SUN_SIZE / SUN_MERCURY_RATIO

SCREEN_TITLE = "Solar System 1.4"
SHIP_TURN_AMOUNT = 3
SHIP_SPEED = 3

class Point:
    """
    This class is a coordinates of a central point of objects
    """
    def __init__(self):
        """
        Basic stat initialization.
        By default, the object is located at a point with coordinates 0,0
        """
        self.x = 0
        self.y = 0

class Velocity:
    """
    This class tells how the coordinates will change while moving.
    (It is necessary for moving elements. For example: a ship)
    """
    def __init__(self):
        """
        Basic stat initialization.
        By default, the coordinates do not change, so the coefficients are specified as 0.
        """
        self.dx = 0
        self.dy = 0

class Ship:
    """
    This class describes all the characteristics and capabilities of the ship.
    """
    def __init__(self):
        """
        Basic stat initialization
        """  
        self.img = relpath("images/ship_1.png")
        self.texture = arcade.load_texture(self.img) # -> the path to the image
        self.width = self.texture.width*0.10
        self.height = self.texture.height*0.10
        self.ship_dist = EARTH_DIST # -> distance between Sun and ship
        self.center = Point() # -> coordinates of the center
        self.center.x = 350 # -> x-coordinate changed
        self.center.y = 250 # -> y-coordinate changed
        self.velocity = Velocity() # -> values for changing coordinates
        self.angle = 0
    
    def advance(self):
        """ a base method for movement"""
        # self.bounds() this would help to limit the movement of the ship
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def draw(self): 
        arcade.draw_texture_rectangle(self.center.x,self.center.y, 
                                    self.width, self.height, 
                                    self.texture, self.angle, 255)
    
    def rotate(self, key):
        if key == 'l':
            self.angle += SHIP_TURN_AMOUNT
        if key == 'r':
            self.angle -= SHIP_TURN_AMOUNT
    def move(self, key):
        if key == 'u':
            self.velocity.dx = (-SHIP_SPEED)*math.sin(math.radians(self.angle))# * SHIP_SPEED
            self.velocity.dy = (SHIP_SPEED)*math.cos(math.radians(self.angle))# * SHIP_SPEED
        if key == 'd':
            self.velocity.dx = 0
            self.velocity.dy = 0


# This could be a planet base class
class Planet:
    """
    The class describes the main characteristics of the planet and draws it.
    """
    def __init__(self, name, p_dist, distX, radius):
        """
        Basic stat initialization.
        It uses:
        name - can be used for img path and for info part on the screen
        p_dist - planet distance from the Sun. Will be used fof info part
        distX - position on the screen. Can be related to the actual distance from the Sun. Now it is form the head.
        radius - planet radius. Can be related to the real numbers. Now it is form the head.
        """

        self.name = name # -> planet name (can be used for img name)
        self.p_dist = p_dist # -> planet distance from the Sun
        self.radius = radius # -> radius of the planet to help with scaling
        self.img = f"images/{self.name}.png" # -> the path to the image
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width*SCALE_PLANET*radius
        self.height = self.texture.height*SCALE_PLANET*radius
        self.center = Point() # -> coordinates of the center
        self.center.x = distX # -> x-coordinate changed according to the planet distance
        self.center.y = SCREEN_HEIGHT//2 # -> y-coordinate changed to the default
        # Planet location need to be fixed

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x,self.center.y, self.width, self.height, self.texture, 0, 255)
            
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """
    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)
        
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        # arcade.set_background_color(arcade.color.SMOKY_BLACK) # a default background

        self.background = arcade.load_texture(relpath ("images\\background.png"))
        
        self.held_keys = set()

        # Create each object
        self.ship = Ship()
        
        self.planets = [ # -> planets created
            Planet("Sun", 0,-500, SUN_SIZE),
            Planet("Mercury", MERCURY_DIST, 150, MERCURY_SIZE),
            Planet("Venus", VENUS_DIST, 250, VENUS_SIZE),
            Planet("Earth", EARTH_DIST, 350, EARTH_SIZE),
            Planet("Mars", MARS_DIST, 450,MARS_SIZE),
            Planet("Jupiter", JUPITER_DIST, 660, JUPITER_SIZE),
            Planet("Saturn", SATURN_DIST, 950, SATURN_SIZE),
            Planet("Uranus", URANUS_DIST, 1100, URANUS_SIZE),
            Planet("Neptune", NEPTUNE_DIST, 1200, NEPTUNE_SIZE),
            Planet("Pluto", PLUTO_DIST, 1400, PLUTO_SIZE)
        ]

        # Used in scrolling
        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_bottom = 0
        self.view_left = 0

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Get viewport sizes
        left, screen_width, botton, screen_height = self.get_viewport()
        #Set default values for info box at the top left of the screen
        self.place = ''
        self.radius = ''
        self.distance_from_earth = 0
        self.box_width = (2/6)*screen_width
        self.box_height = (0.7/4)*screen_height
        self.box_center_x = self.box_width//2
        self.box_center_y = screen_height-(self.box_height//2)

        self.no_repeat_planet = '' # variable to check if we already visit a planet to be written to trave_log file

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
        
        #Set new values to resize info box
        self.box_width = (2.1/6)*width
        self.box_height = (0.7/4)*height
        self.box_center_x = self.box_width//2
        self.box_center_y = height-(self.box_height//2)


    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        self.clear()
        # Clear the screen to begin drawing
        arcade.start_render()
        
        # Get viewport dimensions
        left, screen_width, bottom, screen_height = self.get_viewport()

        # Draw Background
        arcade.draw_lrwh_rectangle_textured(0,0,screen_width,screen_height, self.background)

        text_size = 18
        # Draw text on the screen so the user has an idea of what is happening
        arcade.draw_text("Press F to toggle between full screen and windowed mode, unstretched.",
                         screen_width // 2, screen_height // 2 - 20,
                         arcade.color.WHITE, text_size, anchor_x="center")


        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw each object
        for planet in self.planets:
            planet.draw() # -> each planet is drawn
        
        # the ship is drawn
        self.ship.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()
        
        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, {self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

        # Draw backgroud for info box
        arcade.draw_rectangle_filled(self.box_center_x, self.box_center_y, self.box_width, self.box_height, arcade.color.ALMOND)
        
        # Draw text for info box
        text_1 = f"Last Planet: {self.place}"
        arcade.draw_text(text_1, self.box_center_x*0.05,screen_height-self.box_height*0.25, arcade.color.BLACK_BEAN, 15)
        text_2 = f"Distance from center: {self.distance_from_earth} [Km]"
        arcade.draw_text(text_2, self.box_center_x*0.05,screen_height-self.box_height*0.50, arcade.color.BLACK_BEAN, 15)
        text_3 = f"Radius: {self.radius} [Km]"
        arcade.draw_text(text_3, self.box_center_x*0.05,screen_height-self.box_height*0.75, arcade.color.BLACK_BEAN, 15)     

    
    def check_collision(self):
        # this would help to check if we get in to a planet
        
        for planet in self.planets:
        
        # if self.ship.alive and asteroid.alive:
            too_close = planet.radius + Ship().width//2
            
            if (abs(planet.center.x - self.ship.center.x) < too_close and abs(planet.center.y - self.ship.center.y) < too_close):
                self.place = planet.name

                if self.place == "Sun":
                    self.distance_from_earth = 0
                    self.radius = SUN_RADIUS
                if self.place == "Mercury":   
                    self.distance_from_earth = MERCURY_DIST
                    self.radius = MERCURY_RADIUS
                if self.place == "Venus":   
                    self.distance_from_earth = VENUS_DIST
                    self.radius = VENUS_RADIUS
                if self.place == "Earth":   
                    self.distance_from_earth = EARTH_DIST
                    self.radius = EARTH_RADIUS
                if self.place == "Mars":   
                    self.distance_from_earth = MARS_DIST
                    self.radius = MARS_RADIUS
                if self.place == "Jutiper":   
                    self.distance_from_earth = JUPITER_DIST
                    self.radius = JUPITER_RADIUS
                if self.place == "Saturn":   
                    self.distance_from_earth = SATURN_DIST
                    self.radius = SATURN_RADIUS
                if self.place == "Uranus":   
                    self.distance_from_earth = URANUS_DIST
                    self.radius = URANUS_RADIUS
                if self.place == "Neptune":   
                    self.distance_from_earth = NEPTUNE_DIST
                    self.radius = NEPTUNE_RADIUS
                if self.place == "Pluto":   
                    self.distance_from_earth = PLUTO_DIST
                    self.radius = PLUTO_RADIUS
        
            with open("travel_log.txt", "a") as travel_log:
                if self.no_repeat_planet == self.place:
                    continue
                else:
                    travel_log.write(f"User travelled to {planet.name} which is {planet.p_dist} miles away from the sun.\n")
                    self.no_repeat_planet = planet.name

    def check_keys(self):
        """This function checks for keys that are being held down."""
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate('l')

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate('r')

        if arcade.key.UP in self.held_keys:
            self.ship.move('u')

        if arcade.key.DOWN in self.held_keys:
            self.ship.move('d')

        if arcade.key.SPACE in self.held_keys:
            # this key would help to display a planet info
            # or something like that
            pass

    def on_key_press(self, key: int, modifiers: int):
        self.held_keys.add(key)

        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
      
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
    
    def on_update (self, delta):
        """Logic for movement and other future features"""
        self.check_keys()
        self.ship.advance()
        self.check_collision()
        self.scroll_to_player()
    
    def scroll_to_player(self):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.
        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.ship.center.x < left_boundary:
            self.view_left -= left_boundary - self.ship.center.x

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.ship.center.x > right_boundary:
            self.view_left += self.ship.center.x - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.ship.center.y > top_boundary:
            self.view_bottom += self.ship.center.y - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.ship.center.y < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.ship.center.y

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera_sprites.move_to(position, CAMERA_SPEED)

def main():
    Game()
    arcade.run()


if __name__ == "__main__":
    main()
