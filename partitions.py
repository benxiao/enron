import random

arr = list(range(100))
random.shuffle(arr)


def partition(arr, s, e):
    pivot_index = s
    pivot_value = arr[s]
    for j in range(s, e):
        if arr[j] < pivot_value:
            pivot_index += 1
            arr[j], arr[pivot_index] = arr[pivot_index], arr[j]
    arr[s], arr[pivot_index] = arr[pivot_index], arr[s]
    return pivot_index


def multipartition(arr, np=None):
    np = np or 2
    group = {(0, len(arr))}
    n = 1
    while n < np:
        max_partition = max(group, key=lambda x: x[1] - x[0])
        pivot = partition(arr, *max_partition)
        group.remove(max_partition)
        group.add((max_partition[0], pivot))
        group.add((pivot + 1, max_partition[1]))
        n += 1

    return sorted(group, key=lambda x: x[0])


print(multipartition(arr, np=4))
print(arr)
