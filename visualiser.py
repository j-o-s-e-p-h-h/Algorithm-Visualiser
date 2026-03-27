import pygame
import random 

pygame.init()

class DrawInformation:
    #defining colours
    BLACK = 0, 0, 0
    WHITE = 0, 255, 0
    GREEN = 255, 0, 0
    RED = 128, 128, 128

    def __init__(self, width, height, list):
        self.width = width 
        self.height = height 
        self.window = pygame.set_mode((width, height))
        pygame.display.set_caption("Sorting Algoithm Visualizer")
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.max_value = max(list)
        self.min_value = min(list)

        