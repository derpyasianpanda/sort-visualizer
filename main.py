import numpy
import pygame
import math
import random
import os
import sys
import time
import colorsys
import concurrent.futures


class Tile:
    def __init__(self, coord1, coord2=0, color=[0, 0, 0]):
        if isinstance(coord1, int):
            self.x = coord1
            self.y = coord2
        else:
            self.x, self.y = coord1
        self.coord = [self.x, self.y]
        self.color = self.update_color(color)
        r, g, b = self.color
        self.hue = int(colorsys.rgb_to_hsv(r, g, b)[0] * 360)

    def __repr__(self):
        return f"Tile at {self.x}, {self.y} with {self.hue} degree"

    def update_color(self, color):
        try:
            if self.color != color:
                time.sleep(step_time)
        except AttributeError:
            pass
        self.color = color
        pygame.draw.rect(screen, color, (self.x * tile_width, self.y * tile_height, tile_width, tile_height))
        pygame.display.update((self.x * tile_width, self.y * tile_height, tile_width, tile_height))
        r, g, b = self.color
        self.hue = int(colorsys.rgb_to_hsv(r, g, b)[0] * 360)
        return self.color


def selection_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(selection_sort_helper, y)


def selection_sort_helper(y):
    for x in range(grid_width):
        min_x = x
        for next_x in range(x + 1, grid_width):
            if grid[min_x, y].hue > grid[next_x, y].hue:
                min_x = next_x
        swap(grid[x, y], grid[min_x, y])


def insertion_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(insertion_sort_helper, y)


def insertion_sort_helper(y):
    for x in range(1, grid_width):
        current_hue = grid[x, y].hue
        current_color = grid[x, y].color
        x_before = x - 1
        while x_before >= 0 and current_hue < grid[x_before, y].hue:
            grid[x_before + 1, y].update_color(grid[x_before, y].color)
            x_before -= 1
        grid[x_before + 1, y].update_color(current_color)


def bubble_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(bubble_sort_helper, y)


def bubble_sort_helper(y):
    for x in range(grid_width):
        swapped = False
        for current_x in range(0, grid_width - x - 1):
            if grid[current_x, y].hue > grid[current_x + 1, y].hue:
                swap(grid[current_x, y], grid[current_x + 1, y])
                swapped = True

        if not swapped:
            break


def merge_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(merge_sort_helper, range(0, grid_width), y)


def merge_sort_helper(indices, row):
    if len(indices) > 1:
        mid = len(indices) // 2
        left = indices[:mid]
        right = indices[mid:]

        merge_sort_helper(left, row)
        merge_sort_helper(right, row)
        left = [[grid[index, row].color, grid[index, row].hue] for index in left]
        right = [[grid[index, row].color, grid[index, row].hue] for index in right]

        cur_l = cur_r = cur_overall = 0

        while cur_l < len(left) and cur_r < len(right):
            if left[cur_l][1] < right[cur_r][1]:
                grid[indices[cur_overall], row].update_color(left[cur_l][0])
                cur_l += 1
            else:
                grid[indices[cur_overall], row].update_color(right[cur_r][0])
                cur_r += 1
            cur_overall += 1

        while cur_l < len(left):
            grid[indices[cur_overall], row].update_color(left[cur_l][0])
            cur_l += 1
            cur_overall += 1

        while cur_r < len(right):
            grid[indices[cur_overall], row].update_color(right[cur_r][0])
            cur_r += 1
            cur_overall += 1


def quick_sort_last():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(quick_sort_last_helper, 0, grid_width - 1, y)


def quick_sort_last_helper(first_index, last_index, row):
    if first_index < last_index:
        partition_index = partition_last(first_index, last_index, row)
        quick_sort_last_helper(first_index, partition_index - 1, row)
        quick_sort_last_helper(partition_index + 1, last_index, row)


def partition_last(first_index, last_index, row):
    pivot = grid[last_index, row]
    smaller_index = first_index - 1

    for current_index in range(first_index, last_index):
        if grid[current_index, row].hue < pivot.hue:
            smaller_index += 1
            swap(grid[smaller_index, row], grid[current_index, row])
    swap(grid[smaller_index + 1, row], grid[last_index, row])
    return smaller_index + 1


def quick_sort_random():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(quick_sort_random_helper, 0, grid_width - 1, y)


def quick_sort_random_helper(first_index, last_index, row):
    if first_index < last_index:
        partition_index = partition_random_r(first_index, last_index, row)
        quick_sort_random_helper(first_index, partition_index - 1, row)
        quick_sort_random_helper(partition_index + 1, last_index, row)


def partition_random_r(first_index, last_index, row):
    random_pivot = random.randrange(first_index, last_index)
    swap(grid[first_index, row], grid[random_pivot, row])
    return partition_random(first_index, last_index, row)


def partition_random(first_index, last_index, row):
    pivot = grid[first_index, row]
    smaller_index = first_index + 1

    for current_index in range(first_index + 1, last_index + 1):
        if grid[current_index, row].hue < pivot.hue:
            swap(grid[smaller_index, row], grid[current_index, row])
            smaller_index += 1
    swap(pivot, grid[smaller_index - 1, row])
    return smaller_index - 1


def multi_algorithm():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(0, grid_height, 4):
            executor.submit(bubble_sort_helper, y)
            executor.submit(insertion_sort_helper, y + 1)
            executor.submit(merge_sort_helper, list(range(0, grid_width)), y + 2)
            executor.submit(selection_sort_helper, y + 3)


def bucket_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(bucket_sort_helper, y)


