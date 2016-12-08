import random


class StreamSampling:
    def __init__(self, source, edges_size, wedges_size):
        self.source = source
        self.edges_size = edges_size
        self.wedges_size = wedges_size
        self.edges = []
        self.wedges = [None] * wedges_size
        self.is_closed = [False] * wedges_size
        self.edges_filled = False
        self.edges_updated = False

    def total_wedges(self):
        """Calculate the total number of wedges formed by current edges reservoir.
        """
        counter = 0
        for index, edge_i in enumerate(self.edges):
            for edge_j in self.edges[index + 1:]:
                if set(edge_j).intersection(edge_i):
                    counter += 1
        return counter

    def calculate_triangle(self, t):
        """Calculate the estimates T_i
        """
        closed = self.is_closed.count(True)
        p = closed / float(self.wedges_size)
        return (p * t * t / self.edges_size / (self.edges_size-1)) * self.total_wedges()

    # def keep(self, n):
    #     """Prop
    #     """
    #     return random.randint(0, n) < self.edges_size

    def insert_edge(self, edge, t):
        """Insert a new edge into reservoir samples with probability s/t
        """
        self.edges_updated = False
        if self.edges_filled:
            for i in range(self.edges_size):
                if random.randint(0, t) <= 1:
                    self.edges[i] = edge
                    self.edges_updated = True
        else:
            self.edges.append(edge)
            if len(self.edges) >= self.edges_size:
                self.edges_filled = True
            self.edges_updated = True

    def get_wedges(self, edge):
        """new edges involving new edge e_t
        """
        new_wedges = []
        for each in self.edges:
            if edge == each:
                continue
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
        """set the close bit in is_closed list if wedge reservoir is closed by e_t
        """
        for index, wedge in enumerate(self.wedges):
            try:
                if edge == wedge[:2]:
                    self.is_closed[index] = True
                    print wedge[0] + '-' + wedge[2], wedge[1] + '-' + wedge[2]
            except TypeError:
                # if wedge is None
                continue

    def update_wedges(self, new_wedges, wedges):
        """Insert new wedge into wedges reservoir
        """
        current_wedges = self.total_wedges()
        for index in range(self.wedges_size):
            if random.randint(0, current_wedges) < len(new_wedges):
                choice = random.randint(1, len(new_wedges))
                wedge = new_wedges[choice - 1]
                wedges[index] = wedge
                self.is_closed[index] = False

    def sampling(self):
        """ run the sampling process
        """
        with open(self.source) as f:
            stream = f.readlines()
            for n, line in enumerate(stream):
                u, v = line.strip().split()
                edge = [u, v] if int(u) < int(v) else [v, u]
                self.check_close(edge)
                self.insert_edge(edge, n)
                if self.edges_updated:
                    new_wedges = self.get_wedges(edge)
                    if new_wedges:
                        self.update_wedges(new_wedges, self.wedges)
                # self.calculate_triangle(n)
            print "edges", self.edges
            print "wedges", self.wedges
            print "is_closed", self.is_closed
            print "True count", self.is_closed.count(True)
            t = len(stream)
            print "triangle estimate", self.calculate_triangle(t)


def main():
    spectral = StreamSampling("data/com-amazon", 200, 200)  # com-amazon  ego-facebook
    spectral.sampling()


if __name__ == "__main__":
    main()
