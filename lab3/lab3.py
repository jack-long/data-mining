import random


edges_size = 100
wedges_size = 100

edges = []
wedges = [None] * wedges_size

is_closed = [False] * wedges_size

p = 0
k = 3 * p

t = 0


def total_wedges(edges):
    counter = 0
    for index, edge_i in enumerate(edges):
        for edge_j in edges[index + 1:]:
            if set(edge_j).intersection(edge_i):
                counter += 1
    return counter


def calculate_triangle(t):
    p = is_closed.count(True)
    return [p * t * t / edges_size * (edges_size-1)] * total_wedges(edges)


def keep(n, edges_size):
    return random.randint(1, n) < edges_size


def insert_edge(edge, edges):
    if len(edges) <= 100:
        edges.append(edge)
    else:
        index = random.randint(1, len(edges))
        edges[index - 1] = edge


def get_wedges(edge, edges):
    new_wedges = []
    for each in edges:
        wedge = []
        if edge[0] == each[0]:
            wedge = [each[1], edge[1]] if int(each[1]) < int(edge[1]) else [edge[1], each[1]]
            wedge.append(edge[0])
        if edge[0] == each[1]:
            wedge = [each[0], edge[1], edge[0]]
        if edge[1] == each[0]:
            wedge = [edge[0], each[1], each[0]]
        if edge[1] == each[1]:
            wedge = [each[0], edge[0]] if int(each[0]) < int(edge[0]) else [edge[0], each[0]]
            wedge.append(edge[1])
        if wedge:
            new_wedges.append(wedge)
    # print "new wedge", new_wedges
    return new_wedges


def check_close(edge, wedges, is_closed):
    for index, wedge in enumerate(wedges):
        if wedge is None:
            continue
        if edge == wedge[:2]:
            is_closed[index] = True
            print wedge[0] + '-' + wedge[2], wedge[1] + '-' + wedge[2]


def update_wedges(new_wedges, wedges):
    current_wedges = total_wedges(edges)
    for index in range(wedges_size):
        if random.randint(0, current_wedges) < len(new_wedges):
            choice = random.randint(1, len(new_wedges))
            wedge = new_wedges[choice - 1]
            wedges[index] = wedge
            if not wedge:
                print "update", wedge, new_wedges
            is_closed[index] = False


with open("data/ego-facebook") as f:
    stream = f.readlines()
    for n, line in enumerate(stream):
        u, v = line.strip().split()
        edge = [u, v] if int(u) < int(v) else [v, u]
        if keep(n+1, edges_size):
            check_close(edge, wedges, is_closed)
            new_wedges = get_wedges(edge, edges)
            insert_edge(edge, edges)
            if new_wedges:
                update_wedges(new_wedges, wedges)

    # print calculate_triangle(len(stream))
    print "edges", edges
    print "wedges", wedges
    print "is_closed", is_closed


