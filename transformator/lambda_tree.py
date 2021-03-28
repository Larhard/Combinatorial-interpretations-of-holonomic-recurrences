from transformator.tree import Tree


class LambdaTree(Tree):
    kinds = ["l", "@", "s", "o"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_vertex(self, kind, children):
        left, right = children

        if kind == "l":
            if left is None:
                return False
            if right is not None:
                return False

        elif kind == "s":
            if left is not None:
                return False
            if right not in ("s", "o"):
                return False

        elif kind == "@":
            if left is None:
                return False
            if right is None:
                return False

        elif kind == "o":
            if left is not None:
                return False
            if right is not None:
                return False

        else:
            return False

        return True
