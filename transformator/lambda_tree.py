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

    @classmethod
    def generate(cls, n, kinds=None, validate=True):
        kinds = kinds or cls.kinds

        if n == 0:
            yield cls([None])

        if n == 1:
            yield cls(["o", None, None])

        else:
            for kind in kinds:
                if kind == "o":
                    pass

                elif kind == "l" and n >= 2:
                    for left in cls.generate(n - 1, kinds, validate=False):
                        result = cls(["l"] + left.pre_order + [None])

                        if validate:
                            assert result.validate(), result

                        yield result

                elif kind == "s" and n >= 2:
                    for right in cls.generate(n - 1, ["s", "o"], validate=False):
                        result = cls(["s", None] + right.pre_order)

                        if validate:
                            assert result.validate(), result

                        yield result

                elif kind == "a" and n >= 3:
                    for i in range(1, n - 1):
                        left_n = n - i - 1
                        right_n = i

                        for left in cls.generate(left_n, kinds, validate=False):
                            for right in cls.generate(right_n, kinds, validate=False):
                                result = cls(["a"] + left.pre_order + right.pre_order)

                                if validate:
                                    assert result.validate(), result

                                yield result
