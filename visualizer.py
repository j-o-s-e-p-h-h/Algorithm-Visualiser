import math
import random

import pygame


pygame.init()


class DrawInformation:
    BACKGROUND_COLOR = (10, 15, 24)
    SURFACE_COLOR = (19, 29, 42)
    PANEL_COLOR = (24, 36, 52)
    PANEL_EDGE_COLOR = (57, 89, 124)
    GRID_COLOR = (34, 50, 72)

    TEXT_COLOR = (241, 245, 249)
    MUTED_TEXT_COLOR = (145, 160, 182)
    ACCENT_COLOR = (91, 192, 255)
    SUCCESS_COLOR = (89, 214, 159)
    WARNING_COLOR = (255, 205, 112)
    DANGER_COLOR = (255, 130, 130)

    BAR_GRADIENTS = [
        (88, 149, 255),
        (95, 212, 186),
        (132, 169, 255),
    ]

    TITLE_FONT = pygame.font.SysFont("georgia", 42, bold=True)
    FONT = pygame.font.SysFont("verdana", 20)
    SMALL_FONT = pygame.font.SysFont("verdana", 15)

    SIDE_PAD = 120
    TOP_PAD = 220
    BOTTOM_PAD = 70

    def __init__(self, width, height, values):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        self.graph_width = self.width - self.SIDE_PAD
        self.graph_height = self.height - self.TOP_PAD - self.BOTTOM_PAD
        self.graph_top = self.TOP_PAD
        self.graph_bottom = self.height - self.BOTTOM_PAD
        self.start_x_coordinate = self.SIDE_PAD // 2

        self.set_list(values)

    def set_list(self, values):
        self.list = values
        self.max_value = max(values)
        self.min_value = min(values)

        value_range = self.max_value - self.min_value or 1
        self.block_width = max(1, math.floor(self.graph_width / len(values)))
        self.block_height = self.graph_height / value_range


def generate_starting_list(length, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(length)]


def should_swap(first, second, ascending):
    return (first > second and ascending) or (first < second and not ascending)


