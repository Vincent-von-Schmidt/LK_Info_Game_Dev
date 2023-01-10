import pygame

import core
import sprites.player as player
import infos
import map.background as background


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
        self.infos = infos.Infos()
        self.background = background.Background()

        # Pygame

        self.maxfps = maxfps

        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("The Master Sword's Return")
        
        self.clock = pygame.time.Clock()
        
        pygame.key.set_repeat(500, 30)

        self.eventqueue = []
        self.running = True
    
    def handle_inputs(self) -> None:
        """Get the user input and react."""

        ################################################################
        # 1. Clear event queue.                                        #
        # 2. Create event queue.                                       #
        ################################################################

        self.eventqueue.clear()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    self.eventqueue += [(core.MOVE, core.LEFT)]
                
                elif event.key == pygame.K_d:
                    self.eventqueue += [(core.MOVE, core.RIGHT)]
                
                elif event.key == pygame.K_w:
                    self.eventqueue += [(core.MOVE, core.UP)]
                
                elif event.key == pygame.K_s:
                    self.eventqueue += [(core.MOVE, core.DOWN)]
                
                elif event.key == pygame.K_LEFT:
                    self.eventqueue += [(core.VIEW, core.LEFT)]
                
                elif event.key == pygame.K_RIGHT:
                    self.eventqueue += [(core.VIEW, core.RIGHT)]
                
                elif event.key == pygame.K_UP:
                    self.eventqueue += [(core.VIEW, core.UP)]
                
                elif event.key == pygame.K_DOWN:
                    self.eventqueue += [(core.VIEW, core.DOWN)]
                
                elif event.key == pygame.K_SPACE:
                    self.eventqueue += [(core.VIEW, core.RESET)]
    
    def update(self) -> None:
        """Update scores and handle actual game logic."""

        ################################################################
        # 1. Handle input events.                                      #
        # 2. Check collisions.                                         #
        # 3. Update game infos.                                        #
        ################################################################

        elapsed_time = self.clock.get_time() / 1_000
        
        # Handle events

        for event in self.eventqueue:

            key, info = event

            if key == core.MOVE:

                if info == core.LEFT:
                    self.player.move_left(elapsed_time=elapsed_time)
                
                elif info == core.RIGHT:
                    self.player.move_right(elapsed_time=elapsed_time)

                elif info == core.UP:
                    self.player.move_up(elapsed_time=elapsed_time)
                
                elif info == core.DOWN:
                    self.player.move_down(elapsed_time=elapsed_time)
                
            elif key == core.VIEW:

                if info == core.LEFT:
                    
                    dis = self.background.move_left(elapsed_time=elapsed_time)
                    self.player.move_right(pixel=dis, still=True)
                
                elif info == core.RIGHT:
                    
                    dis = self.background.move_right(elapsed_time=elapsed_time)
                    self.player.move_left(pixel=dis, still=True)
                
                elif info == core.UP:
                    
                    dis = self.background.move_up(elapsed_time=elapsed_time)
                    self.player.move_down(pixel=dis, still=True)
                
                elif info == core.DOWN:
                    
                    dis = self.background.move_down(elapsed_time=elapsed_time)
                    self.player.move_up(pixel=dis, still=True)
                
                elif info == core.RESET:

                    x_dis = 320 - self.player.x
                    y_dis = 240 - self.player.y

                    self.player.move_right(pixel=x_dis, still=True)
                    self.player.move_down(pixel=y_dis, still=True)

                    self.background.move_left(pixel=x_dis)
                    self.background.move_up(pixel=y_dis)
        
        # Check collisions
        
        # TODO
        ...

        # Update infos
        
        curr_millis = pygame.time.get_ticks()
        curr_minutes, curr_millis = divmod(curr_millis, 60_000)
        curr_seconds, curr_millis = divmod(curr_millis, 1_000)

        curr_fps = self.clock.get_fps()

        self.infos.set_time(curr_minutes, curr_seconds)
        self.infos.set_fps(curr_fps)
    
    def render(self) -> None:
        """Render the seen image."""

        ################################################################
        # 1. Render the game objects.                                  #
        # 2. Update the display.                                       #
        ################################################################

        # Objects

        objects = []

        objects += self.background.render()
        objects += self.player.render()
        objects += self.infos.render()
        
        # Display

        self.screen.blits(objects)
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
