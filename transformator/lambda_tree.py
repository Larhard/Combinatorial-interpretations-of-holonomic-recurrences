from transformator.tree import Tree


class LambdaTree(Tree):
    kinds = ["l", "a", "s", "o"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_vertex(self, kind, children):
        left, right = children

        sk = kind[0]
        sl = left[0] if left is not None else None
        sr = right[0] if right is not None else None

        if sk == "l":
            if sl is None:
                return False
            if sr is not None:
                return False

        elif sk == "s":
            if sl is not None:
                return False
            if sr not in ("s", "o"):
                return False

        elif sk == "a":
            if sl is None:
                return False
            if sr is None:
                return False

        elif sk == "o":
            if sl is not None:
                return False
            if sr is not None:
                return False

        else:
            return False

        return True
