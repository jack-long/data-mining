import random


class SpectralClustering:
    def __init__(self, source, edges_size, wedges_size):
        self.source = source
        self.edges_size = edges_size
        self.wedges_size = wedges_size
        self.edges = []
        self.wedges = [None] * wedges_size
        self.is_closed = [False] * wedges_size
        # self.p = 0
        # self.k = 3 * self.p

    def total_wedges(self):
        counter = 0
        for index, edge_i in enumerate(self.edges):
            for edge_j in self.edges[index + 1:]:
                if set(edge_j).intersection(edge_i):
                    counter += 1
        return counter

    def calculate_triangle(self, t):
        p = self.is_closed.count(True) / float(self.wedges_size)
        return (p * t * t / self.edges_size / (self.edges_size-1)) * self.total_wedges()

    def keep(self, n):
        return random.randint(1, n) < self.edges_size

    def insert_edge(self, edge):
        if len(self.edges) <= 100:
            self.edges.append(edge)
        else:
            index = random.randint(1, len(self.edges))
            self.edges[index - 1] = edge

    def get_wedges(self, edge):
        new_wedges = []
        for each in self.edges:
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

    def check_close(self, edge):
        for index, wedge in enumerate(self.wedges):
            if wedge is None:
                continue
            if edge == wedge[:2]:
                self.is_closed[index] = True
                print wedge[0] + '-' + wedge[2], wedge[1] + '-' + wedge[2]
                # print is_closed.count(True)

    def update_wedges(self, new_wedges, wedges):
        current_wedges = self.total_wedges()
        for index in range(self.wedges_size):
            if random.randint(0, current_wedges) < len(new_wedges):
                choice = random.randint(1, len(new_wedges))
                wedge = new_wedges[choice - 1]
                wedges[index] = wedge
                if not wedge:
                    print "update", wedge, new_wedges
                self.is_closed[index] = False

    def cluster(self):
        with open(self.source) as f:
            stream = f.readlines()
            for n, line in enumerate(stream):
                u, v = line.strip().split()
                edge = [u, v] if int(u) < int(v) else [v, u]
                if self.keep(n+1):
                    self.check_close(edge)
                    new_wedges = self.get_wedges(edge)
                    self.insert_edge(edge)
                    if new_wedges:
                        self.update_wedges(new_wedges, self.wedges)

            print "edges", self.edges
            print "wedges", self.wedges
            print "is_closed", self.is_closed
            t = len(stream)
            print "triangle estimate", self.calculate_triangle(t)


def main():
    spectral = SpectralClustering("data/ego-facebook", 100, 100)  # com-amazon  ego-facebook
    spectral.cluster()


if __name__ == "__main__":
    main()
