from heapq import heappop, heappush
import curses

class Node:
    def __init__(self, coord, vertical):
        self.coord = coord
        self.vertical = vertical

    def __str__(self):
        return f"{self.coord}, {self.vertical}"

    def __gt__(self, other):
        return abs(self.coord) > abs(other.coord)

    def __lt_(self, other):
        return abs(self.coord) < abs(other.coord)

    def __eq__(self, other):
        return self.coord == other.coord and self.vertical == other.vertical

    def __hash__(self):
        return hash((self.coord, self.vertical))

def parse_data():
    maze_string = open("input-data/day16.txt").read()
    return {x + 1j * y: val for y, line in enumerate(maze_string.split("\n"))
       for x, val in enumerate(line)}


class Printer:
    """Displays progress when solving
    If the maze can't find in the terminal, it'll only display the top left
    It's a bit lazy, but I wrote it for fun in a few minutes"""
    def __init__(self, width, height, stdscr: curses.window=None):
        self.screen = stdscr
        if stdscr == None:
            return
        self.pad = curses.newpad(width+1, height+1)
        self.width = width
        self.height = height
        self.screen = stdscr
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.min_row = 0
        self.prev_visited = None
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
    def print_initial(self, maze, start_coord):
        if self.screen == None:
            return
        self.prev_visited = start_coord
        for y in range(self.height):
            for x in range(self.width):
                char = maze[x+1j*y]
                self.pad.addch(y, x, char)
        self.pad.refresh(self.min_row,0, 0,0, self.max_y-1, self.max_x-1)

    def update(self, current_node):
        if self.screen == None:
            return
        prev_x = int(self.prev_visited.coord.real)
        prev_y = int(self.prev_visited.coord.imag)
        current_x = int(current_node.coord.real)
        current_y = int(current_node.coord.imag)
        self.pad.addch(prev_y, prev_x, "X", curses.color_pair(2))
        self.pad.addch(current_y, current_x, "O", curses.color_pair(1))
        self.pad.refresh(self.min_row,0, 0,0, self.max_y-1, self.max_x-1)
        self.prev_visited = current_node
        
    def print_result(self, result, nodes_visited):
        if self.screen == None:
            print(f"Result: {result}")
            return
        max_y, max_x = self.screen.getmaxyx()
        self.screen.addstr(max_y-3, 0, f"Result found: {result}")
        self.screen.addstr(max_y-2, 0, f"Nodes visited: {nodes_visited}/{self.width*self.height*2}")
        self.screen.addstr(max_y-1, 0, f"Color: {curses.has_colors()}")
        self.screen.refresh()
        self.pad.refresh(0,0, 0,0, max_y-4, max_x-1)

MOVE_COST = 1
TURN_COST = 1000

def part_one(stdscr=None):
    maze = parse_data()
    start_point = next(x for x in maze.keys() if maze[x] == "S")
    visited = {Node(x, True): False for x in maze.keys()}
    visited.update({Node(x, False): False for x in maze.keys()})
    nodes = []
    first_node = Node(start_point, False)
    heappush(nodes, (0, first_node))
    maze_width = int(max(maze.keys(), key=lambda x: x.real).real) + 1
    maze_height = int(max(maze.keys(), key=lambda x: x.imag).imag) + 1
    printer = Printer(maze_width, maze_height, stdscr)
    printer.print_initial(maze, first_node)
    while nodes:
        cost, vertex = heappop(nodes)
        visited[vertex] = True
        if maze[vertex.coord] == "#":
            continue
        elif maze[vertex.coord] == "E":
            nodes_visited = len([x for x in visited.items() if x[1]])
            printer.print_result(cost, nodes_visited)
            break
        if printer:
            printer.update(vertex)
        other_axis = Node(vertex.coord, not vertex.vertical)
        if visited[other_axis] == False:
            heappush(nodes, (cost+TURN_COST, other_axis))
        direction = 1j if vertex.vertical else 1
        for new_node in [Node(vertex.coord + direction, vertex.vertical), 
                         Node(vertex.coord - direction, vertex.vertical)]:
            if visited[new_node] == False:
                heappush(nodes, (cost + MOVE_COST, new_node))

def display_part_one(stdscr):
    screen = stdscr
    curses.cbreak()
    screen.clear()
    part_one(screen)
    screen.getkey()
    curses.nocbreak()
    curses.endwin()

if __name__ == "__main__":
    # uncomment below for visualisation
    # curses.wrapper(display_part_one)
    part_one()