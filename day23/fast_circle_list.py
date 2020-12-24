#
#  A fast circular list implementation
#

# a node, one item in the list
# if knows the value that it stores and the previous and next items in the list
class Node:
    def __init__(self, the_value, previous_node, next_node):
        self.value = the_value
        if previous_node is None:
            self.previous_node = self
        else:
            self.previous_node = previous_node

        if next_node is None:
            self.next_node = self
        else:
            self.next_node = next_node

    def print(self):
        print(f"{self.value}")

    def __repr__(self):
        return f"<{self.value}>"

    def next(self):
        return self.next_node

    def set_next(self, target_node):
        self.next_node = target_node

    def set_prev(self, target_node):
        self.previous_node = target_node

    def previous(self):
        return self.previous_node


class FastCircleList:
    def __init__(self):
        self.lookup = dict()
        self.current_node = None

    def __contains__(self, item):
        return item in self.lookup

    def item_count(self):
        return len(self.lookup)

    def max_value(self):
        return max(self.lookup.keys())

    def min_value(self):
        return min(self.lookup.keys())

    def print(self, message=None, walk=None):
        s = ""
        if message is not None:
            s = f" <--- {message}"
        print(
            f"FastCircleList(current_node={self.current_node}, total_nodes={len(self.lookup)}){s}"
        )
        if walk is not None:
            self.print_walk(walk, False)

    def locate_node(self, item):
        """
        Return the node corresponding to an item
        """
        result = None
        if item in self.lookup:
            result = self.lookup[item]
        return result

    def get_current_node(self):
        """
        Return the current node
        """
        return self.current_node

    def set_current_node(self, target_node):
        """
        Set the current node to the one specified
        this assume that it's already part of the list
        """
        self.current_node = target_node

    def remove_item(self, item):
        """
        Return the removed item or None if not found
        """
        result = None
        # find the node
        if item in self.lookup:
            the_node = self.lookup[item]
            result = self.remove_node(the_node)
        return result

    def remove_next_node(self, the_node=None):
        """
        Given a starting node, remove the one after it and return it..
        if the_node is None then we use the self.current_node value as a starting point
        """
        if the_node is None:
            the_node = self.current_node
        the_node = the_node.next()
        self.remove_node(the_node)
        return the_node

    def remove_node(self, the_node):
        """
        Remove the mentioned node from the collection, returning the removed node or
        """
        the_value = the_node.value
        next_node = the_node.next()
        prev_node = the_node.previous()
        next_node.set_prev(prev_node)
        prev_node.set_next(next_node)
        del self.lookup[the_value]

        # make sure we're not pointing at an orphan
        if self.current_node == the_node:
            self.current_node = next_node

        return the_node

    def print_list(self):
        start = self.current_node
        s = str(start)
        this_node = start.next()
        while this_node != start:
            s += f", {str(this_node)}"
            this_node = this_node.next()
        print(f"{s}")

    def print_walk(self, walk_count, backwards=False):
        """
        print out the current item and walk_count-1 subsequent steps
        """
        s = ""
        this_node = self.current_node
        remaining_steps = walk_count
        while remaining_steps > 0:
            # print this one..
            s += f"{str(this_node)} "
            # next one..
            if backwards:
                this_node = this_node.previous()
            else:
                this_node = this_node.next()
            # and reduce the count..
            remaining_steps -= 1

        print(
            f'Walking {"backwards" if backwards else "forwards"} for {walk_count} steps: {s}'
        )

    def add(self, item):
        """
        Add the mentioned item at the current location
        """
        return self.add_after(self.current_node, item)

    def append(self, item):
        """
        Add this at the point furthest away from the current head (in a next->next->next direction)
        """
        return self.add_behind(self.current_node, item)

    def add_behind(self, target_node, item):
        """
        Add the item mentioned behind the specified node
        """
        if target_node is not None:
            # find the current next node
            prev_node = target_node.previous()
            # create a new node sitting between these two
            new_node = Node(item, prev_node, target_node)
            # fix the pointers in those nodes to point at the new node
            target_node.set_prev(new_node)
            prev_node.set_next(new_node)
        else:
            # first time adding a node.. so..
            new_node = Node(item, None, None)
            self.current_node = new_node

        # and whatever the case, we need to add the value to the quick lookup
        self.lookup[item] = new_node

        return new_node

    def add_after(self, target_node, item):
        """
        Add the mentioned item after the specified node
        """

        # target node has two pointers, previous and next
        if target_node is not None:
            # find the current next node
            next_node = target_node.next()
            # create a new node sitting between these two
            new_node = Node(item, target_node, next_node)
            # fix the pointers in those nodes to point at the new node
            target_node.set_next(new_node)
            next_node.set_prev(new_node)
        else:
            # first time adding a node.. so..
            new_node = Node(item, None, None)
            self.current_node = new_node

        # and whatever the case, we need to add the value to the quick lookup
        self.lookup[item] = new_node

        return new_node


# main, some simple testing..
if __name__ == "__main__":
    l = FastCircleList()
    l.append("ant")
    l.append("bat")
    l.append("cat")
    l.append("dog")
    l.append("egg")
    l.append("frog")

    l.print("added everything")
    l.print_list()

    l.remove_item("bat")
    l.print("removed bat")
    l.print_list()

    l.remove_item("ant")
    l.print("removed ant")
    l.print_list()
    l.print_walk(10, backwards=False)
    l.print_walk(10, backwards=True)

    if "bat" in l:
        print("we have a bat..")
    else:
        print("we don't have a bat..")

    for i in range(10):
        l.append(i)
    l.print("added 0..9")
    l.print_list()

    # find item 3
    target_node = l.locate_node(3)
    print(f"Found item 3: {target_node}")
    # cut the next 3 values after that out..
    cut_values = [l.remove_next_node(target_node) for i in range(3)]
    print(f"removed these values: {cut_values}")
    l.print("after removal")
    l.print_list()
