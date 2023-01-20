import pygame

import core
import collision
import objects.bullet
import objects.player
import objects.archer
import infos
import map.t_map
import map.tiles
import entity


class Game:
    """Main game class."""

    def __init__(self, maxfps: int) -> None:
        """Initialisation of game objects and variables."""

        ################################################################
        # 1. Create game objects.                                      #
        # 2. Init PyGame.                                              #
        ################################################################

        # Pygame

        self.maxfps = maxfps
        self.collision = collision.Quadtree(
            pygame.Rect(0, 32, 272, 176),
            capacity = 10
        )

        self.screen = pygame.display.set_mode((816, 624))
        pygame.display.set_caption("The Master Sword's Return")
        
        self.clock = pygame.time.Clock()
        
        pygame.key.set_repeat(30, 30)

        pygame.font.init()
        self.running = True
        self.start = False

        # Objects
        
        self.player = objects.player.Player(
            x = 125,
            y = 100,
            fac = core.FRIEND,
            dir = core.DOWN,
            speed = 30,
            change =0.2
        )
        self.infos = infos.Infos()
        self.map = map.t_map.TilesMap(
            heightmap = "./assets/map/heightmaps/test.json",
            door_north = "open",
            door_south = "closed",
            door_east = "open",
            door_west = "closed",
        )
        self.archer = objects.archer.Archer(
            x = 210,
            y = 100,
            fac = core.ENEMY,
            dir = core.DOWN,
            speed = 50,
            change = 0.2
        )

        self.entities = []

        self.entities.append(self.player)
        self.entities += self.map.get_entity_map()
        self.entities.append(self.archer)

        self.dead = False
        self.killer = None
    
    def handle_inputs(self) -> None:
        """Get the user input and react."""

        ################################################################
        # 1. Clear event queue.                                        #
        # 2. Create event queue.                                       #
        ################################################################

        self.eventqueue = []
        
        events = pygame.event.get()            
        keys = pygame.key.get_pressed()

        # Window

        for event in events:
            
            if event.type == pygame.QUIT:
                
                self.eventqueue += [(core.APP, core.QUIT)]
                return
        
        if self.dead:
            
            if keys[pygame.K_RETURN]:
                
                self.running = False
                return
            
            else:
                return

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

        elif keys[pygame.K_j]:
            
            self.map.set_door_state(
                north = "closed",
                south = "open",
                west = "open",
                east = "closed"
            )

        elif keys[pygame.K_k]:
            
            self.map.set_door_state(
                north = "open",
                south = "closed",
                west = "closed",
                east = "open"
            )

        elif keys[pygame.K_DELETE]:
            
            self.dead = True
            return
        
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
        
        # Handle events
        
        for event in self.eventqueue:

            key, info = event

            # Window

            if key == core.APP:
                if info == core.QUIT:
                    
                    self.running = False
                    return
                
            # Movement

            elif key == core.MOVE:

                if info == core.DOWN_LEFT:
                    self.player.move_down_left(elapsed_time)
                
                elif info == core.DOWN_RIGHT:
                    self.player.move_down_right(elapsed_time)
                
                elif info == core.UP_LEFT:
                    self.player.move_up_left(elapsed_time)
                
                elif info == core.UP_RIGHT:
                    self.player.move_up_right(elapsed_time)

                elif info == core.LEFT:
                    self.player.move_left(elapsed_time)
                
                elif info == core.RIGHT:
                    self.player.move_right(elapsed_time)

                elif info == core.UP:
                    self.player.move_up(elapsed_time)
                
                elif info == core.DOWN:
                    self.player.move_down(elapsed_time)
            
            # Actions

            elif key == core.ACTION:
                if info == core.SHOOT:
                    
                    bullet = self.player.shoot()
                    
                    if bullet != None:
                        
                        self.entities.append(bullet)
                        bullet.init_rect()

        # AI Actions

        for en in self.entities:
            if isinstance(en, objects.archer.Archer):
                
                bullet = en.action(self.player, elapsed_time)
                
                if bullet != None:
                    
                    self.entities.append(bullet)
                    bullet.init_rect()
        
        # Update hitboxes

        self.collision.clear()

        for en in self.entities:

            en.update_rect()
            self.collision.insert(en)

        # Check collisions

        self.collision.handle(self.entities)

        # Update entities

        for en in self.entities:
            
            if not isinstance(
                en, (
                    objects.archer.Archer,
                    objects.bullet.Bullet,
                    objects.player.Player
                )
            ):
                continue

            en.update_sprite(elapsed_time)
            en.update(elapsed_time)
        
        # Inactive entities

        for en in self.entities:
            if not en.active:
                self.entities.remove(en)

        # Infos
        
        curr_millis = pygame.time.get_ticks()
        curr_minutes, curr_millis = divmod(curr_millis, 60_000)
        curr_seconds, curr_millis = divmod(curr_millis, 1_000)
        if not self.dead:
            self.infos.update_time(curr_minutes, curr_seconds)

        curr_fps = self.clock.get_fps()
        self.infos.update_fps(curr_fps)

        curr_health = self.player.health
        self.infos.update_hearts(curr_health) # Player info
    
    def render(self) -> None:
        """Render the seen image."""

        ################################################################
        # 1. Render the game objects.                                  #
        # 2. Update the display.                                       #
        ################################################################

        # Objects

        objects = []

        objects += self.map.get_map()
        for en in self.entities:
            if isinstance( en, map.tiles.Tile ): continue # map bugfix
            objects += en.render()
        objects += self.infos.render()
        if self.dead:
            objects += self.infos.kill_screen(self.killer)
        
        objects += self.collision.render(self.player)
        objects += core._render_coordinates(
            core._downscale_coordinates(
                pygame.mouse.get_pos(),
                (816, 624), (272, 208)
            )
        )
        
        # Display

        orig_surface = pygame.surface.Surface((272, 208))
        orig_surface.fill((0, 0, 0))
        orig_surface.blits(objects)

        scld_surface = pygame.transform.scale(orig_surface, (816, 624))

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
