import math
import arcade
import os

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
SUN_RADIUS = 432690
MERCURY_RADIUS = 2439.5
VENUS_RADIUS = 6054
EARTH_RADIUS = 6378
MARS_RADIUS = 3396
JUPITER_RADIUS = 71492
SATURN_RADIUS = 60268
URANUS_RADIUS = 25559
NEPTUNE_RADIUS = 24764
PLUTO_RADIUS = 7444 #this is not real

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

SCREEN_TITLE = "Solar System 1.3"
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
        self.center.x = 250 # -> x-coordinate changed
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
        self.center.x = distX*SCALE_SYSTEM # -> x-coordinate changed according to the planet distance
        self.center.y = SCREEN_HEIGHT//2 # -> y-coordinate changed to the default

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
        # arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        # self.background = arcade.load_texture(r"C:\Users\Joseph Raymant\Documents\School\2022 Spring\Applied Programming(CSE 310)\Team\SolarSystem\SimpleSpace.jpg")
        self.background = arcade.load_texture(relpath ("images\\background.png"))
        
        self.held_keys = set()
        # Create each object
        self.ship = Ship()
        
        # self.planets = [ # -> planets created
        #     Planet("Sun", 0, -500, SUN_SIZE),
        #     Planet("Mercury", MERCURY_DIST, 150, MERCURY_SIZE),
        #     Planet("Venus", VENUS_DIST, 250, VENUS_SIZE),
        #     Planet("Earth", EARTH_DIST, 350, EARTH_SIZE),
        #     Planet("Mars", MARS_DIST, 450, MARS_SIZE),
        #     Planet("Jupiter", JUPITER_DIST, 620, JUPITER_SIZE),
        #     Planet("Saturn", SATURN_DIST, 800, SATURN_SIZE),
        #     Planet("Uranus", URANUS_DIST, 925, URANUS_SIZE),
        #     Planet("Neptune", NEPTUNE_DIST, 1050, NEPTUNE_SIZE),
        #     Planet("Pluto", PLUTO_DIST, 1150, PLUTO_SIZE)
        # ]
        self.planets = [ # -> planets created
            Planet("Sun", 0, 0.0, SUN_SIZE),
            Planet("Mercury", MERCURY_DIST, MERCURY_DIST, MERCURY_SIZE),
            Planet("Venus", VENUS_DIST, VENUS_DIST, VENUS_SIZE),
            Planet("Earth", EARTH_DIST, EARTH_DIST, EARTH_SIZE),
            Planet("Mars", MARS_DIST, MARS_DIST, MARS_SIZE),
            Planet("Jupiter", JUPITER_DIST, JUPITER_DIST, JUPITER_SIZE),
            Planet("Saturn", SATURN_DIST, SATURN_DIST, SATURN_SIZE),
            Planet("Uranus", URANUS_DIST, URANUS_DIST, URANUS_SIZE),
            Planet("Neptune", NEPTUNE_DIST, NEPTUNE_DIST, NEPTUNE_SIZE),
            Planet("Pluto", PLUTO_DIST, PLUTO_DIST, PLUTO_SIZE)
        ]


        # Used in scrolling
        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_bottom = 0
        self.view_left = 0

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Draw info box continuously updating the
        left, screen_width, botton, screen_height = self.get_viewport()
        self.place = ''
        self.radius = ''
        self.distance_from_earth = 0
        self.box_width = (2/6)*screen_width
        self.box_height = (1/4)*screen_height
        self.box_center_x = self.box_width//2
        self.box_center_y = screen_height-(self.box_height//2)

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
        
        self.box_width = (2/6)*width
        self.box_height = (1/4)*height
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
        
        # self.player_list.draw() # -> the ship is drawn
        self.ship.draw()
        # Display speed
        # ----------------------------HERE we need relative values for position
        # arcade.draw_text(f"X position: {self.ship.center.x:6.3f}", 10, 20, arcade.color.WHITE)
        # arcade.draw_text(f"Y position: {self.ship.center.y:6.3f}", 10, 40, arcade.color.WHITE)
        # arcade.draw_text(f"X vel: {self.ship.velocity.dx:6.3f}", 10, 60, arcade.color.WHITE)
        # arcade.draw_text(f"Y vel: {self.ship.velocity.dy:6.3f}", 10, 80, arcade.color.WHITE)

        # self.info.draw() # -> draw the list with distances
        # self.planet_info.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()
        
        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, {self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

        # Draw the 

        # Backgroud for info part
        arcade.draw_rectangle_filled(self.box_center_x, self.box_center_y, self.box_width, self.box_height, arcade.color.ALMOND)
        # Text display
        text = f"Current Planet: {self.place}"
        arcade.draw_text(text, self.box_center_x*0.05,screen_height-self.box_height*0.2, arcade.color.BLACK_BEAN, 15)
        text = f"Distance from the Earth: {self.distance_from_earth}"
        arcade.draw_text(text, self.box_center_x*0.05,screen_height-self.box_height*0.4, arcade.color.BLACK_BEAN, 15)
        text = f"Radius: {self.radius}"
        arcade.draw_text(text, self.box_center_x*0.05,screen_height-self.box_height*0.6, arcade.color.BLACK_BEAN, 15)     

                # Text
        # for i in range(len(self.dist_text['line'])):
        #     arcade.draw_text(self.dist_text['line'][i], 
        #                     start_x=self.start_x, start_y=self.dist_text['start_y'][i], 
        #                     font_size=12, color=arcade.color.NAVY_BLUE)

        # Draw the box that we work to make sure the user stays inside of.
        # This is just for illustration purposes. We'd want to remove this
        # in our game.

        # left_boundary = VIEWPORT_MARGIN
        # right_boundary = self.width - VIEWPORT_MARGIN
        # top_boundary = self.height - VIEWPORT_MARGIN
        # bottom_boundary = VIEWPORT_MARGIN
        # arcade.draw_lrtb_rectangle_outline(left_boundary, right_boundary, top_boundary, bottom_boundary,
        #                                    arcade.color.RED, 2)
    
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


                # self.planet_info = PlanetInfo(self.ship.center.x, self.ship.center.y, planet.name)

                # if self.shield_status and self.shield_life > 0 :
                #     asteroid.hit(self.asteroids)
                #     self.shield_life -= 10
                # else:
                #     if asteroid.radius == BIG_ROCK_RADIUS:
                #         self.ship_life -= 20
                #     elif asteroid.radius == MEDIUM_ROCK_RADIUS:
                #         self.ship_life -= 10
                #     elif asteroid.radius == SMALL_ROCK_RADIUS:
                #         self.ship_life -= 5
                    
                #     asteroid.hit(self.asteroids)
                
                # if self.score < 0 :
                #     self.score = 0
                
                # if self.ship_life <= 0:
                #     self.ship.active = False
                #     self.ship.alive = False
        pass

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