def bucket_sort_helper(row):
    sorted_references = []
    buckets = int(grid_width ** .5)

    for i in range(buckets):
        sorted_references.append([])

    for x in range(grid_width):
        sorted_references[int(buckets * (grid[x, row].hue / 360))].append(grid[x, row])

    for j in range(buckets):
        insertion_sort_bucket(sorted_references[j], row)

    for j in range(buckets):
        sorted_references[j] = [tile.color for tile in sorted_references[j]]

    x = 0
    for i in range(buckets):
        for j in range(len(sorted_references[i])):
            grid[x, row].update_color(sorted_references[i][j])
            x += 1


def radix_sort():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for y in range(grid_height):
            executor.submit(radix_sort_helper, y)


def radix_sort_helper(row):
    references = []
    for x in range(grid_width):
        references.append(grid[x, row])

    maximum = max([tile.hue for tile in references])
    exp = 1
    while maximum // exp > 0:
        counting_sort(exp, references)
        exp *= 10


def counting_sort(place, references):

    output = [0] * len(references)
    count = [0] * 10

    for i in range(len(references)):
        index = references[i].hue // place
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(len(references) - 1, -1, -1):
        index = references[i].hue // place
        output[count[index % 10] - 1] = references[i]
        count[index % 10] -= 1

    output = [tile.color for tile in output]

    for i in range(0, len(references)):
        references[i].update_color(output[i])


def insertion_sort_bucket(arr, row):
    for index in range(1, len(arr)):
        current_hue = arr[index].hue
        current_color = arr[index].color
        last_index = index - 1
        while last_index >= 0 and current_hue < arr[last_index].hue:
            grid[arr[last_index + 1].x, row].update_color(arr[last_index].color)
            last_index -= 1
        grid[arr[last_index + 1].x, row].update_color(current_color)


def swap(tile1, tile2):
    temp = tile2.color[:]
    tile2.update_color(tile1.color)
    tile1.update_color(temp)


def change_sort(index):
    global current_sort_index
    if index == "next":
        if current_sort_index >= len(sorts) - 1:
            current_sort_index = 0
        else:
            current_sort_index += 1
    elif index == "back":
        if current_sort_index <= 0:
            current_sort_index = len(sorts) - 1
        else:
            current_sort_index += -1
    else:
        current_sort_index = index
    pygame.display.set_caption(f"{sort_names[current_sort_index]} Sort")


def change_increment(index):
    global current_increment_index, grid_width, display_width, tile_width, tile_height, screen, colors, grid
    if index == "next":
        if current_increment_index >= len(increments) - 1:
            current_increment_index = 0
        else:
            current_increment_index += 1
    elif index == "back":
        if current_increment_index <= 0:
            current_increment_index = len(increments) - 1
        else:
            current_increment_index += -1
    else:
        current_increment_index = index
    grid_width = 255 // increments[current_increment_index][0] * 6
    display_width = increments[current_increment_index][1]
    tile_width = display_width // grid_width
    tile_height = display_height // grid_height
    screen = pygame.display.set_mode((display_width, display_height))
    colors = make_colors()
    grid = make_board()


def make_colors():
    result = []
    for i in range(3):
        for j in range(3):
            temp_color = [0, 0, 0]
            temp_color[i] = 255
            if j != i:
                for k in range(0, 256, increments[current_increment_index][0]):
                    temp_color[j] = k
                    if temp_color not in result:
                        result.append(temp_color[:])
    print(len(result))
    return result


def make_board():
    result_grid = numpy.empty((grid_width, grid_height), object)
    for y in range(grid_height):
        temp = colors[:]
        for x in range(grid_width):
            result_grid[x, y] = Tile(x, y, temp.pop(random.randint(0, len(temp) - 1)))
    return result_grid


sort_names = [
    "Selection",
    "Insertion",
    "Bubble",
    "Merge",
    "Quick (Last Item Pivot)",
    "Quick (Random Item Pivot)",
    "Bucket",
    "Radix",
    "Multi-Algorithm"
]
sorts = [
    selection_sort,
    insertion_sort,
    bubble_sort,
    merge_sort,
    quick_sort_last,
    quick_sort_random,
    bucket_sort,
    radix_sort,
    multi_algorithm
]
increments = [
    [85, 360],
    [51, 600],
    [17, 900],
    [15, 918],
    [5, 918],
    [3, 1020]
]

current_increment_index = 0

grid_width = 255 // increments[current_increment_index][0] * 6
grid_height = 8
display_width = increments[current_increment_index][1]
display_height = 360
tile_width = display_width // grid_width
tile_height = display_height // grid_height

default_step_time = 1 / 500
step_show = True
step_time = default_step_time

max_threads = 4
os.environ['SDL_VIDEO_CENTERED'] = "0"
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

current_sort_index = 0
pygame.display.set_caption(f"{sort_names[current_sort_index]} Sort")

colors = make_colors()

grid = make_board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                print("Resetting Board")
                grid = make_board()
                print("Board Reset")
            if event.key == pygame.K_RETURN:
                print("Sorting")
                start = time.time()
                sorts[current_sort_index]()
                elapsed = time.time() - start
                print(f"Sorted in {elapsed} second(s)")
            if event.key == pygame.K_RIGHT:
                change_sort("next")
            if event.key == pygame.K_LEFT:
                change_sort("back")
            if event.key == pygame.K_UP:
                change_increment("next")
            if event.key == pygame.K_DOWN:
                change_increment("back")
            if event.key == pygame.K_s:
                step_show = not step_show
                step_time = default_step_time if step_show else 0
                print(f"Showing steps is {step_show}")
    pygame.display.flip()
