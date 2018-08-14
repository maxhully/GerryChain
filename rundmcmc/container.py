from collections import ChainMap


class Assignment(ChainMap):
    def __init__(self, assignment, flips=None):
        if isinstance(assignment, ChainMap):
            _assignment = assignment.commit_flips()
        else:
            _assignment = assignment

        if not flips:
            flips = dict()

        super().__init__(flips, _assignment)

    def commit_flips(self):
        """Record the proposed flips in the old assignment, and
        then return this updated version. This mutates assignment in place,
        in order to avoid the assignment becoming a giant tower of ChainMaps
        as the chain runs.
        """
        flips = self.maps[0]
        assignment = self.maps[1]

        for node, part in flips.items():
            assignment[node] = part

        return assignment
