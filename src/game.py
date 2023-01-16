import pygame

import core
import objects.bullet
import objects.player
import objects.archer
import infos
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

        # Objects
        
        self.player = objects.player.Player(
            x=100,
            y=100,
            fac=core.FRIEND,
            dir = core.DOWN,
            speed = 30,
            change = 0.2
        )
        self.infos = infos.Infos()
        self.map = map.tiles.TilesMap(
            heightmap = "./assets/map/heightmaps/test.json",
            door_north = "open",
            door_south = "closed",
            door_east = "open",
            door_west = "closed",
        )
        self.archer = objects.archer.Archer(
            x=200,
            y=100,
            fac=core.ENEMY,
            dir = core.DOWN,
            speed = 50,
            change = 0.2
        )

        self.entities = []

        self.entities.append(self.player)
        self.entities += self.map.get_entity_list()
        self.entities.append(self.archer)

        # Pygame

        self.maxfps = maxfps

        self.screen = pygame.display.set_mode((816, 624))
        pygame.display.set_caption("The Master Sword's Return")
        
        self.clock = pygame.time.Clock()
        
        pygame.key.set_repeat(30, 30)

        self.running = True
    
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

        id = 0
        for en in self.entities:
            en.id = id
            id += 1
        
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
            
            # Actions (vielleicht for das Movement und im Movement schauen ob geschossen wird)

            elif key == core.ACTION:
                if info == core.SHOOT:
                    if self.player.shooting:
                
                        self.entities.append(objects.bullet.Bullet(
                            x=self.player.x,
                            y=self.player.y,
                            dir=self.player.dir,
                            target=self.archer,
                            speed=100,
                            fac=core.FRIEND
                        ))

                        self.entities.append(objects.bullet.Bullet(
                            x=self.archer.x,
                            y=self.archer.y,
                            target=self.player,
                            dir=core.LEFT,
                            speed=100,
                            fac=core.ENEMY
                        ))

                        self.player.attack_last = 0
        
        # Update hitboxes

        for en in self.entities:

            if type(en) == entity.Entity: # Map bugfix
                continue

            en.update_rect()

        # Check collisions

        for entity1 in self.entities:
            for entity2 in self.entities:

                entity1: entity.Entity
                entity2: entity.Entity

                # Exklusion

                if entity1 is entity2: # Same entities
                    continue

                if not entity1.fac == core.FRIEND:
                    continue

                if not entity2.fac in (core.ENEMY, core.MAP):
                    continue

                if not entity1.rect.colliderect(entity2.rect): # No collision
                    continue

                # Inklusion

                if isinstance(entity1, objects.player.Player): # Player hit
                    
                    if (
                        isinstance(entity2, objects.bullet.Bullet)
                        and entity2.fac == core.ENEMY
                    ):

                        entity1.update_health(-0.5)
                        entity2.active = False
                        continue
                
                if (
                    isinstance(entity1, objects.bullet.Bullet)
                    and entity1.fac == core.FRIEND
                ): # Enemy hit
                    if isinstance(entity2, objects.archer.Archer):

                        entity1.active = False
                        entity2.update_health(-1)
                        continue
                
                if isinstance(entity1, objects.bullet.Bullet): # Wall hit
                    if entity2.fac == core.MAP:

                        entity1.active = False
                        continue

                if isinstance(entity1, objects.player.Player): # Wall hit
                    if entity2.fac == core.MAP:

                        tmp_up = [
                            entity1.x, entity1.y,
                            entity1.w, 1
                        ]
                        tmp_down = [
                            entity1.x, entity1.y + entity1.h,
                            entity1.w, -1
                        ]
                        tmp_left = [
                            entity1.x, entity1.y,
                            1, entity1.h
                        ]
                        tmp_right = [
                            entity1.x + entity1.w,
                            entity1.y, -1, entity1.h
                        ]
                        
                        top_offset = 6
                        tmp_rect = pygame.Rect(
                            entity2.x - entity1.w/2 - top_offset,
                            entity2.y - entity1.h/2 - top_offset,
                            entity2.w + entity1.w + 2*top_offset,
                            entity2.h + entity1.h + 2*top_offset
                        )
                        
                        if (
                            tmp_rect.contains(tmp_up)
                            and not tmp_rect.contains(tmp_left)
                            and not tmp_rect.contains(tmp_right)
                        ):
                            
                            dis = entity2.y + entity2.h - entity1.y
                            entity1.y += dis
                            continue
                        
                        if (
                            tmp_rect.contains(tmp_down)
                            and not tmp_rect.contains(tmp_left)
                            and not tmp_rect.contains(tmp_right)
                        ):
                            
                            dis = -entity1.y - entity1.h + entity2.y
                            entity1.y += dis
                            continue
                        
                        if (
                            tmp_rect.contains(tmp_left)
                            and not tmp_rect.contains(tmp_up)
                            and not tmp_rect.contains(tmp_down)
                        ):
                            
                            dis = entity2.x + entity2.w - entity1.x
                            entity1.x += dis
                            continue
                        
                        if (
                            tmp_rect.contains(tmp_right)
                            and not tmp_rect.contains(tmp_up)
                            and not tmp_rect.contains(tmp_down)
                        ):
                            
                            dis = -entity1.x - entity1.w + entity2.x
                            entity1.x += dis
                            continue

        # Update Entitties

        for en in self.entities:
            
            if type(en) == entity.Entity: # Map bugfix
                continue
            
            en.update_sprite(elapsed_time)
            en.update(elapsed_time)
        
        # Inactive entities

        for en in self.entities:
            if not en.active:
                
                entity.Entity.max_id -= 1
                self.entities.remove(en)

        # Infos
        
        curr_millis = pygame.time.get_ticks()
        curr_minutes, curr_millis = divmod(curr_millis, 60_000)
        curr_seconds, curr_millis = divmod(curr_millis, 1_000)
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
            if type(en) == entity.Entity: # Map bugfix
                continue
            objects += en.render()
        objects += self.infos.render()
        
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
