import random


edges_size = 100
wedges_size = 100

edges = []
wedges = []

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
            wedge = sorted([each[1], edge[1]])
            wedge.append(edge[0])
        if edge[0] == each[1]:
            wedge = [each[0], edge[1], edge[0]]
        if edge[1] == each[0]:
            wedge = [edge[0], each[1], each[0]]
        if edge[1] == each[1]:
            wedge = sorted([each[0], edge[0]])
            wedge.append(edge[1])
        new_wedges.append(wedge)
    print "new wedge", new_wedges
    return new_wedges


def check_close(edge, wedges, is_closed):
    for index, wedge in enumerate(wedges):
        if edge == wedge[:2]:
            is_closed[index] = True
            print wedge[0] + '-' + wedge[2], wedge[1] + '-' + wedge[2]


def update_wedges(new_wedges, wedges):
    current_wedges = total_wedges(edges)
    for index, _ in wedges:
        if random.randint(current_wedges) < len(new_wedges):
            choice = random.randint(1, len(new_wedges))
            wedge = wedges[choice - 1]
            wedges[index] = wedge
            is_closed[index] = False


with open("data/ego-facebook") as f:
    stream = f.readlines()
    for n, line in enumerate(stream[:100]):
        u, v = line.strip().split()
        edge = sorted([u, v])
        if keep(n+1, edges_size):
            check_close(edge, wedges, is_closed)
            insert_edge(edge, edges)
            new_wedges = get_wedges(edge, edges)
            update_wedges(new_wedges, wedges)

    # print calculate_triangle(len(stream))
    print "edges", edges
    print "wedges", wedges


