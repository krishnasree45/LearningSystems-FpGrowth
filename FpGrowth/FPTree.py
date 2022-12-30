from FPNode import *
from collections import namedtuple


class FPTree(object):
    """
    Class for FP Tree objects
    """
    # """
    # An FP tree.
    #
    # This object may only store transaction items that are hashable
    # (i.e., all items must be valid as dictionary keys or set members).
    # """

    Node_links = namedtuple('Link', 'begin end')

    def __init__(self):
        # The root node of the tree.
        self._root = FPNode(self, None, None)

        # A dictionary mapping items to the begin and end of a path of
        # "neighbors" that will hit every node containing that item.
        self._links = {}

    @property
    def root(self):
        """Root of the tree"""
        return self._root

    def add(self, record):
        """Appending record to the tree"""
        tree_point = self._root

        for item in record:
            # Update every item in the record to the tree
            tree_next_point = tree_point.search_child(item)
            if tree_next_point:

                # If the tree_next_point already exists in the tree for the current record
                # Increment the count and use it again
                tree_next_point.increment()
            else:
                # If the tree_next_point doesn't exist in the tree, create a new one and add it as child to tree_point
                tree_next_point = FPNode(self, item)
                tree_point.add_child(tree_next_point)
                # After adding the new node update the link which comprises the newly added node
                self._update_link(tree_next_point)

            # Update the current tree_point to tree_next_point so that the next child gets added to the next point
            tree_point = tree_next_point

    def _update_link(self, point):
        """Add the given node to the link through all nodes for its item."""
        if self != point.tree:
            print('For updating links self should equal point.tree')

        if point.item in self._links:
            link = self._links[point.item]
            link[1].neighbor = point
            self._links[point.item] = self.Node_links(link[0], point)
        else:
            self._links[point.item] = self.Node_links(point, point)

    def items(self):

        """

        :returns:
        This method returns the table which contains items - data points,
         and the corresponding pointers to the nodes in the tree
        Yields a tuple which contains the (item, links to items) that belong to the item
        """
        data_points_list = []

        for data_point in self._links.keys():
            data_points_list.append(data_point)

        for data_point in reversed(data_points_list):
            yield data_point, self.nodes(data_point)

    def nodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """
        if item in self._links:
            node = self._links[item][0]
        else:
            return

        while node is not None:
            yield node
            node = node.neighbor  # Update node to node.neighbor

    def preceding_branches(self, data_point):
        """

        :param data_point:
        :return: preceding_branches

        Calculates all the prior paths of the given item.
        """
        preceding_branches = []
        for node in self.nodes(data_point):
            branch = []
            while node and not node.root:
                branch.append(node)
                node = node.parent
            branch.reverse()
            preceding_branches = [branch] + preceding_branches
        return preceding_branches
