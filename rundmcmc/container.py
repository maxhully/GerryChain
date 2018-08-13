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


class UpdaterContainer:
    def __init__(self, updaters):
        self.updaters = updaters

    def _update(self):
        self._cache = dict()

        for key in self.updaters:
            if key not in self._cache:
                self._cache[key] = self.updaters[key](self)

    def __getitem__(self, key):
        """Allows keying on a Partition instance.

        :key: Property to access.

        """
        if key not in self._cache:
            self._cache[key] = self.updaters[key](self)
        return self._cache[key]
