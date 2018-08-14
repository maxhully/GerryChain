import collections

from .assignment import Assignment
from ..updaters import compute_edge_flows, flows_from_changes


class Partition:
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

        self.parts = get_parts_from_assignment(assignment)

    def _from_parent(self, parent, flips):
        self.parent = parent
        self.assignment = Assignment(parent.assignment, flips)
        self.flips = flips
        self.graph = parent.graph

        self._update_parts_and_flows()

    def _update_parts_and_flows(self):
        self.flows = flows_from_changes(self.parent.assignment, self.flips)
        self.edge_flows = compute_edge_flows(self)
        self.parts = update_parts_from_flows(self.parent.assignment, self.flows)

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


def get_parts_from_assignment(assignment):
    parts = collections.defaultdict(set)
    for node, part in assignment.items():
        parts[part].add(node)
    return parts


def update_parts_from_flows(old_parts, flows):
    parts = dict(old_parts)

    for part, flow in flows.items():
        parts[part] = (old_parts[part] | flow['in']) - flow['out']

    return parts
