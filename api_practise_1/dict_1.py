# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:16
# @Author  : Fighter
# dict_1={'data1':"{\'data\':\'123\',\'param\':\'456\'}"}
# new_dict=dict_1.get('data1')

# for i in range(1,6):
#     for j in range(0
#             ,5-i):
#      print('^',end='')
#     print('* '*i)
# 1X1 i j
# 1X2 2X2
# 1X3 2X3 3X3
import requests

# def find_product_price(products, product_id):
#     for id ,price in products:
#         if id == product_id:
#             return price
#     return None
def find_unique_price_using_set(products):
    unique_price_set=set()
    for _,price in products:
        unique_price_set.add(price)
    return len(unique_price_set)
products = [(143121312, 100), (432314553, 30),(32421912367, 150)]
print('The price of product 432314553 is {}'.format(find_unique_price_using_set(products)))


