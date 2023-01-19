import pygame

import entity
import core
import map.tiles
import objects.player
import objects.archer
import objects.bullet


class Quadtree:
    """A class for quad tree collision handle."""

    def __init__(
        self, rect: pygame.Rect, capacity: int, __root: bool = True, **kwargs
    ):
        
        self.root = __root
        self.capacity = capacity

        # Init self

        self.entities = []
        self.leaf = True
        self.fix = False

        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h

        # Quadrants calc

        cw = self.rect.w / 2
        ch = self.rect.h / 2

        self.rect_up_left = pygame.Rect(
            self.rect.x, self.rect.y, cw, ch
        )
        self.rect_up_right = pygame.Rect(
            self.rect.x + cw, self.rect.y, cw, ch
        )
        self.rect_down_left = pygame.Rect(
            self.rect.x, self.rect.y + ch, cw, ch
        )
        self.rect_down_right = pygame.Rect(
            self.rect.x + cw, self.rect.y + ch, cw, ch
        )

        # Init quadrants
        
        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None
    
    @property
    def rect(self): # BUG: pygame rect only int
        return pygame.Rect(self.x, self.y, self.w, self.h)
    
    def insert(self, en: entity.Entity) -> None:
        """Insert an entity."""

        # Recursive propagation

        if not self.leaf:
            
            if self.rect_up_left.contains(en.rect):
                self.up_left.insert(en)
            
            elif self.rect_up_right.contains(en.rect):
                self.up_right.insert(en)
            
            elif self.rect_down_left.contains(en.rect):
                self.down_left.insert(en)
            
            elif self.rect_down_right.contains(en.rect):
                self.down_right.insert(en)
            
            # Size check
            
            # else: # BUG
                
            #     self.destruct()
            #     self.entities += [en]

        # Append entity

        else:

            self.entities += [en]

            # Split quadrant

            if (not self.fix) and (len(self.entities) > self.capacity):
                self.split()
    
    def destruct(self) -> None:
        """Reconstruct all childs for size reasons."""
        
        # Destruct tree

        self.entities = self._destruct()

        self.fix = True

        # Clear subtrees

        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None

        self.leaf = True
    
    def _destruct(self, __collector=[]) -> list[entity.Entity]:
        """Reconstruct all childs for size reasons."""

        # Collect entities

        __collector += self.entities

        if not self.leaf:

            self.up_left._destruct(__collector)
            self.up_right._destruct(__collector)
            self.down_left._destruct(__collector)
            self.down_right._destruct(__collector)
        
        return __collector
    
    def split(self) -> None:
        """Split the tree into quad subtrees."""

        # Create quadrants
        
        self.up_left = Quadtree(self.rect_up_left, self.capacity, False)
        self.up_right = Quadtree(self.rect_up_right, self.capacity, False)
        self.down_left = Quadtree(self.rect_down_left, self.capacity, False)
        self.down_right = Quadtree(self.rect_down_right, self.capacity, False)

        self.leaf = False

        # Clear entities
        
        entities = self.entities.copy()
        self.entities.clear()

        # Insert entities

        for en in entities:
            self.insert(en)

    def retrieve(self, en: entity.Entity) -> list[entity.Entity]:
        """Retrieve all possible colliders with an entity."""
    
        # Collect entities

        entities = []

        if not self.leaf:

            if self.rect_up_left.colliderect(en.rect):
                entities += self.up_left.retrieve(en)
            
            if self.rect_up_right.colliderect(en.rect):
                entities += self.up_right.retrieve(en)
            
            if self.rect_down_left.colliderect(en.rect):
                entities += self.down_left.retrieve(en)
            
            if self.rect_down_right.colliderect(en.rect):
                entities += self.down_right.retrieve(en)

        else:
            entities += self.entities
        
        return entities
    
    def clear(self) -> None:
        """
        Deletes all subtrees and elements to regenerate the quadrants
        """

        # Clear quadrants / entities

        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None

        self.fix = False
        self.leaf = True

        self.entities.clear()
    
    def print_(self):
        """Prints the collision handler structure."""

        self._print_()

    def _print_(self, __height: int = 0):
        """Prints the collision handler structure."""

        # Print entities

        indent = __height * "    "
        
        print(indent, self.rect, "fix" if self.fix else "")
        print(indent, self.entities)
            
        # Step down

        if not self.leaf:

            self.up_right._print_(__height + 1)
            self.up_left._print_(__height + 1)
            self.down_right._print_(__height + 1)
            self.down_left._print_(__height + 1)
    
    def lenght(self) -> int:
        """Returns the count of objects managed."""

        lenght = 0

        if not self.leaf:

            lenght += self.up_right.lenght()
            lenght += self.up_left.lenght()
            lenght += self.down_right.lenght()
            lenght += self.down_left.lenght()
        
        else:
            return len(self.entities)
        
        return lenght
    
    def render(
        self, en: entity.Entity | None = None
    ) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Renders a surface of quadrants for debugging."""
        
        # Prepare surface

        surface = pygame.Surface((272, 208), pygame.SRCALPHA)
        surface.convert_alpha()
        surface.fill([0, 0, 0, 0])

        # Draw rectangles
        
        return [(self._render(surface, en), (0, 0))]
    
    def _render(
        self, __surface, en: entity.Entity | None = None
    ) -> pygame.Surface:
        """Renders a surface of quadrants for debugging."""
        
        # Check collision (with debug object)

        collide = False

        if en:
            if self.leaf and self.rect.colliderect(en.rect):
                collide = True

        # Draw rect

        if collide:

            pygame.draw.rect(
                __surface, pygame.Color("Yellow"), self.rect, width=1
            )
        
        else:

            pygame.draw.rect(
                __surface, pygame.Color("Red"), self.rect, width=1
            )

        # Step down

        if not self.leaf:

            self.up_right._render(__surface, en)
            self.up_left._render(__surface, en)
            self.down_right._render(__surface, en)
            self.down_left._render(__surface, en)

        return __surface    
    
    def handle(self, entities: list[entity.Entity]) -> None:
        """Handle collisions in map."""

        for entity1 in entities:

            # Get possibilities

            entities2 = self.retrieve(entity1)

            for entity2 in entities2:

                # Not active

                if not (entity1.active and entity2.active):
                    continue

                # Same object

                if entity1 is entity2:
                    continue

                # Check collision

                if not entity1.rect.colliderect(entity2.rect):
                    continue

                # Player - Bullet

                if isinstance(entity1, objects.player.Player):
                    
                    if (
                        isinstance(entity2, objects.bullet.Bullet)
                        and entity2.fac == core.ENEMY
                    ):

                        entity1.update_health(-0.5)
                        entity2.active = False
                
                # Bullet - Archer
                
                if isinstance(entity2, objects.archer.Archer):

                    if (
                        isinstance(entity1, objects.bullet.Bullet)
                        and entity1.fac == core.FRIEND
                    ):
                        
                        entity1.active = False
                        entity2.update_health(-1)
                
                # Bullet - Wall
                
                if isinstance(entity1, objects.bullet.Bullet):
                    
                    if isinstance(
                        entity2, (
                            map.tiles.Block,
                            map.tiles.Edge,
                            map.tiles.Block,
                            map.tiles.Wall
                        )
                    ): # BUG

                        entity1.active = False
                
                # Player / Archer - Wall

                if isinstance(
                    entity1,
                    (objects.player.Player, objects.archer.Archer)
                ):
                    
                    if isinstance(
                        entity2, (
                            map.tiles.Block,
                            map.tiles.Edge,
                            map.tiles.Block,
                            map.tiles.Wall
                        )
                    ): # BUG

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
                        
                        if (
                            tmp_rect.contains(tmp_down)
                            and not tmp_rect.contains(tmp_left)
                            and not tmp_rect.contains(tmp_right)
                        ):
                            
                            dis = -entity1.y - entity1.h + entity2.y
                            entity1.y += dis
                        
                        if (
                            tmp_rect.contains(tmp_left)
                            and not tmp_rect.contains(tmp_up)
                            and not tmp_rect.contains(tmp_down)
                        ):
                            
                            dis = entity2.x + entity2.w - entity1.x
                            entity1.x += dis
                        
                        if (
                            tmp_rect.contains(tmp_right)
                            and not tmp_rect.contains(tmp_up)
                            and not tmp_rect.contains(tmp_down)
                        ):
                            
                            dis = -entity1.x - entity1.w + entity2.x
                            entity1.x += dis

if __name__ == "__main__":

    collision = Quadtree(pygame.Rect(0, 0, 500, 400), 3)

    entities = [
        entity.Entity(x=12, y=40, w=13, h=20, fac=core.FRIEND),
        entity.Entity(x=14, y=54, w=13, h=40, fac=core.ENEMY),
        entity.Entity(x=18, y=30, w=18, h=14, fac=core.FRIEND),
        entity.Entity(x=322, y=1, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=3, w=15, h=30, fac=core.ENEMY),
        entity.Entity(x=12, y=7, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=14, w=200, h=110, fac=core.ENEMY),
        entity.Entity(x=12, y=234, w=18, h=14, fac=core.FRIEND),
        entity.Entity(x=322, y=1, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=3, w=13, h=20, fac=core.ENEMY),
        entity.Entity(x=12, y=3, w=400, h=300, fac=core.ENEMY),
        entity.Entity(x=12, y=3, w=13, h=40, fac=core.ENEMY)
    ]

    [en.init_rect() for en in entities]

    for i, en in enumerate(entities):

        collision.insert(en)

        print()
        collision.print_()

        print()
        print("Inserted:", en.rect)
        print("Lenght:", collision.lenght())

        print("--------------------------------------------")

        # if i + 1 == 5: break
