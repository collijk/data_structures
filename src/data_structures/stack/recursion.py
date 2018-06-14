from .stack import Stack


def array_sum_recursive(array):
    if array:
        return array[0] + array_sum_recursive(array[1:])
    return 0


def fibonacci_recursive_good(n, a=1, b=1):
    if n == 0:
        return a
    return fibonacci_recursive_good(n-1, b, a+b)


def fibonacci_recursive_bad(n):
    if n <= 1:
        return 1
    return fibonacci_recursive_bad(n-1) + fibonacci_recursive_bad(n-2)


def ackermann_recursive(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann_recursive(m - 1, 1)
    return ackermann_recursive(m - 1, ackermann_recursive(m, n-1))


class DontUseExponentialAlgorithmsError(Exception):
    pass


def fibonacci_stack(n, show_stack=False):
    if n > 10:
        raise DontUseExponentialAlgorithmsError("You'd be sad if I let you.")

    s = Stack(maxsize=10000)

    s.push('fib')
    s.push(n)

    while len(s) > 1:
        if show_stack:
            print(s._storage)

        arguments = []
        while not isinstance(s.peek(), str):
            arguments.append(s.pop())

        current_op = s.pop()

        if current_op == 'fib':
            fib_arg = arguments.pop()

            for a in arguments:
                s.push(a)

            if fib_arg <= 1:
                s.push(1)
            else:
                s.push('sum')
                s.push('fib')
                s.push(fib_arg-2)
                s.push('fib')
                s.push(fib_arg-1)

        else:  # current_op == 'sum':
            arg1, arg2 = arguments  # Sum works on two operands
            s.push(arg1 + arg2)

    return s.pop()




