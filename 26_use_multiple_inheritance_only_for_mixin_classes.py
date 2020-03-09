from pprint import pprint


'''
An example of Mixin Classes
'''
class ToDictMixin:
    def to_dict(self):
        # print(self.__dict__)
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        # input()
        # print(value)

        if isinstance(value, ToDictMixin):
            # print('isinstance(value, ToDictMixin)')
            return value.to_dict()
        elif isinstance(value, dict):
            # print('isinstance(value, dict)')
            return self._traverse_dict(value)
        elif isinstance(value, list):
            # print('isinstance(value, list)')
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            # print('hasattr(value, __dict__):')
            return self._traverse_dict(value.__dict__)
        else:
            # print('value')
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))

pprint(tree.to_dict())
print()


'''
The best part about mix-ins is that you can make their generic functionality
pluggable so behaviors can be overridden when required.

This circular reference would cause the default implementation of
ToDictMixin.to_dict to loop forever.

The solution is to override the ToDictMixin._traverse method in the
BinaryTreeWithParent class to only process values that matter, preventing
cycles encountered by the mix-in.
'''
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # Prevent cycles else:
        return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
pprint(root.to_dict())
print()


'''
By defining BinaryTreeWithParent._traverse, I’ve also enabled any class that
has an attribute of type BinaryTreeWithParent to automatically work with
ToDictMixin.
'''
class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
pprint(my_tree.to_dict()) # No infinite loop
print()
