"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        # aici retin operatiile pe produse pe care trebuie sa le fac
        self.products_list = carts
        # aici retin marketplace-ul
        self.marketplace = marketplace
        # aici retin timpul de asteptare in cazul in care o operatie esueaza
        self.time_to_wait = retry_wait_time

    def run(self):
        # ii dau consumatorului un cos nou din market
        cart = self.marketplace.new_cart()

        # iterez prin lista de operatii
        for new_cart in self.products_list:
            for product in new_cart:
                index_consumer = 0
                number_of_products = product['quantity']

                # cat timp inca nu am cumparat/eliminat toate produsele dorite
                while index_consumer < number_of_products:
                    # verific tipul operatiei
                    if str(product['type']) == 'add':
                        # retin valoarea intoarsa de apelul functiei add_to_cart
                        returned_val = self.marketplace.add_to_cart(cart, product['product'])

                        # daca operatia anterioara nu a avut loc cu succes
                        if not returned_val:
                            # astept time_to_wait secunde
                            sleep(self.time_to_wait)

                        # in caz contrar, trec la urmatorul produs
                        if returned_val:
                            index_consumer = index_consumer + 1
                    else:
                        # daca vreau sa elimin un produs din cos, apelez remove_from_cart
                        self.marketplace.remove_from_cart(cart, product['product'])
                        # trec la urmatorul produs
                        index_consumer = index_consumer + 1
            # dupa primul set de operatii, afisez produsele cumparate
            self.marketplace.place_order(cart)
            # eliberez cosul
            self.marketplace.carts_list[cart].clear()
    