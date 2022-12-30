
class FPNode(object):
    """
    Node of the FP Tree
    """

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add_child(self, child_node):
        """

        :param child_node:
        :return:

        This method adds the child to the given FP Node
        """
        if child_node.item in self.children:
            return
        else:
            self._children[child_node.item] = child_node
            child_node.parent = self

    def search_child(self, item):
        """

        :param item:
        :return:
        """
        """
        Check whether this node contains a child node for the given item.
        If so, that node is returned; otherwise, `None` is returned.
        """
        if item in self._children:
            return self._children[item]
        else:
            return None

    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        """
        Reference of the tree which contains the node
        :return:
        """
        return self._tree

    @property
    def item(self):
        """

        :return: Item contained in this node. eg: I1, I2, I3..
        """
        return self._item

    @property
    def count(self):
        """
        :return: The count of the item.
        """
        return self._count

    def increment(self):
        """
        :return: None
        Increment the count by one for the count associated with the item
        """
        if self._count is None:
            print("This is a root node and doesn't have a count")
        self._count += 1

    @property
    def root(self):
        """
        :return: boolean, true - if the node is a root, i.e if the node doesn't contain any item and the count is also
                        None
        false - If the node is not root
        """
        if self._item is None and self.count is None:
            return True
        return False

    @property
    def leaf(self):
        """
        :return: true, if the length of the children is 0 i.e a leaf node
                false, if the lenght of the children is not 0 i.e an internal node
        """
        return len(self._children) == 0

    @property
    def parent(self):
        """
        :return: parent of the self
        Property for the node's parent
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def neighbor(self):
        """

        :return: neighbour of the self
        Property of the node's neighbor. The same item which is present to the right in the tree
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        self._neighbor = value

    @property
    def children(self):
        """The nodes that are children of this node."""
        return tuple(self._children.values())