def get_bar_height(draw_info, value):
    if draw_info.max_value == draw_info.min_value:
        return max(12, draw_info.graph_height // 2)

    scaled_height = int((value - draw_info.min_value) * draw_info.block_height)
    return max(8, scaled_height)


def draw_stat_card(draw_info, label, value, x, y, width, accent_color):
    card_rect = pygame.Rect(x, y, width, 58)
    pygame.draw.rect(draw_info.window, draw_info.SURFACE_COLOR, card_rect, border_radius=18)
    pygame.draw.rect(draw_info.window, accent_color, card_rect, 2, border_radius=18)

    label_surface = draw_info.SMALL_FONT.render(label, True, draw_info.MUTED_TEXT_COLOR)
    value_surface = draw_info.FONT.render(value, True, draw_info.TEXT_COLOR)

    draw_info.window.blit(label_surface, (x + 14, y + 10))
    draw_info.window.blit(value_surface, (x + 14, y + 27))


def draw_list(draw_info, color_positions=None):
    if color_positions is None:
        color_positions = {}

    graph_rect = pygame.Rect(
        draw_info.start_x_coordinate - 18,
        draw_info.graph_top - 18,
        draw_info.graph_width + 36,
        draw_info.graph_height + 36,
    )
    pygame.draw.rect(draw_info.window, draw_info.SURFACE_COLOR, graph_rect, border_radius=24)
    pygame.draw.rect(draw_info.window, draw_info.PANEL_EDGE_COLOR, graph_rect, 1, border_radius=24)

    for row in range(6):
        y = draw_info.graph_top + row * draw_info.graph_height // 5
        pygame.draw.line(
            draw_info.window,
            draw_info.GRID_COLOR,
            (draw_info.start_x_coordinate, y),
            (draw_info.width - draw_info.SIDE_PAD // 2, y),
            1,
        )

    max_label = draw_info.SMALL_FONT.render(str(draw_info.max_value), True, draw_info.MUTED_TEXT_COLOR)
    min_label = draw_info.SMALL_FONT.render(str(draw_info.min_value), True, draw_info.MUTED_TEXT_COLOR)

    draw_info.window.blit(max_label, (16, draw_info.graph_top - 8))
    draw_info.window.blit(min_label, (16, draw_info.graph_bottom - min_label.get_height()))

    bar_width = max(1, draw_info.block_width - 1)

    for index, value in enumerate(draw_info.list):
        x = draw_info.start_x_coordinate + index * draw_info.block_width
        bar_height = get_bar_height(draw_info, value)
        y = draw_info.graph_bottom - bar_height

        color = color_positions.get(index, draw_info.BAR_GRADIENTS[index % len(draw_info.BAR_GRADIENTS)])
        border_radius = 4 if bar_width >= 4 else 0

        pygame.draw.rect(
            draw_info.window,
            color,
            (x, y, bar_width, bar_height),
            border_radius=border_radius,
        )


def draw(draw_info, algorithm_name, ascending, sorting, frame_rate, highlights=None):
    if highlights is None:
        highlights = {}

    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    header_rect = pygame.Rect(30, 28, draw_info.width - 60, 182)
    pygame.draw.rect(draw_info.window, draw_info.PANEL_COLOR, header_rect, border_radius=28)
    pygame.draw.rect(draw_info.window, draw_info.PANEL_EDGE_COLOR, header_rect, 2, border_radius=28)

    title_surface = draw_info.TITLE_FONT.render("Algorithm Visualizer", True, draw_info.TEXT_COLOR)
    subtitle_surface = draw_info.SMALL_FONT.render(
        "Clean visuals, live comparisons, and multiple classic sorting algorithms.",
        True,
        draw_info.MUTED_TEXT_COLOR,
    )

    status_text = f"{algorithm_name} | {'Ascending' if ascending else 'Descending'} | {'Sorting' if sorting else 'Ready'}"
    status_color = draw_info.WARNING_COLOR if sorting else draw_info.SUCCESS_COLOR
    status_surface = draw_info.FONT.render(status_text, True, status_color)

    draw_info.window.blit(title_surface, (54, 44))
    draw_info.window.blit(subtitle_surface, (56, 96))
    draw_info.window.blit(status_surface, (56, 126))

    stat_width = 150
    stat_gap = 12
    first_stat_x = draw_info.width - (stat_width * 3 + stat_gap * 2 + 48)

    draw_stat_card(
        draw_info,
        "Order",
        "Ascending" if ascending else "Descending",
        first_stat_x,
        52,
        stat_width,
        draw_info.ACCENT_COLOR,
    )
    draw_stat_card(
        draw_info,
        "Bars",
        str(len(draw_info.list)),
        first_stat_x + stat_width + stat_gap,
        52,
        stat_width,
        draw_info.SUCCESS_COLOR,
    )
    draw_stat_card(
        draw_info,
        "Speed",
        f"{frame_rate} FPS",
        first_stat_x + (stat_width + stat_gap) * 2,
        52,
        stat_width,
        draw_info.WARNING_COLOR,
    )

    controls_line_one = "SPACE start/pause   R reshuffle   A ascending   D descending"
    controls_line_two = "B bubble   I insertion   S selection   C cocktail   M merge   Q quick"
    controls_line_three = "UP more bars   DOWN fewer bars   LEFT slower   RIGHT faster"

    controls_surfaces = [
        draw_info.SMALL_FONT.render(controls_line_one, True, draw_info.MUTED_TEXT_COLOR),
        draw_info.SMALL_FONT.render(controls_line_two, True, draw_info.MUTED_TEXT_COLOR),
        draw_info.SMALL_FONT.render(controls_line_three, True, draw_info.MUTED_TEXT_COLOR),
    ]

    for row, surface in enumerate(controls_surfaces):
        draw_info.window.blit(surface, (56, 156 + row * 18))

    draw_list(draw_info, highlights)
    pygame.display.update()


def bubble_sort(draw_info, ascending=True):
    values = draw_info.list

    for end in range(len(values) - 1, 0, -1):
        for index in range(end):
            if should_swap(values[index], values[index + 1], ascending):
                values[index], values[index + 1] = values[index + 1], values[index]
                yield {index: draw_info.SUCCESS_COLOR, index + 1: draw_info.DANGER_COLOR}
            else:
                yield {index: draw_info.WARNING_COLOR, index + 1: draw_info.ACCENT_COLOR}


def insertion_sort(draw_info, ascending=True):
    values = draw_info.list

    for index in range(1, len(values)):
        current_value = values[index]
        position = index

        while position > 0 and should_swap(values[position - 1], current_value, ascending):
            values[position] = values[position - 1]
            yield {position - 1: draw_info.WARNING_COLOR, position: draw_info.DANGER_COLOR}
            position -= 1

        values[position] = current_value
        yield {position: draw_info.SUCCESS_COLOR, index: draw_info.ACCENT_COLOR}


def selection_sort(draw_info, ascending=True):
    values = draw_info.list

    for start in range(len(values)):
        selected_index = start

        for scan_index in range(start + 1, len(values)):
            if should_swap(values[selected_index], values[scan_index], ascending):
                selected_index = scan_index

            yield {
                start: draw_info.ACCENT_COLOR,
                selected_index: draw_info.WARNING_COLOR,
                scan_index: draw_info.DANGER_COLOR,
            }

        if selected_index != start:
            values[start], values[selected_index] = values[selected_index], values[start]
            yield {start: draw_info.SUCCESS_COLOR, selected_index: draw_info.DANGER_COLOR}


def cocktail_sort(draw_info, ascending=True):
    values = draw_info.list
    start = 0
    end = len(values) - 1
    swapped = True

    while swapped:
        swapped = False

        for index in range(start, end):
            if should_swap(values[index], values[index + 1], ascending):
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
                yield {index: draw_info.SUCCESS_COLOR, index + 1: draw_info.DANGER_COLOR}
            else:
                yield {index: draw_info.WARNING_COLOR, index + 1: draw_info.ACCENT_COLOR}

        if not swapped:
            break

        swapped = False
        end -= 1

        for index in range(end - 1, start - 1, -1):
            if should_swap(values[index], values[index + 1], ascending):
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
                yield {index: draw_info.SUCCESS_COLOR, index + 1: draw_info.DANGER_COLOR}
            else:
                yield {index: draw_info.WARNING_COLOR, index + 1: draw_info.ACCENT_COLOR}

        start += 1


def merge_sort(draw_info, ascending=True):
    values = draw_info.list
    yield from merge_sort_range(values, 0, len(values) - 1, ascending, draw_info)


def merge_sort_range(values, left, right, ascending, draw_info):
    if left >= right:
        return

    middle = (left + right) // 2
    yield from merge_sort_range(values, left, middle, ascending, draw_info)
    yield from merge_sort_range(values, middle + 1, right, ascending, draw_info)
    yield from merge(values, left, middle, right, ascending, draw_info)


def merge(values, left, middle, right, ascending, draw_info):
    left_values = values[left : middle + 1]
    right_values = values[middle + 1 : right + 1]

    left_index = 0
    right_index = 0
    merged_index = left

    while left_index < len(left_values) and right_index < len(right_values):
        left_value = left_values[left_index]
        right_value = right_values[right_index]

        if (left_value <= right_value and ascending) or (left_value >= right_value and not ascending):
            values[merged_index] = left_value
            left_index += 1
        else:
            values[merged_index] = right_value
            right_index += 1

        yield {
            merged_index: draw_info.SUCCESS_COLOR,
            left: draw_info.ACCENT_COLOR,
            right: draw_info.WARNING_COLOR,
        }
        merged_index += 1

    while left_index < len(left_values):
        values[merged_index] = left_values[left_index]
        yield {merged_index: draw_info.SUCCESS_COLOR, left: draw_info.ACCENT_COLOR}
        left_index += 1
        merged_index += 1

    while right_index < len(right_values):
        values[merged_index] = right_values[right_index]
        yield {merged_index: draw_info.SUCCESS_COLOR, right: draw_info.WARNING_COLOR}
        right_index += 1
        merged_index += 1


def quick_sort(draw_info, ascending=True):
    values = draw_info.list
    yield from quick_sort_range(values, 0, len(values) - 1, ascending, draw_info)


def quick_sort_range(values, low, high, ascending, draw_info):
    if low >= high:
        return

    pivot_index = yield from partition(values, low, high, ascending, draw_info)
    yield from quick_sort_range(values, low, pivot_index - 1, ascending, draw_info)
    yield from quick_sort_range(values, pivot_index + 1, high, ascending, draw_info)


def partition(values, low, high, ascending, draw_info):
    pivot_value = values[high]
    smaller_index = low

    for scan_index in range(low, high):
        yield {
            high: draw_info.WARNING_COLOR,
            scan_index: draw_info.ACCENT_COLOR,
            smaller_index: draw_info.SUCCESS_COLOR,
        }

        if (values[scan_index] <= pivot_value and ascending) or (
            values[scan_index] >= pivot_value and not ascending
        ):
            values[smaller_index], values[scan_index] = values[scan_index], values[smaller_index]
            yield {
                smaller_index: draw_info.SUCCESS_COLOR,
                scan_index: draw_info.DANGER_COLOR,
                high: draw_info.WARNING_COLOR,
            }
            smaller_index += 1

    values[smaller_index], values[high] = values[high], values[smaller_index]
    yield {smaller_index: draw_info.SUCCESS_COLOR, high: draw_info.DANGER_COLOR}
    return smaller_index


SORTING_ALGORITHMS = {
    pygame.K_b: ("Bubble Sort", bubble_sort),
    pygame.K_i: ("Insertion Sort", insertion_sort),
    pygame.K_s: ("Selection Sort", selection_sort),
    pygame.K_c: ("Cocktail Sort", cocktail_sort),
    pygame.K_m: ("Merge Sort", merge_sort),
    pygame.K_q: ("Quick Sort", quick_sort),
}


def main():
    clock = pygame.time.Clock()

    list_size = 72
    min_value = 10
    max_value = 500
    frame_rate = 90

    values = generate_starting_list(list_size, min_value, max_value)
    draw_info = DrawInformation(1280, 760, values)

    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None
    highlights = {}

    run = True
    while run:
        clock.tick(frame_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                values = generate_starting_list(list_size, min_value, max_value)
                draw_info.set_list(values)
                sorting = False
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_SPACE:
                if sorting:
                    sorting = False
                else:
                    if sorting_algorithm_generator is None:
                        sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                    sorting = True
            elif event.key == pygame.K_a and not sorting:
                ascending = True
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_d and not sorting:
                ascending = False
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_UP and not sorting:
                list_size = min(180, list_size + 10)
                values = generate_starting_list(list_size, min_value, max_value)
                draw_info.set_list(values)
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_DOWN and not sorting:
                list_size = max(20, list_size - 10)
                values = generate_starting_list(list_size, min_value, max_value)
                draw_info.set_list(values)
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_RIGHT:
                frame_rate = min(240, frame_rate + 15)
            elif event.key == pygame.K_LEFT:
                frame_rate = max(15, frame_rate - 15)
            elif event.key in SORTING_ALGORITHMS and not sorting:
                sorting_algorithm_name, sorting_algorithm = SORTING_ALGORITHMS[event.key]
                sorting_algorithm_generator = None
                highlights = {}

        if sorting and sorting_algorithm_generator is not None:
            try:
                highlights = next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                sorting_algorithm_generator = None
                highlights = {}
        else:
            highlights = {}

        draw(draw_info, sorting_algorithm_name, ascending, sorting, frame_rate, highlights)

    pygame.quit()


if __name__ == "__main__":
    main()
