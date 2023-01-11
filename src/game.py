import pygame

import core
import sprites.player as player
import infos
import map.tiles as map
import sprites.player as player
import sprites.bullets as bullets



class Game:
    """Main game class."""

    def __init__(self, maxfps: int) -> None:
        """Initialisation of game objects and variables."""

        ################################################################
        # 1. Create game objects.                                      #
        # 2. Init PyGame.                                              #
        ################################################################

        # Objects

        self.player = player.Player()
        self.bullets_list = []
        self.infos = infos.Infos()
        self.map = map.TilesMap()
        self.entities = []

        # Pygame

        self.maxfps = maxfps

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("The Master Sword's Return")
        
        self.clock = pygame.time.Clock()
        
        pygame.key.set_repeat(30, 30)

        self.eventqueue = []
        self.running = True
    
    def handle_inputs(self) -> None:
        """Get the user input and react."""

        ################################################################
        # 1. Clear event queue.                                        #
        # 2. Create event queue.                                       #
        ################################################################

        self.eventqueue.clear()
        
        events = pygame.event.get()            
        keys = pygame.key.get_pressed()

        # Window

        for event in events:
            if event.type == pygame.QUIT:
                self.eventqueue += [(core.APP, core.QUIT)]

        # Movement

        if keys[pygame.K_a] and keys[pygame.K_s]:
            self.eventqueue += [(core.MOVE, core.DOWN_LEFT)]
        
        elif keys[pygame.K_a] and keys[pygame.K_w]:
            self.eventqueue += [(core.MOVE, core.UP_LEFT)]
        
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.eventqueue += [(core.MOVE, core.DOWN_RIGHT)]
        
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            self.eventqueue += [(core.MOVE, core.UP_RIGHT)]

        elif keys[pygame.K_a]:
            self.eventqueue += [(core.MOVE, core.LEFT)]
        
        elif keys[pygame.K_d]:
            self.eventqueue += [(core.MOVE, core.RIGHT)]
        
        elif keys[pygame.K_w]:
            self.eventqueue += [(core.MOVE, core.UP)]
        
        elif keys[pygame.K_s]:
            self.eventqueue += [(core.MOVE, core.DOWN)]

        # TODO -> remove -> test map change
        elif keys[pygame.K_n]:
            self.map.load_height_map( "./assets/map/heightmaps/test.json" )

        elif keys[pygame.K_m]:
            self.map.load_height_map( "./assets/map/heightmaps/blank.json" )
        
        # Actions
        
        if keys[pygame.K_SPACE]:
            self.eventqueue += [(core.ACTION, core.SHOOT)]
    
    def update(self) -> None:
        """Update scores and handle actual game logic."""

        ################################################################
        # 1. Handle input events.                                      #
        # 2. Check collisions.                                         #
        # 3. Update game infos.                                        #
        ################################################################

        # Reset variables

        elapsed_time = self.clock.get_time() / 1_000
        self.player.walking = False
        
        # Handle events
        
        for event in self.eventqueue:

            key, info = event

            # Window

            if key == core.APP:
                if info == core.QUIT:
                    self.running = False
                
            # Movement

            elif key == core.MOVE:

                if info == core.DOWN_LEFT:
                    self.player.move_down_left(elapsed_time=elapsed_time)
                
                elif info == core.DOWN_RIGHT:
                    self.player.move_down_right(elapsed_time=elapsed_time)
                
                elif info == core.UP_LEFT:
                    self.player.move_up_left(elapsed_time=elapsed_time)
                
                elif info == core.UP_RIGHT:
                    self.player.move_up_right(elapsed_time=elapsed_time)

                elif info == core.LEFT:
                    self.player.move_left(elapsed_time=elapsed_time)
                
                elif info == core.RIGHT:
                    self.player.move_right(elapsed_time=elapsed_time)

                elif info == core.UP:
                    self.player.move_up(elapsed_time=elapsed_time)
                
                elif info == core.DOWN:
                    self.player.move_down(elapsed_time=elapsed_time)
            
            # Actions

            elif key == core.ACTION:
                if info == core.SHOOT:
                    if not self.player.walking:
                        if self.player.shooting:
                    
                            self.bullets_list += [(
                                bullets.Bullets(
                                    self.player.x,
                                    self.player.y,
                                    self.player.pos
                                )
                            )]

                            self.player.attack_last -= self.player.attack_block

        # Check collisions
        
        # TODO

        # Bullets

        for bullet in self.bullets_list: 
            
            bullet.update(elapsed_time)
            
            if bullet.end == True: 
                self.bullets_list.remove(bullet)
            
        # Player

        self.player.update(elapsed_time)

        # Infos
        
        curr_millis = pygame.time.get_ticks()
        curr_minutes, curr_millis = divmod(curr_millis, 60_000)
        curr_seconds, curr_millis = divmod(curr_millis, 1_000)
        self.infos.set_time(curr_minutes, curr_seconds)

        curr_fps = self.clock.get_fps()
        self.infos.set_fps(curr_fps)

        self.infos.update_hearts(self.player.health) # Player info
        # TODO
        ...
    
    def render(self) -> None:
        """Render the seen image."""

        ################################################################
        # 1. Render the game objects.                                  #
        # 2. Update the display.                                       #
        ################################################################

        # Objects

        objects = []

        objects += self.map.get_map()
        for bullet in self.bullets_list: 
            objects += bullet.render()
        objects += self.player.render()
        objects += self.infos.render()
        
        # Display

        orig_surface = pygame.surface.Surface((240, 192))
        orig_surface.fill((0, 0, 0))
        orig_surface.blits(objects)

        scld_surface = pygame.transform.scale(orig_surface, (1280, 720))

        self.screen.blit(scld_surface, (0, 0))
        pygame.display.flip()
    
    def wait(self) -> None:
        """Wait to keep up a perfect frame rate."""

        ################################################################
        # 1. Wait to keep same fps.                                    #
        ################################################################

        self.clock.tick(self.maxfps)
    
    def run(self) -> None:
        """Run the main loop of the game."""

        ################################################################
        # 1. Start PyGame.                                             #
        # 2. Run mainloop.                                             #
        # 3. Quit pygame.                                              #
        ################################################################
    
        pygame.init()

        while self.running:

            self.handle_inputs()
            self.update()
            self.render()
            self.wait()
        
        pygame.quit()
