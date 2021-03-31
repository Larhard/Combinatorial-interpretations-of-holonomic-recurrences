from graphviz import Graph


class Tree:
    shape = "plain"
    arity = 2
    kinds = ["o"]
    pointers = ["*"]

    def __init__(self, pre_order):
        self.pre_order = [k if isinstance(k, tuple) else (k, ) for k in pre_order]

    def __iter__(self):
        return iter(self.pre_order)

    def _repr_svg_(self):
        return self.graph._repr_svg_()

    def _repr_html_(self):
        return self._repr_svg_()

    def get_kind_label(self, kind):
        if kind[0] is None:
            return "".join(kind[1:])

        return "".join(kind)

    def get_kind_shape(self, kind):
        if kind[0] is None:
            return "none"

        return self.shape

    def get_kind_node_dict(self, kind):
        result = {}

        result["label"] = self.get_kind_label(kind)
        result["shape"] = self.get_kind_shape(kind)

        return result

    def get_kind_edge_dict(self, kind, parent_kind):
        result = {}

        if kind[0] is None:
            result["color"] = "lightgreen"

        return result

    @property
    def graph(self):
        graph = Graph()
        graph.attr(size="4,4")

        stack = []

        for i, kind in enumerate(self.pre_order):
            idx = str(i)

            if i == 0:
                if kind[0] is not None:
                    graph.node(idx, **self.get_kind_node_dict(kind))

            else:
                p_idx, p_kind, p_n = stack.pop()
                p_n -= 1

                graph.node(idx, **self.get_kind_node_dict(kind))
                graph.edge(p_idx, idx, **self.get_kind_edge_dict(kind, p_kind))

                if p_n > 0:
                    stack.append((p_idx, p_kind, p_n))

            if kind[0] is not None and self.arity > 0:
                stack.append((idx, kind, self.arity))

        if len(stack):
            raise RuntimeError(f"Non-empty stack left: {stack}")

        return graph

    def get_subtree(self, idx):
        start = idx
        end = idx

        count = 1
        while count > 0:
            if self.pre_order[end][0] is None:
                count -= 1
            else:
                count += 1

            end += 1

        return self.pre_order[start:end]

    def split_subree(self, idx):
        pre = self.pre_order[:idx]

        kind = self.pre_order[idx]

        if kind[0] is not None:
            left = self.get_subtree(idx + 1)
            right = self.get_subtree(idx + 1 + len(left))
        else:
            left = []
            right = []

        post = self.pre_order[idx + 1 + len(left) + len(right):]

        return pre, kind, left, right, post

    def visit_subtrees(self, func):
        for i in range(len(self.pre_order)):
            pre, kind, left, right, post = self.split_subree(i)
            result = func(kind, left, right)

            if result is not None:
                yield self.__class__(pre + result + post)

    def visit_parent_subtrees(self, func):
        for i in range(len(self.pre_order)):
            pre, kind, left, right, post = self.split_subree(i)

            if len(left) > 0:
                result = func(left[0], kind, left, right)

                if result is not None:
                    yield self.__class__(pre + result + post)

            if len(right) > 0:
                result = func(right[0], kind, left, right)

                if result is not None:
                    yield self.__class__(pre + result + post)

    def validate(self):
        stack = []

        stack.append((self.pre_order[0], []))

        for kind in self.pre_order[1:]:
            if len(stack) == 0:
                return False

            p_kind, p_children = stack.pop()
            p_children.append(kind)

            if len(p_children) < self.arity:
                stack.append((p_kind, p_children))
            else:
                if not self.validate_vertex(p_kind, p_children):
                    return False

            if kind[0] is not None:
                stack.append((kind, []))

        if len(stack) > 0:
            return False

        return True

    def validate_vertex(self, kind, children):
        return True

    @classmethod
    def generate(cls, n, kinds=None, validate=True):
        kinds = kinds or cls.kinds

        if n == 0:
            yield cls([(None, )])

        else:
            for kind in kinds:
                for i in range(n):
                    left_n = n - i - 1
                    right_n = i

                    for left in cls.generate(left_n, kinds, validate=False):
                        for right in cls.generate(right_n, kinds, validate=False):
                            result = cls([(kind, )] + left.pre_order + right.pre_order)

                            if validate:
                                if result.validate():
                                    yield result
                            else:
                                yield result

    @classmethod
    def generate_pointed(cls, n, kinds=None, pointers=None):
        pointers = pointers or cls.pointers

        for tree in cls.generate(n, kinds):
            for pointer in pointers:
                for t in tree.visit_subtrees(lambda kind, left, right: [kind + (pointer, )] + left + right):
                    yield t

    def with_pointers_removed(self):
        return self.__class__(k[0] for k in self.pre_order)

    def __str__(self):
        result = [
            self.get_kind_label(kind) for kind in self
        ]

        return f"<{', '.join(result)}>"

    def __repr__(self):
        return str(self)

