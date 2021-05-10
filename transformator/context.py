import functools as fn

from collections import defaultdict


class cached_property(fn.cached_property):
    def __set_name__(self, owner, name):
        if not hasattr(owner, "_cached"):
            setattr(owner, "_cached", [])

        owner._cached.append(name)

        return super().__set_name__(owner, name)


class Context:
    def __init__(self):
        self._ns = None
        self._class_constructor = None
        self._section_expressions = None

        self._active_class = None
        self._active_section = None

    @property
    def ns(self):
        return self._ns

    @ns.setter
    def ns(self, value):
        self._ns = value

        self.clear_cache()

    @property
    def class_constructor(self):
        return self._class_constructor

    @class_constructor.setter
    def class_constructor(self, value):
        self._class_constructor = value

        self.clear_cache()

    @property
    def section_expressions(self):
        return self._section_expressions

    @section_expressions.setter
    def section_expressions(self, value):
        self._section_expressions = value

        self.clear_cache()

    @cached_property
    def classes(self):
        return [list(self.class_constructor(n)) for n in self.ns]

    @cached_property
    def section_counts(self):
        result = []
        for class_idx, _ in enumerate(self.ns):
            result.append([])
            for equation, _ in self.section_expressions[class_idx]:
                result[-1].append(self.eval_section_equation(equation, class_idx))

        return result

    @cached_property
    def classes_counts(self):
        return [sum(k) for k in self.section_counts]

    @cached_property
    def sections(self):
        result = []
        for k in range(len(self.ns)):
            result.append([[] for _ in range(len(self.section_expressions[k]))])

        return result

    @cached_property
    def minus(self):
        return self.get_side(negative=True)

    @cached_property
    def plus(self):
        return self.get_side(negative=False)

    @cached_property
    def diff(self):
        minus = []
        plus = []

        p = 0
        q = 0

        while p < len(self.minus) and q < len(self.plus):
            minus_key = str(self.minus[p][0])
            plus_key = str(self.plus[q][0])

            if minus_key < plus_key:
                minus.append(self.minus[p])
                p += 1
            elif minus_key > plus_key:
                plus.append(self.plus[q])
                q += 1
            else:
                p += 1
                q += 1

        minus.extend(self.minus[p:])
        plus.extend(self.plus[q:])

        return minus, plus

    def get_side(self, negative=False):
        result = []

        multiplier_multiplier = -1 if negative else 1

        for class_idx, class_sections in enumerate(self.sections):
            for section_idx, section_parts in enumerate(class_sections):
                for part_idx, (multiplier, trees) in enumerate(section_parts):
                    for tree in trees:
                        if multiplier * multiplier_multiplier > 0:
                            data = (tree, (class_idx, section_idx, part_idx))

                            for _ in range(abs(multiplier)):
                                result.append(data)

        sorting_key = lambda data: (str(data[0]), -data[1][0], data[1][1], data[1][2])

        result.sort(key=sorting_key)
        return result

    def define_class(self, k):
        self.clear_stats_cache()

        self._active_class = k
        self._active_section = None

        self.clear_class(self._active_class)

    def define_section(self, k):
        assert k < len(self.section_expressions[self._active_class])

        self.clear_stats_cache()

        self._active_section = k

        self.clear_section(self._active_class, self._active_section)

        equation, introduction = self.section_expressions[self._active_class][self._active_section]
        print(f"# define {self._active_class},{self._active_section}: {equation} [{introduction}]")

    def append_r_class_subtree_visitor(self, multiplier, visitor):
        self.clear_stats_cache()

        trees = sum(
            [
                list(t.visit_subtrees(visitor))
                for t
                in self.classes[self._active_class]
            ],
            []
        )

        self.sections[self._active_class][self._active_section].append((multiplier, trees))

    def append_r_class_parent_subtree_visitor(self, multiplier, visitor):
        self.clear_stats_cache()

        trees = sum(
            [
                list(t.visit_parent_subtrees(visitor))
                for t
                in self.classes[self._active_class]
            ],
            []
        )

        self.sections[self._active_class][self._active_section].append((multiplier, trees))

    def append_r_class_left_parent_subtree_visitor(self, multiplier, visitor):
        self.clear_stats_cache()

        trees = sum(
            [
                list(t.visit_left_parent_subtrees(visitor))
                for t
                in self.classes[self._active_class]
            ],
            []
        )

        self.sections[self._active_class][self._active_section].append((multiplier, trees))

    def append_r_class_right_parent_subtree_visitor(self, multiplier, visitor):
        self.clear_stats_cache()

        trees = sum(
            [
                list(t.visit_right_parent_subtrees(visitor))
                for t
                in self.classes[self._active_class]
            ],
            []
        )

        self.sections[self._active_class][self._active_section].append((multiplier, trees))

    def eval_section_equation(self, equation, class_idx):
        ctx = {
            "n": self.ns[class_idx],
            "Cn": len(self.classes[class_idx]),
        }
        return eval(equation, ctx)

    def clear_all_classes(self):
        for i in range(len(self.sections)):
            self.clear_class(i)

    def clear_class(self, class_idx=None):
        class_idx = class_idx if class_idx is not None else self._active_class

        self.sections[class_idx] = [[] for _ in range(len(self.section_expressions[class_idx]))]

    def clear_section(self, class_idx, section_idx):
        class_idx = class_idx if class_idx is not None else self._active_class
        section_idx = section_idx if section_idx is not None else self._active_section

        self.sections[class_idx][section_idx] = []

    def clear_cache(self):
        for key in self._cached:  # set by @cached_property
            try:
                delattr(self, key)
            except AttributeError:
                pass

    def clear_stats_cache(self):
        for key in ["plus", "minus", "diff"]:
            try:
                delattr(self, key)
            except AttributeError:
                pass

    def print_all_classes_stats(self, class_idx=None):
        print("=== Classes stats ===")

        for i in range(len(self.sections)):
            self.print_class_stats(i, show_header=False)

    def print_class_stats(self, class_idx=None, show_header=True):
        if show_header:
            print("=== Class stats ===")

        class_idx = class_idx if class_idx is not None else self._active_class

        for i in range(len(self.sections[class_idx])):
            self.print_section_stats(class_idx, i, show_header=False)

    def print_section_stats(self, class_idx=None, section_idx=None, show_header=True):
        if show_header:
            print("=== Section stats ===")

        class_idx = class_idx if class_idx is not None else self._active_class
        section_idx = section_idx if section_idx is not None else self._active_section

        section_count = self.section_counts[class_idx][section_idx]
        equation, introductions = self.section_expressions[class_idx][section_idx]
        count = sum(map(lambda x: x[0] * len(x[1]), self.sections[class_idx][section_idx]))

        ready = section_count == count

        print(f"[{'x' if ready else ' '}]  {class_idx},{section_idx}: {count:5d} of {section_count:5d} | {equation:25} [{introductions}]")

    def print_diff_stats(self):
        print("=== Diff stats ===")
        result = defaultdict(lambda: [0, 0])

        for i in range(2):
            for k in self.diff[i]:
                key = k[1][:2]
                result[key][i] += 1

        for key in result:
            print(f"{key[0]},{key[1]}: {result[key][0]:5d} {result[key][1]:5d}")

    def print_stats(self):
        self.print_all_classes_stats()
        self.print_diff_stats()

    def display_diff_trees(self, class_idx=None, section_idx=None, part_idx=None):
        self.display_diff_trees_side(0, class_idx, section_idx, part_idx)
        self.display_diff_trees_side(1, class_idx, section_idx, part_idx)

    def display_diff_trees_side(self, side, class_idx=None, section_idx=None, part_idx=None):
        from IPython.display import display, HTML
        import pyAgrum.lib.notebook as gnb

        filter_key = lambda x: \
            (class_idx is None or x[1][0] == class_idx) and \
            (section_idx is None or x[1][1] == section_idx) and \
            (part_idx is None or x[1][2] == part_idx)

        trees = filter(filter_key, self.diff[side])

        display(HTML(f"=== {'Minus' if side == 0 else 'Plus'} ==="))
        for tree, _ in trees:
            gnb.sideBySide(tree, tree.extra["base"])

    def display_trees(self, class_idx=None, section_idx=None, part_idx=None):
        if class_idx is None:
            for i in range(len(self.sections)):
                self.display_trees(i)
        elif section_idx is None:
            for i in range(len(self.sections[class_idx])):
                self.display_trees(class_idx, i)
        elif part_idx is None:
            for i in range(len(self.sections[class_idx][section_idx])):
                self.display_trees(class_idx, section_idx, i)
        else:
            from IPython.display import display, HTML
            import pyAgrum.lib.notebook as gnb

            multiplier, trees = self.sections[class_idx][section_idx][part_idx]

            display(HTML(f"{class_idx},{section_idx},{part_idx}: {multiplier} * {len(trees)}"))

            for tree in trees:
                gnb.sideBySide(tree, tree.extra["base"])
