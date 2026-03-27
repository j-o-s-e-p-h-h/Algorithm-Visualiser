import pygame
import random 

pygame.init()

class DrawInformation:
    #defining colours
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 255, 0
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [(128, 128, 128),
                 (160, 160, 160),
                 (192, 192,192)]
    #displaying of controls
    FONT = pygame.font.SysFont('comicsans', 30)
    large_font = pygame.font.SysFont('comicsans', 40)

    #explain later
    side_pad = 100 
    top_pad = 150

    def __init__(self, width, height, list):
        self.width = width 
        self.height = height 
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algoithm Visualizer")
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.max_value = max(list)
        self.min_value = min(list)

        #calculating size of each block based off of total num of blocks
        self.block_width = round((self.width - self.side_pad) / len(list))
        self.block_height = round((self.height - self.top_pad) / (self.max_value - self.min_value))
        
        #where to start drawing blocks
        self.start_x_coordinate = self.side_pad // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK) 
    #displaying and centering the font
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5)) 

    sorting = draw_info.FONT.render("I - Insertion Sort | b - Bubble Sort", 1, draw_info.BLACK) 
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 35))         

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info):
    list = draw_info.list

    for i, value in enumerate(list):
        x = draw_info.start_x_coordinate + i * draw_info.block_width
        y = draw_info.height - (value - draw_info.min_value) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))


def generate_starting_list(n, min_value, max_value):
    list = []

    for _ in range(n):
        value = random.randint(min_value, max_value)
        list.append(value)

    return list
def main():
    run = True 
    #clock to regulate how quickly loop can run for
    clock = pygame.time.Clock()

    n = 50 
    min_value = 0 
    max_value = 100
    list = generate_starting_list(n, min_value, max_value)
    draw_info = DrawInformation(800, 600, list)
    sorting = False
    ascending = True


    while run:
        clock.tick(120)

        draw(draw_info) 

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = generate_starting_list(n, min_value, max_value)
                draw_info.set_list(list)
                sorting = False 
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting  = True
            elif event.key == pygame.K_a and not sorting:
                ascending  = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
                
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()
    
