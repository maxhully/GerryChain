from ..updaters import (boundary_nodes, cut_edges, cut_edges_by_part,
                        exterior_boundaries, interior_boundaries, perimeters)
from .updating import UpdatingPartition


class GeographicPartition(UpdatingPartition):
    """
    This is a shaky implementation of this idea.
    """
    default_updaters = {'perimeters': perimeters,
            'exterior_boundaries': exterior_boundaries,
            'interior_boundaries': interior_boundaries,
            'boundary_nodes': boundary_nodes,
            'cut_edges': cut_edges,
            'cut_edges_by_part': cut_edges_by_part}

    def __init__(self, graph=None, assignment=None, updaters=None,
                 parent=None, flips=None):
        # TODO: Validate here that the graph has the right attributes
        if updaters:
            # Here, .update() is the dictionary method, not
            # anything to do with our notion of updaters.
            updaters.update(self.default_updaters)
        super().__init__(graph=graph, assignment=assignment, updaters=updaters,
                         parent=parent, flips=flips)
