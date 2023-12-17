def push_first(a, v):
    """
    Inserts the value to the first position in
    the array without increasing the size.
    "Pushes" the values down, so the last element
    will dissapear. Destructive method.

    Examples:
    a = [1, 2, 3]
    push_first(a, 0)
    a -> [0, 1, 2]
    """

    if a == None:
        raise Exception("Array is None")

    if len(a) == 0:
        a.append(v)

    i = len(a) - 1
    while i > 0:
        a[i] = a[i - 1]
        i -= 1

    a[0] = v


a = [1, 2, 3]
push_first(a, 333)
print(a)

a = [1, 2]
push_first(a, 333)

a = []
push_first(a, 333)

a = [1]
push_first(a, 333)

a = None
push_first(a, 333)
