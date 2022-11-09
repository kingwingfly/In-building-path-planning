import queue

import numpy as np
import model


def my_map(height, width):
    print(height, width)
    return np.ones([height, width])


class graph:
    def __init__(self, height, width, file):
        self.my_map = my_map(height, width)
        with open('data/cost_map.txt', 'r', encoding='utf-8') as f:
            t = f.read()
            lst = []
            for i in t[1:-1:]:
                if i == '[':
                    lst.append([])
                elif i == '1':
                    lst[-1].append(1)
                elif i == 'i':
                    lst[-1].append(float('inf'))
            self.cost_map = np.array(lst)
        self.height, self.width = height, width

    def neighbors(self, point: tuple):
        x = point[0]
        y = point[1]
        x1 = x - 1 if x > 0 else 0
        x2 = x + 1 if x < self.height - 1 else self.height - 1
        y1 = y - 1 if y > 0 else 0
        y2 = y + 1 if y < self.width - 1 else self.width - 1
        lst1 = [(x1, y1), (x1, y), (x1, y2), (x, y1), (x, y2), (x2, y1), (x2, y), (x2, y2)]
        lst = []
        for i in lst1:
            if i not in lst and i != point:
                lst.append(i)
        return lst

    def cost(self, current, next_point):
        return ((current[0] - next_point[0]) ** 2 + (current[1] - next_point[1]) ** 2) ** 0.5 * \
               0.5 * (self.cost_map[current] + self.cost_map[next_point])


def heuristic(next_point, goal):
    return abs(next_point[0] - goal[0]) + abs(next_point[1] - goal[1])


def astar(graph, start, goal):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while not frontier.empty():
        current = frontier.get()[1]
        if current == goal:
            break
        for next_point in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_point)
            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost + heuristic(next_point, goal)
                frontier.put((priority, next_point))
                came_from[next_point] = current
    return came_from, cost_so_far


def astar_search(height, width, start, goal, file):
    graph1 = graph(height, width, file)
    came_from, cost_so_far = astar(graph1, start, goal)
    way = []
    while True:
        way.append(goal)
        if goal == start:
            break
        goal = came_from[goal]
    print(cost_so_far[goal])
    return way[::-1]


if __name__ == '__main__':
    height, width = 100, 100
    start, goal = (0, 0), (99, 99)
    file = 'data/sj_test.csv'
    way = astar_search(height, width, start, goal, file)
    print(way)
