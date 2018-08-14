from .partition import Partition


class UpdatingPartition(Partition):
    def __init__(self, graph=None, assignment=None, updaters=None,
                 parent=None, flips=None):
        if parent:
            updaters = parent.updaters
        elif not updaters:
            updaters = dict()
        self.updaters = updaters

        super().__init__(graph=graph, assignment=assignment, parent=parent, flips=flips)

        self._update()

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
