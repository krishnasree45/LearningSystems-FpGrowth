from FPTree import *
from collections import defaultdict
import time
import tracemalloc


def conditional_db_from_branches(branches):
    """

    :param branches:
    :return: Returns the conditional tree based on the conditional item

    Building a conditional FP tree from the given preceding branches of the main tree
    1) Parameter - 'branches' contains all the paths which end with the item using which we find the conditional db
    2) Create the conditional tree -
        a) Create a root
        b) Method - 'add_point_to_conditional_tree' - adds every point to the tree .
        c) Updates the count only to the leaf node which is the conditioned item.
        d) Updates the links to the tree by adding next point.
    3) Remove the conditioned item in the database(Conditional tree)
    4) Reverse the branch and increment the count of the preceding items in the tree.
    5) Return conditional tree db
    """
    # Initialise an empty tree
    conditional_tree_db = FPTree()
    # Item on which we are going to condition the database
    item_to_be_conditioned = None

    # Create a new conditional tree and copy the branches into it.
    # Only we calculate the leaf nodes count.
    # The parents count will be calculated based on the leaf node count
    for branch in branches:  # For every branch
        if item_to_be_conditioned is None:
            item_to_be_conditioned = branch[-1].item  # Take the last node which is the item to be conditioned

        # Initialising tree root point
        tree_point = conditional_tree_db.root

        for node in branch:
            # Retrieves the child node of the tree point
            tree_next_point = tree_point.search_child(node.item)
            # check if the child node is the node to be conditioned
            if tree_next_point is None:

                if node.item != item_to_be_conditioned:
                    # If the node is not the item to be conditioned, keep the count as 0
                    item_count = 0

                else:
                    # If the item is item to be conditioned, keep the same count
                    item_count = node.count

                # Create a new FP Node for the tree_next_point
                tree_next_point = FPNode(conditional_tree_db, node.item, item_count)

                # Add the newly created tree_next_point to the previous node
                tree_point.add_child(tree_next_point)
                # Update the link of the tree
                conditional_tree_db._update_link(tree_next_point)
            tree_point = tree_next_point

    if item_to_be_conditioned is None:
        print('item_to_be_conditioned should not be None')

    # Find the count of the parent nodes from leaf
    for branch in conditional_tree_db.preceding_branches(item_to_be_conditioned):
        # Count is the initial count of the conditioned item
        count = branch[-1].count

        # For all the parent nodes, find the count
        for node in reversed(branch[:-1]):
            node._count += count

    return conditional_tree_db


def find_frequent_itemsets(input_records, min_sup):
    """

    :param input_records:
    :param min_sup:
    :yields: All the frequent itemsets generated

    Calculates frequent itemsets from the passed transaction db using FP Growth algorithm.
    The method yields all the frequent items to the calling method.

    'input_records' parameter is a list of lists consisting of all the transaction records
    'min_sup' is the value defined by the user for finding the frequent itemsets whose count is
    greater than the min_sup
    """
    items_dict = defaultdict(lambda: 0)  # Initialising the items dict with 0 which is further used to store the count

    # For every input record and every item in it store the number of occurrences in the 'items_dict'
    for record in input_records:
        for item in record:
            # PreProcessing of the data, remove empty sets.
            if item != '' and item != '?':
                # Remove whitespaces present in the item
                item.strip()
                items_dict[item] += 1
            else:
                record.remove(item)

    # For every item in, we retain it only if the support is greater than the minimum support
    # items_modified_dict = {}
    temp = []
    for item, support in items_dict.items():
        if support >= min_sup:
            items_dict[item] = support
        else:
            temp.append(item)

    for iter in temp:
        del items_dict[iter]

    # Building the Frequent pattern tree. If the record contains the items which have count less than min_sup,
    # remove them from the transaction db. And sort the items in the record in non increasing order.

    def remove_infreq_items(record):
        for item in record:
            if item not in items_dict:
                record.remove(item)
        record = sorted(record, key=lambda v: items_dict[v], reverse=True)
        return record

    main_tree = FPTree()
    for record in input_records:
        # Add all the records to the tree, after removing the infrequent items
        main_tree.add(remove_infreq_items(record))

    def get_freq_itemsets_of_all_size(tree, items_to_be_appended):
        """

        :param tree: Takes in the main tree or the conditional tree
        :param items_to_be_appended: The suffix items which are used to generate the frequent itemsets
        :return: yields the frequent itemsets
        """
        for item, nodes in tree.items():
            support = 0
            # For all the nodes in the tree calculate the count which is in turn the support
            for n in nodes:
                support += n.count
            if item not in items_to_be_appended and support >= min_sup:
                # Add the item to the items_to_be_appended
                new_appended_set = [item] + items_to_be_appended

                # Found a new frequent itemset yield it to the calling method
                yield (new_appended_set, support)

                # Construct a conditional tree and recurrently check for frequent itemsets
                cond_tree = conditional_db_from_branches(tree.preceding_branches(item))

                for s in get_freq_itemsets_of_all_size(cond_tree, new_appended_set):
                    # Yield the newly found frequent itemset to the calling method
                    yield s

    # Search for frequent itemsets, and yield the results we find.
    for itemset in get_freq_itemsets_of_all_size(main_tree, []):
        yield itemset


if __name__ == '__main__':
    import csv

    min_sup = input('Enter Minimum support value')
    csv_path = input('Enter transaction database csv path')

    input_records = []  # Transaction DB containing transactions as list of lists
    with open(csv_path) as db:
        for row in csv.reader(db):
            input_records.append(row)

    tracemalloc.start()
    st = time.time()
    result = []
    for itemset, support in find_frequent_itemsets(input_records, int(min_sup)):
        result.append((itemset, support))

    result = sorted(result, key=lambda i: i[0])
    for itemset, support in result:
        print(str(itemset) + ' ' + str(support))
    current, peak = tracemalloc.get_traced_memory()
    et = time.time()

    print('Elapsed time: ', et - st)
    tracemalloc.stop()
    print('Size: ', len(result))

    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
