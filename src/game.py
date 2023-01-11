import pygame

import core
import objects.bullet
import objects.player
import infos
import map.gen
import map.tiles


class Game:
    """Main game class."""

    def __init__(self, maxfps: int) -> None:
        """Initialisation of game objects and variables."""

        ################################################################
        # 1. Create game objects.                                      #
        # 2. Init PyGame.                                              #
        ################################################################

        # Objects

        self.player = objects.player.Player(x=100, y=100, fac=core.FRIEND)
        self.infos = infos.Infos()
        self.map = map.gen.Room()
        self.bullets_list = []
        self.infos = infos.Infos()
        self.map = map.tiles.TilesMap()
        self.entities = []
        #Lists for collision (killed entities replaced with 'None')
        self.NEUTRAL = []
        self.MAP = []
        self.FRIEND = []
        self.ENEMY = []
        self.FAUNA = []

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
            
            # Actions (vielleicht for das Movement und im Movement schauen ob geschossen wird)

            elif key == core.ACTION:
                if info == core.SHOOT:
                    if self.player.shooting:
                
                        self.bullets_list += [(
                            objects.bullet.Bullet(
                                x=self.player.x,
                                y=self.player.y,
                                dir=self.player.dir,
                                speed=1000,
                                fac=core.FRIEND
                            )
                        )]

                        self.player.attack_last = 0

        # Check collisions
        """
        (check if schield is hit)
        (remember schielded)
        check if Player is hit
        handle Player hit
        check if Player is blocked
        handle Player block
        (vielleicht erst block dann hit um durch die Wand hitten zu vermeiden)
        check if enemy is hit
        handle enemy hit
        check if enemy blocked
        handle enemy block
        check if projectile blocked
        handle projectile block
        """
        """
        #Player hit
        l = []
        l = self.ENEMY + self.FAUNA
        r = []
        for el in l: r.append(el.rect)
        n = self.player.rect.collidelistall(r)
        for el in n:
            self.player.update_health(-0.5)
            died = self.player.check_health()
            if died:
                killer = l[el]
        
        #Enemy hit
        l = self.FRIEND + self. FAUNA
        r = []
        for el in l: r.append(el.rect)
        for en in self.ENEMY:
            if type(en) == objects.bullet.Bullet:
                continue
            r_n = r
            r_n.pop(en.id)
            n = en.rect.collidelistall(r)
            for el in n:
                en.update_health(-0.5)
                k = en.check_health()
                if k:
                    self.infos.update_kills(1)
        
        #Projectile block
        l = self.ENEMY + self.FAUNA + self.MAP + [self.player]
        r = []
        for el in l: r.append(el.rect)
        for en in self.ENEMY + self.FRIEND:
            if type(en) != objects.bullet.Bullet:
                continue
            r_n = r
            r_n.pop(en.id)
            n = en.rect.collidelistall(r)
            for el in n:
                en.revert(l[el])
        
        #Player/Enemy block
        l = self.ENEMY + self.MAP + [self.player]
        r = []
        for el in l: r.append(el.rect)
        for en in self.ENEMY + [self.player]:
            if type(en) == objects.bullet.Bullet:
                continue
            r_n = r
            r_n.pop(en.id)
            n = en.rect.collidelistall(r)
            for el in n:
                en.revert(l[el])

        

        """

        
        # TODO

        # Bullets

        for bullet in self.bullets_list: 
            
            bullet.update_sprite(elapsed_time)
            bullet.update(elapsed_time)
            
            if bullet.end == True: 
                self.bullets_list.remove(bullet)
            
        # Player

        self.player.update_sprite(elapsed_time)
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
