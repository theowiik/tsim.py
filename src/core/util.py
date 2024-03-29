from typing import List


class ArrayUtils:
    @staticmethod
    def push_first(a: List[any], v: any) -> None:
        """
        Inserts the value to the first position in
        the array without increasing the size.
        "Pushes" the values down, so the last element
        will dissapear. Destructive method.

        Examples:
        a = [1, 2, 3];
        push_first(a, -4);
        print(a) -> [-4, 1, 2];
        """

        if a is None:
            raise ValueError("Array is None")

        if len(a) == 0:
            a.append(v)

        i = len(a) - 1
        while i > 0:
            a[i] = a[i - 1]
            i -= 1

        a[0] = v


def none_or_whitespace(s: str) -> bool:
    return not s or not s.strip()
