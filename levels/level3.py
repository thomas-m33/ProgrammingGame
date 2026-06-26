from base import BaseLevelPage


class Level3Page(BaseLevelPage):
    def __init__(self, back_method):
        level_info = ("Unfortunately, Dave has been laid off from his job and he's now on a budget. "
                      "He wants to buy some bread from the shops but he isn't sure where it would be cheapest.\n\n"
                      "The dictionaries shop1, shop2 and shop3 contain the prices of various items at "
                      "stores close to Dave. Accessing one of these dictionaries with the key 'bread' will return the "
                      "price of bread there as a number.\n\n"
                      "To help Dave out, write an algorithm which will return the dictionary where he can get bread "
                      "for the cheapest. If multiple stores tie for the lowest price, return the one with the lower "
                      "number in its name.\n\n"
                      "Example:\n"
                      "shop1 = {\"bread\": 5, \"apple\": 2}\n"
                      "shop2 = {\"bread\": 3.50, \"orange\": 1}\n"
                      "shop3 = {\"bread\": 3.50, \"banana\": 1.50}\n\n"
                      "return {\"bread\": 3.50, \"orange\": 1}\n")

        func_name = "price_check"
        parameters = "shop1, shop2, shop3"

        io_dict = {'{"bread": 4.50}, {"bread": 3}, {"bread": 4}': {"bread": 3},
                   '{"bread": 2.90}, {"bread": 2.50}, {"bread": 2.65}': {"bread": 2.50},
                   '{"bread": 5}, {"bread": 5, "apples": 2}, {"bread": 5, "bananas": 2}': {"bread": 5},
                   '{"bread": 1}, {"bread": 2}, {"bread": 5}': {"bread": 1},
                   '{"bread": 25, "bananas": 2}, {"bread": 25, "apples": 2}, {"bread": 35}': {"bread": 25,
                                                                                              "bananas": 2},
                   '{"bread": 3}, {"bread": 2}, {"bread": 1}': {"bread": 1}}
        # Keys are inputs, values are the expected output of the function
        # Some dictionaries have more entries to distinguish them from other shops with the same bread price

        super().__init__(back_method, level_info, func_name, parameters, io_dict)

"""
Solution:

def price_check(shop1, shop2, shop3):
    price1 = shop1["bread"]
    price2 = shop2["bread"]
    price3 = shop3["bread"]

    if price1 <= price2:
        if price1 <= price3:	
            return shop1
        else:
            return shop3
    else:
        if price2 <= price3:
            return shop2
        else:
            return shop3


Alternatively you can use the min() function:

def price_check(shop1, shop2, shop3):
    shops = (shop1, shop2, shop3)
    return min(shops, key=lambda shop: shop["bread"])
"""
