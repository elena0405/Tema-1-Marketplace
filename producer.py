"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        # aici retin lista de produse pe care trebuie sa le adaug
        self.products_list = products
        # aici retin marketplace-ul
        self.marketplace = marketplace
        # aici retin timpul de asteptare pentru a republica un produs
        self.time_to_wait = republish_wait_time
        # aici retin id-ul producatorului
        self.id = self.marketplace.register_producer()
        # adaug o lista vida noua pentru produsele ce vor fi achizitionate de la
        # producatorul curent
        self.marketplace.taken_products.append([])

    def run(self):
        # retin numarul maxim de elemente ce pot fi adaugate de producator
        max_products_per_producer = self.marketplace.max_products_per_producer

        while True:
            # parcurg tuplul de produse
            for (name, quantity, time_to_wait) in self.products_list:
                # folosesc aceasta variabila ca sa contorizez numarul de produse de 
                # acelasi tip pe care le adaug
                index_producer = 0

                # cat timp nu am terminat de adaugat elementele 
                while index_producer < quantity:
                    # verific daca pot sa adaug produsul in lista de produse
                    if len(self.marketplace.producers_products[self.id - 1]) < max_products_per_producer:
                        # daca da, atunci apelez functia de adaugare a unui produs
                        returned_value = self.marketplace.publish(str(self.id), name)
                        # daca instructiunea de mai sus nu s-a efectuat cu succes
                        if not returned_value:
                            # astept un timp, pana cand incerc din nou
                            sleep(self.time_to_wait)
                        else:
                            # daca functia publish s-a executat cu succes, astept un timp
                            # si trec la produsul urmator
                            sleep(time_to_wait)
                            index_producer = index_producer + 1
                    else:
                        # daca nu mai pot adauga elemente, astept un timp
                        sleep(self.time_to_wait)
