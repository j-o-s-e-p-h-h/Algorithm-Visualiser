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

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting", 1, draw_info.BLACK) 
    
    #displaying and centering the font
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 5)) 

    direction = draw_info.FONT.render("A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(direction, (draw_info.width/2 - direction.get_width()/2, 40))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK) 
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))         

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_background=False):
    list = draw_info.list

    if clear_background:
        clear_rectangle = (draw_info.side_pad//2, draw_info.top_pad, draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rectangle)

    for i, value in enumerate(list):
        x = draw_info.start_x_coordinate + i * draw_info.block_width
        y = draw_info.height - (value - draw_info.min_value) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_background:
        pygame.display.update()


def generate_starting_list(n, min_value, max_value):
    list = []

    for _ in range(n):
        value = random.randint(min_value, max_value)
        list.append(value)

    return list


def bubble_sort(draw_info , ascending=True):
    list = draw_info.list

    for i in range(len(list)- 1):
        for j in range(len(list) - 1- i):
            num1 = list[j]
            num2 = list[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                list[j], list[j + 1] = list[j + 1], list[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
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

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None


    while run:
        #framerate
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False

        else:
            draw(draw_info)

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
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending  = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
                
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()
    
