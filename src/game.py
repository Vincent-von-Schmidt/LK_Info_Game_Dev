import pygame

import core
import objects.bullet
import objects.player
import objects.archer
import infos
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

        self.player = objects.player.Player(
            x=100,
            y=100,
            fac=core.FRIEND,
            dir = core.DOWN,
            speed = 30,
            change = 0.2
        )
        self.infos = infos.Infos()
        self.map = map.tiles.TilesMap( door_north = True, door_south = True )
        self.archer = objects.archer.Archer(
            x=200,
            y=100,
            fac=core.ENEMY,
            dir = core.DOWN,
            speed = 30,
            change = 0.2
        )
        self.entities = []
        self.NEUTRAL = []
        self.MAP = []
        self.FRIEND = []
        self.ENEMY = []
        self.FAUNA = []

        self.entities.append(self.player)
        self.entities.append(self.archer)

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
                                speed=100,
                                fac=core.FRIEND
                            ))

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
        for en in self.entities:
            if en.fac == core.ENEMY or en.fac == core.FAUNA:
                l.append(en)
        r = []
        for en in l: r.append(en.rect)
        n = self.player.rect.collidelistall(r)
        for el in n:
            self.player.update_health(-0.5)
            died = self.player.check_health()
            if died:
                killer = l[n]
        
        #Enemy hit
        l = []
        for en in self.entities:
            if (en.fac == core.FRIEND or en.fac == core.FAUNA) and en != self.player:
                l.append(en)
        r = []
        for el in l: r.append(el.rect)
        enemies = []
        for en in self.entities:
            if en.fac == core.ENEMY and type(en) == objects.bullet.Bullet:
                enemies.append(en)
        k = 0
        for en in enemies:
            r_n = r
            r_n.pop(en.id)
            n = en.rect.collidelistall(r)
            for el in n:
                en.update_health(-0.5)
                if en.check_health():
                    k += 1
        self.infos.update_kills(k)
        
        #Projectile block
        l = []
        for en in self.entities:
            if en.fac == core.ENEMY or en.fac == core.FAUNA or en.fac == core.MAP or en == self.player:
                l.append(en)
        r = []
        for el in l: r.append(el.rect)
        bullets = []
        for en in self.entities:
            if type(en) == objects.bullet.Bullet:
                bullets.append(en)
        for en in bullets:
            r_n = r
            r_n.pop(en.id)
            n = en.rect.collidelistall(r)
            if n != []:
                en.active = False
                

        
        #Player/Enemy block
        l = []
        for en in self.entities:
            if (en.fac == core.ENEMY or en.fac == core.MAP or en == self.player) and type(en) != objects.bullet.Bullet:
                l.append(en)
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

        # Check Health

        # Update Entitties

        for en in self.entities:
            en.update_sprite(elapsed_time)
            en.update(elapsed_time)

        # Infos
        
        curr_millis = pygame.time.get_ticks()
        curr_minutes, curr_millis = divmod(curr_millis, 60_000)
        curr_seconds, curr_millis = divmod(curr_millis, 1_000)
        self.infos.update_time(curr_minutes, curr_seconds)

        curr_fps = self.clock.get_fps()
        self.infos.update_fps(curr_fps)

        curr_health = self.player.health
        self.infos.update_hearts(curr_health) # Player info
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
        for en in self.entities: 
            objects += en.render()
        objects += self.infos.render()
        
        # Display

        orig_surface = pygame.surface.Surface((272, 208))
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
