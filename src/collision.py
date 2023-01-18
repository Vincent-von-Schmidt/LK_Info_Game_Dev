import pygame

import entity
import core
import objects.player
import objects.archer
import objects.bullet


class Quadtree:
    """A class for quad tree collision handle."""

    def __init__(
        self, rect: pygame.Rect, capacity: int, root: bool = False, **kwargs
    ):
        
        self.root = root
        self.capacity = capacity

        # Init self

        self.entities = []
        self.leaf = True

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
            
            # else:
            #     self.reconstruct()

        # Split quadrant

        else:

            self.entities += [en]

            if len(self.entities) > self.capacity:
                self.split()
    
    def reconstruct(self) -> None:
        """Reconstruct all childs for size reasons."""

        # Deconstruct

        entities = self._reconstruct()

        if self.root:
            self.capacity = len(entities) + 1

        # Reconstruct

        for en in entities:
            self.insert(en)
    
    def _reconstruct(self) -> list[entity.Entity]:
        """Reconstruct all childs for size reasons."""

        # Collect entities

        entities = []

        if self.leaf:
            return self.entities

        else:

            entities += self.up_left._reconstruct()
            entities += self.up_right._reconstruct()
            entities += self.down_left._reconstruct()
            entities += self.down_right._reconstruct()
        
        # Clear subtrees

        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None

        self.leaf = True
        
        return entities
    
    def split(self) -> None:
        """Split the tree into quad subtrees."""

        # Create quadrants
        
        self.up_left = Quadtree(self.rect_up_left, self.capacity)
        self.up_right = Quadtree(self.rect_up_right, self.capacity)
        self.down_left = Quadtree(self.rect_down_left, self.capacity)
        self.down_right = Quadtree(self.rect_down_right, self.capacity)

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

        self.leaf = True

        self.entities.clear()
    
    def print_(self):
        """Prints the collision handler structure."""

        self._print_()

    def _print_(self, __height=0):
        """Prints the collision handler structure."""

        # Print entities

        print(__height * "  ", self.entities)

        # Step down

        if not self.leaf:

            self.up_right._print_(__height + 1)
            self.up_left._print_(__height + 1)
            self.down_right._print_(__height + 1)
            self.down_left._print_(__height + 1)
    
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

            self.up_right._render(__surface)
            self.up_left._render(__surface)
            self.down_right._render(__surface)
            self.down_left._render(__surface)

        return __surface    
    
    def handle(self, entities: entity.Entity) -> None:
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
                        continue
                
                # Bullet - Archer
                
                if isinstance(entity2, objects.archer.Archer):

                    if (
                        isinstance(entity1, objects.bullet.Bullet)
                        and entity1.fac == core.FRIEND
                    ):
                        
                        entity1.active = False
                        entity2.update_health(-1)
                        continue
                
                # Bullet - Wall
                
                if isinstance(entity1, objects.bullet.Bullet):
                    if entity2.fac == core.MAP:

                        entity1.active = False
                        continue
                
                # Player / Archer - Wall

                if isinstance(
                    entity1,
                    (objects.player.Player, objects.archer.Archer)
                ):
                    if entity2.fac == core.MAP:
                        
                        # BUG

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

if __name__ == "__main__":

    collision = Quadtree(pygame.Rect(0, 0, 500, 400), 2, True)

    entities = [
        entity.Entity(x=12, y=234, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=54, w=13, h=14, fac=core.ENEMY),
        entity.Entity(x=12, y=234, w=18, h=14, fac=core.FRIEND),
        entity.Entity(x=322, y=1, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=3, w=300, h=300, fac=core.ENEMY),
        entity.Entity(x=12, y=234, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=54, w=13, h=14, fac=core.ENEMY),
        entity.Entity(x=12, y=234, w=18, h=14, fac=core.FRIEND),
        entity.Entity(x=322, y=1, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=3, w=13, h=20, fac=core.ENEMY),
        entity.Entity(x=12, y=3, w=13, h=40, fac=core.ENEMY),
        entity.Entity(x=12, y=3, w=13, h=40, fac=core.ENEMY)
    ]

    for i, en in enumerate(entities):
        
        collision.insert(en)

        if i == 2: break
    
    collision.print_()
    print("--------------------------------------------")