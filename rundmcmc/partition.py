import collections

from rundmcmc.updaters import flows_from_changes, compute_edge_flows
from rundmcmc.container import Assignment


class _Partition:
    """
    Partition represents a partition of the nodes of the graph. It will perform
    the first layer of computations at each step in the Markov chain - basic
    aggregations and calculations that we want to optimize.

    """

    def __init__(self, graph=None, assignment=None, parent=None, flips=None):
        """
        :graph: Underlying graph; a NetworkX object.
        :assignment: Dictionary assigning nodes to districts. If None,
                     initialized to assign all nodes to district 0.
        :updaters: Dictionary of functions to track data about the partition.
                   The keys are stored as attributes on the partition class,
                   which the functions compute.

        """
        if parent:
            self._from_parent(parent, flips)
        else:
            self._first_time(graph, assignment)

    def _first_time(self, graph, assignment):
        self.graph = graph

        if not assignment:
            assignment = {node: 0 for node in graph.nodes}

        self.assignment = Assignment(assignment)
        self.parent = None
        self.flips = None

        self.parts = collections.defaultdict(set)
        for node, part in self.assignment.items():
            self.parts[part].add(node)

    def _from_parent(self, parent, flips):
        self.parent = parent
        self.flips = flips
        self.graph = parent.graph

        self.assignment = Assignment(parent.assignment, flips)
        self._update_parts_and_flows()

    def _update_parts_and_flows(self):
        self.flows = flows_from_changes(self.parent.assignment, self.flips)
        self.edge_flows = compute_edge_flows(self)

        self.parts = dict(self.parent.parts)

        for part, flow in self.flows.items():
            self.parts[part] = (self.parent.parts[part] | flow['in']) - flow['out']

    def __len__(self):
        return len(self.parts)

    def __repr__(self):
        number_of_parts = len(self)
        s = "s" if number_of_parts > 1 else ""
        return f"Partition of a graph into {str(number_of_parts)} part{s}"

    def merge(self, flips):
        """
        :flips: dict assigning nodes of the graph to their new districts
        :returns: A new instance representing the partition obtained by performing the given flips
                  on this partition.

        """
        return self.__class__(parent=self, flips=flips)

    def crosses_parts(self, edge):
        return self.assignment[edge[0]] != self.assignment[edge[1]]

# This Partition should be called UpdatingPartition,
# and _Partition should be called just Partition.


class Partition(_Partition):
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
