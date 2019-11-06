def result_func(array):
    array = sorted(array)
    pairs = []
    sum_array = []

    print(array)
    print(pairs)
    print(sum_array)
    print()

    while len(array):
        if len(array) > 1:
            if array[-1] > 0:
                mult = array[-1] * array[-2]
                add = array[-1] + array[-2]

                if mult > add:
                    pairs.append((array.pop(-1), array.pop(-1)))
                    sum_array.append(mult)
                else:
                    pairs.append(array[-1])
                    sum_array.append(array.pop(-1))

            else:
                mult = array[0] * array[1]
                add = array[0] + array[1]

                if mult > add:
                    pairs.append((array.pop(0), array.pop(0)))
                    sum_array.append(mult)
                else:
                    pairs.append(array[-1])
                    sum_array.append(array.pop(-1))
        else:
            pairs.append(array[-1])
            sum_array.append(array.pop(-1))

    # while len(array):
    #     if len(array) > 1:
    #         mult = array[-1] * array[-2]
    #
    #         if mult > 0:
    #             if array[-1] > 0:
    #                 pairs.append((array.pop(-1), array.pop(-1)))
    #                 sum_array.append(mult)
    #             elif array[-1] < 0:
    #                 mult = array[1] * array[0]
    #                 pairs.append((array.pop(0), array.pop(0)))
    #                 sum_array.append(mult)
    #             else:
    #                 exit(1)
    #         elif mult == 0:
    #             if array[-1] > 0:
    #                 pairs.append(array[-1])
    #                 sum_array.append(array.pop(-1))
    #             elif array[-1] == 0:
    #                 if len(array) % 2 == 0:
    #                     pairs.append((array.pop(-1), array.pop(-1)))
    #                     sum_array.append(mult)
    #                 else:
    #                     pairs.append(array.pop(-1))
    #                     sum_array.append(mult)
    #             else:
    #                 exit(2)
    #         elif mult < 0:
    #             pairs.append(array[-1])
    #             sum_array.append(array.pop(-1))
    #     else:
    #         pairs.append(array[-1])
    #         sum_array.append(array.pop(-1))

        print(array)
        print(pairs)
        print(sum_array)
        print()

    return pairs, sum_array, sum(sum_array)


a = [-5, -3, -1, 0, 2, 5, 7]

print(result_func(a))
print("---------------")

b = [0]

print(result_func(b))
print("---------------")

c = [1]

print(result_func(c))
print("---------------")

d = [-3]

print(result_func(d))
print("---------------")

e = [2, 5, 7]

print(result_func(e))
print("---------------")

f = [2, 5, 7, 6]

print(result_func(f))
print("---------------")

f = [0, 2, 5, 7]

print(result_func(f))
print("---------------")

f = [0, 2, 5, 7, 6]

print(result_func(f))
print("---------------")

f = [-1, 2, 5, 7, 6]

print(result_func(f))
print("---------------")

f = [-1, 2, 5, 7]

print(result_func(f))
print("---------------")

f = [-1, 0, 2, 5, 7]

print(result_func(f))
print("---------------")

f = [-1, 0, 2, 5, 7, 6]

print(result_func(f))
print("---------------")

f = [-3, -1, 0, 2, 5, 7]

print(result_func(f))
print("---------------")

f = [-3, -1, 0, 2, 5, 7, 6]

print(result_func(f))
print("---------------")

f = [-5, -3, -1]

print(result_func(f))
print("---------------")

f = [-5, -3]

print(result_func(f))
print("---------------")

f = [-5, -3, -1, 0]

print(result_func(f))
print("---------------")

a = [-5, -3, -1, 0, 2]

print(result_func(a))
print("---------------")

a = [-5, -3, -1, 0, 2, 5]

print(result_func(a))
print("---------------")

a = [-5, -3, -1, 2]

print(result_func(a))
print("---------------")

a = [-5, -3, -1, 2, 5]

print(result_func(a))
print("---------------")

a = [-5, -3, -1, 2, 5, 7]

print(result_func(a))
print("---------------")

a = [-5, -3, -1, 0, 0, 2, 5, 7]

print(result_func(a))
print("---------------")

a = [-6, -5, -3, -1, 0, 0, 0, 2, 5, 7]

print(result_func(a))
print("---------------")

a = [0, 1, 2, 3, 4, 5]

print(result_func(a))
print("---------------")

a = [-1, 0, 1]

print(result_func(a))
print("---------------")

a = [1, 1]

print(result_func(a))
print("---------------")

a = [-1, -1]

print(result_func(a))
print("---------------")
