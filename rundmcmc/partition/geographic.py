import warnings

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
        validate_graph(graph)

        if updaters:
            # Here, .update() is the dictionary method, not
            # anything to do with our notion of updaters.
            updaters.update(self.default_updaters)
        super().__init__(graph=graph, assignment=assignment, updaters=updaters,
                         parent=parent, flips=flips)


def validate_graph(self, graph):
    edges_are_valid = all('shared_perim' in graph.edges[edge]
                            for edge in graph.edges)
    if not edges_are_valid:
        raise TypeError('The provided graph does not have "shared_perim" edge attributes.')

    for node in graph.nodes:
        if graph.nodes[node]['boundary_node'] and 'boundary_perim' not in graph.nodes[node]:
            raise TypeError('The provided graph has invalid boundary data.')

    if all(not graph.nodes[node]['boundary_node'] for node in graph.nodes):
        warnings.warn('The provided graph contains no boundary nodes')

    return True
