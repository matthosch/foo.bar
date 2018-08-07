from heapq import heappop, heappush
from copy import deepcopy

def answer(maze):
    output = []
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            temp = deepcopy(maze)
            if maze[y][x] == 1:
                temp[y][x] = 0
                output.append(find_path_astar(temp))
    return min(output)

def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not maze[row][col + 1]:
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph

def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def find_path_astar(maze):
    start, goal = (0, 0), (len(maze) - 1, len(maze[0]) - 1)
    pr_queue = []
    heappush(pr_queue, (0 + heuristic(start, goal), 0, "", start))
    visited = set()
    graph = maze2graph(maze)
    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return len(path) + 1
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            heappush(pr_queue, (cost + heuristic(neighbour, goal), cost + 1,
                                path + direction, neighbour))
    return 0
    

maze_1 = [[0, 1, 1, 0], 
          [0, 0, 0, 1], 
          [1, 1, 0, 0], 
          [1, 1, 1, 0]]

maze_2 = [[0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1], 
          [0, 1, 1, 1, 1, 1], 
          [0, 0, 0, 0, 0, 0]]

#print find_path_astar(maze_1)
#print find_path_astar(maze_2)
print answer(maze_1)
print answer(maze_2)