import pygame

import core


class Entity:

    max_id = 0

    def __init__(self):
        
        Entity.max_id += 1
        self.id = Entity.max_id