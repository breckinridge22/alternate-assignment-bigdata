from time import time

'''
Given a list l = [] and target t, return True if there exists l[i] + l[j] == t.
Assume elements of l are positive and unique.

Note: you CANNOT use two nested loops.
'''


def targeted_sum(l, t):
    # could iterate through the list
    nums = set()
    # for each element in l
    for i in l:
        # if the element that can be added to i is in the set of things already visited
        # return True
        d = t - i
        if d in nums:
            return True
        nums.add(d)
    return False


def simple_targeted_sum(l, t):
    for i in l:
        for j in l:
            if i + j == t:
                return True

    return False


def test_target1():
    assert targeted_sum([1, 4, 3, 9], 5) is True


def test_target2():
    assert targeted_sum([1, 4, 3, 9], 51) is False


def test_target_time():
    l = range(0, 200)

    t1 = time()
    r1 = targeted_sum(l, 250)
    t2 = time() - t1

    t3 = time()
    r2 = simple_targeted_sum(l, 250)
    t4 = time() - t3

    assert r1 == r2
    assert t2 < t4
