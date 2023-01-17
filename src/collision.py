import pygame

import entity
import core
import objects.player
import objects.archer


class Quadtree:
    """A class for quad tree collision handle."""

    def __init__(
        self, rect: pygame.Rect, capacity: int, root: bool = False, **kwargs
    ):
        
        self.root = root
        self.capacity = capacity
        self.entities = []
        self.leaf = True

        self.rect = rect
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
        
        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None
    
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
            #     if not self.root:
            #         self.reconstruct()

        else:

            self.entities += [en]

            if len(self.entities) > self.capacity:
                self.split()
    
    def reconstruct(self) -> None:
        """Reconstruct all childs for size reasons."""

        entities = self._reconstruct()
        self.capacity = max( len(entities) + 1, self.capacity )

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
        
        self.up_left = Quadtree(self.rect_up_left, self.capacity)
        self.up_right = Quadtree(self.rect_up_right, self.capacity)
        self.down_left = Quadtree(self.rect_down_left, self.capacity)
        self.down_right = Quadtree(self.rect_down_right, self.capacity)

        self.leaf = False

        for en in self.entities:

            if self.rect_up_left.contains(en.rect):
                self.up_left.insert(en)
            
            elif self.rect_up_right.contains(en.rect):
                self.up_right.insert(en)
            
            elif self.rect_down_left.contains(en.rect):
                self.down_left.insert(en)
            
            elif self.rect_down_right.contains(en.rect):
                self.down_right.insert(en)
        
        self.entities.clear()

    def retrieve(self, en: entity.Entity) -> list[entity.Entity]:
        """Retrieve all possible colliders with an entity."""

        if not self.leaf:

            if self.rect_up_left.colliderect(en.rect):
                return self.up_left.retrieve(en)
            
            elif self.rect_up_right.colliderect(en.rect):
                return self.up_right.retrieve(en)
            
            elif self.rect_down_left.colliderect(en.rect):
                return self.down_left.retrieve(en)
            
            elif self.rect_down_right.colliderect(en.rect):
                return self.down_right.retrieve(en)
            
            else:
                return []

        else:
            return self.entities
    
    def clear(self) -> None:
        """
        Deletes all subtrees and elements to regenerate the quadrants
        """

        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None

        self.leaf = True

        self.entities.clear()

    def _print(self, __height=0):

        print(__height * "  ", self.entities)

        if self.up_right:

            self.up_right._print(__height + 1)
            self.up_left._print(__height + 1)
            self.down_right._print(__height + 1)
            self.down_left._print(__height + 1)
    
    def handle(self, entities: entity.Entity) -> None:
        """Handle collisions in map."""

        for entity1 in entities:

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

    collision = Quadtree(0, 0, 500, 400, 2)

    entities = [
        entity.Entity(x=12, y=234, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=54, w=13, h=14, fac=core.ENEMY),
        entity.Entity(x=12, y=234, w=18, h=14, fac=core.FRIEND),
        entity.Entity(x=322, y=1, w=13, h=14, fac=core.FRIEND),
        entity.Entity(x=12, y=3, w=300, h=300, fac=core.ENEMY), #
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

        if i == 5: break
    
    collision._print()
    print("--------------------------------------------")