def diff_sorted(first, second, key=None, first_label="first", second_label="second"):
    key = key or (lambda x: x)

    first_generator = iter(first)
    second_generator = iter(second)

    p = None
    q = None

    p_sent = True
    q_sent = True

    try:
        p = next(first_generator)
        p_sent = False

        q = next(second_generator)
        q_sent = False

        while True:
            k_p = key(p)
            k_q = key(q)

            if k_p == k_q:
                p_sent = True
                q_sent = True

                p = next(first_generator)
                p_sent = False

                q = next(second_generator)
                q_sent = False

            elif k_p < k_q:
                yield first_label, p
                p_sent = True

                p = next(first_generator)
                p_sent = False
            else:
                yield second_label, q
                q_sent = True

                q = next(second_generator)
                q_sent = False
    except StopIteration:
        pass

    try:
        if not p_sent:
            yield first_label, p

        while True:
            yield first_label, next(first_generator)
    except StopIteration:
        pass

    try:
        if not q_sent:
            yield second_label, q

        while True:
            yield second_label, next(second_generator)
    except StopIteration:
        pass
