from pprint import pprint

class ToDictMixin:
    def to_dict(self):
        print(self.__dict__)
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        input()
        print(value)

        if isinstance(value, ToDictMixin):
            print('isinstance(value, ToDictMixin)')
            return value.to_dict()
        elif isinstance(value, dict):
            print('isinstance(value, dict)')
            return self._traverse_dict(value)
        elif isinstance(value, list):
            print('isinstance(value, list)')
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            print('hasattr(value, __dict__):')
            return self._traverse_dict(value.__dict__)
        else:
            print('value')
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
