class Assignment:
    def __init__(self, assignment, flips=None):
        if isinstance(assignment, Assignment):
            self._assignment = assignment.commit_flips()
        else:
            self._assignment = assignment

        if not flips:
            flips = dict()
        self.flips = flips

    def __getitem__(self, node):
        if node in self.flips:
            return self.flips[node]
        else:
            return self._assignment[node]

    def commit_flips(self):
        for node, part in self.flips.items():
            self._assignment[node] = part
        return self._assignment

    def items(self):
        for node, part in self._assignment.items():
            if node in self.flips:
                yield (node, self.flips[node])
            else:
                yield (node, part)

    def keys(self):
        return self._assignment.keys()

    def values(self):
        for node, part in self._assignment.items():
            if node in self.flips:
                yield self.flips[node]
            else:
                yield part
