from transformator.tree import Tree


def main():
    t = Tree(("@", "l", "0", None, None, None, None))
    t.graph.view()

    t.visit_subtrees(lambda kind, left, right: ["l", kind] + left + right)


if __name__ == '__main__':
    main()
