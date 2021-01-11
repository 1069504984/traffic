# -*- coding: utf-8 -*-
# @Time    : 2020/7/31 9:41
# @Author  : Fighter
import functools
import time


def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print('{} took {} ms'.format(func.__name__, (end - start) * 1000))
        return res

    return wrapper


@log_execution_time
def bubble_sort(alist):
    for j in range(len(alist) - 1):
        for i in range(len(alist) - 1 - j):
            if alist[i] > alist[i + 1]:
                alist[i], alist[i + 1] = alist[i + 1], alist[i]
    return alist


@log_execution_time
def strengthen_bubble_sort(items):
    for i in range(len(items) - 1):
        flag = False
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                flag = True
        if not flag:
            break
    return items


@log_execution_time
def bubble_sort_2(nums):
    for i in range(len(nums) - 1):
        flag = False
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                flag = True
        if not flag:
            return nums
    return nums


@log_execution_time
def bubble_sort_double(items):
    for i in range(len(items) - 1):
        flag = False
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                flag = True
        if flag:
            flag = False
            for j in range(len(items) - 2 - i, 0, -1):
                if items[j - 1] > items[j]:
                    items[j], items[j - 1] = items[j - 1], items[j]
                    flag = True
        if not flag:
            break
    return items


@log_execution_time
def bubble_sort_4(my_list):
    length = len(my_list)
    for i in range(length - 1, -1, -1):
        for j in range(0, i):
            if my_list[j] > my_list[j + 1]:
                exchange = my_list[j]
                my_list[j] = my_list[j + 1]
                my_list[j + 1] = exchange


if __name__ == '__main__':
    li = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    li_0 = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    li_2 = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    li_3 = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    li_4 = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    li_5 = [1, 3, 2, 5, 4, 7, 6, 8, 9]
    # print(li)
    bubble_sort(li_0)
    bubble_sort_double(li)
    strengthen_bubble_sort(li_4)
    bubble_sort_2(li_5)
    bubble_sort_4(li_2)

    # print(li)
    # print(li_2)
    # print(li_3)

ignore_dict = {
    'youzan.retail.stock.receiving.order.export.1.0.0': ['response'],
    'youzan.retail.trademanager.refundorder.export.1.0.0': ['response'],
    'youzan.retail.trade.api.service.pay.qrcode.1.0.1': ['url'],
    'youzan.retail.product.spu.queryone.1.0.0': ['list']
}