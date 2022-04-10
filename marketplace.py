"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


from asyncio.log import logger
from logging.handlers import RotatingFileHandler
from multiprocessing import Lock
from pickle import FALSE, TRUE
from string import Formatter
from time import gmtime, sleep
import threading
import unittest
from tema.product import Coffee
from tema.product import Tea
from tema.producer import Producer
from tema.consumer import Consumer
import logging

# Aici implementez partea logging a temei, folosindu-ma de
# link-urile de pe ocw.

logging.basicConfig(filename='marketplace.log', level=logging.INFO)
logging.Formatter.converter = gmtime()

file_handler = RotatingFileHandler('marketplace.log', maxBytes=10000, backupCount=10)
mkt_logger = logging.getLogger('logger')
mkt_logger.addHandler(file_handler)


class TestMarketplace(unittest.TestCase):
    """
    Aceasta este clasa pentru partea unittesting a temei.
    """
    def setUp(self):
        """
        In aceasta metoda fac instantieri ale claselor si retin date pe care
        le folosesc ulterior pentru testare. Datele le-am luat din testul 1
        de input, din cele trimise pentru testarea temei.
        """
        self.marketplace = Marketplace(15)
        self.products = []
        self.product_id1 = Coffee(name='Indonezia', acidity='5.05', roast_level='MEDIUM', price=1)
        self.product_id2 = Tea(name='Linden', type='Herbal', price=9)

        self.producers = []
        self.producers.append(Producer(products=[[self.product_id2, 2, 0.18],
                                                 [self.product_id1, 1, 0.23]],
                                        marketplace=self.marketplace, republish_wait_time=0.15))
        self.consumers = []
        self.consumers.append(Consumer(carts=[[{"type": "add", "product": "id2", "quantity": 1},
                                               {"type": "add", "product": "id1", "quantity": 3},
                                               {"type": "remove", "product": "id1", "quantity": 1}]], 
                                       marketplace=self.marketplace,
                                       retry_wait_time=0.31))
        self.cart_id = -1
        self.carts = []

    def test_register_producer(self):
        """
        In aceasta functie testez corectitudinea functiei register_producer.
        """
        # Retin rezultatul pe care ar trebui sa il obtin, daca rulez functia register_producer.
        self.producers[0].id = 1
        # Compar rezultatul obtinut cu ce trebuie sa obtin.
        self.assertEqual(self.marketplace.producer_id, 1)

    def test_publish(self):
        """
        In aceasta metoda testez functionalitatea metodei publish.
        """
        producer_id = self.producers[0].id

        # retin intr-o lista rezultatele pe care ar trebui sa le primesc
        self.products.append(self.product_id2)
        self.products.append(self.product_id2)
        self.products.append(self.product_id1)

        # apelez publish pentru fiecare obiect pe care vreau sa il adaug
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)

        # verific daca rezultatele sunt egale
        self.assertEqual(self.marketplace.producers_products[producer_id - 1], self.products)

    def test_new_cart(self):
        """
        In aceasta metoda testez functionalitatea metodei new_cart.
        """
        # apelez functia new_cart
        self.cart_id = self.marketplace.new_cart()
        # compar ce am obtinut eu cu ce ar trebui sa obtin
        self.assertEqual(self.cart_id, 0)

    def test_add_to_cart(self):
        """
        In aceasta metoda testez functionalitatea metodei add_to_cart.
        """
        # retin intr-o lista rezultatele pe care ar trebui sa le obtin
        self.carts.append([])
        self.cart_id = self.marketplace.new_cart()
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id2)

        producer_id = self.producers[0].id

        # apelez publish pana cand se umple buffer-ul de produse pentru
        # producator
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)

        # apelez add_to_cart pentru fiecare operatie de tipul 'add'
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id2)

        # compar rezultatele obtinute
        self.assertEqual(self.marketplace.carts_list[self.cart_id], self.carts[self.cart_id])

    def test_remove_from_cart(self):
        """
        In aceasta metoda testez functionalitatea metodei remove_from_cart.
        """
        # retin ce ar trebui sa obtin intr-o lista
        self.carts.append([])
        self.cart_id = self.marketplace.new_cart()
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id2)

        producer_id = self.producers[0].id
        # umplu buffer-ul asociat producatorului cu produse, adica
        # adaug 15 elemente
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)

        # fac operatiile din lista carts a consumatorului (add si remove)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id2)
        self.marketplace.remove_from_cart(self.cart_id, self.product_id1)

        # compar rezultatele
        self.assertEqual(self.marketplace.carts_list[self.cart_id], self.carts[self.cart_id])
    
    def test_place_order(self):
        """
        In aceasta metoda testez functionalitatea metodei place_order.
        """
        producer_id = self.producers[0].id
        # retin ce ar trebui sa primesc intr-o lista
        self.carts.append([])
        self.cart_id = self.marketplace.new_cart()
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id1)
        self.carts[self.cart_id].append(self.product_id2)

        # umplu buffer-ul asociat producatorului cu produse, adica
        # adaug 15 elemente
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id2)
        self.marketplace.publish(str(producer_id), self.product_id1)

        # fac operatiile din lista carts a consumatorului (add si remove)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id1)
        self.marketplace.add_to_cart(self.cart_id, self.product_id2)
        self.marketplace.remove_from_cart(self.cart_id, self.product_id1)

        # afisez produsele din cos
        returned_value = self.marketplace.place_order(self.cart_id)

        # compar rezultatele
        self.assertEqual(returned_value, self.carts[self.cart_id])

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method init receives queue_size = %d\n', queue_size_per_producer)

        # retin numarul maxim de elemente pe care le poate adauga un producator
        # in buffer-ul sau
        self.max_products_per_producer = queue_size_per_producer
        # creez un lock, pe care il voi folosi ca sa restrictionez accesul la
        # anumite zone de program
        self.lock_code = Lock()
        # aici retin id-ul producatorului; il initializez cu 0
        self.producer_id = 0
        # aici retin id-ul unui cos; il initializez cu 0
        self.cart_id = 0
        # aici retin o lista cu toate cosurile de produse ale consumatorilor
        self.carts_list = []
        # aici retin o lista de liste pentru produsele publicate de fiecare
        # producator
        self.producers_products = []
        # aici retin o lista de liste pentru produsele achizitionate de la fiecare producator
        self.taken_products = []

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method init does not return anything!\n')

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method register_producer does not receive arguments!\n')

        self.lock_code.acquire()
        # ii ofer un id nou unui nou producator; am acces
        # restictionat pe aceasta variabila, deoarece adunarea
        # nu este operatie atomica
        self.producer_id = self.producer_id + 1
        self.lock_code.release()

        # creez o noua intrare in lista de produse a fiecarui prodycator
        self.producers_products.append([])
        self.taken_products.append([])

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method register_producer returns producer_id = %d\n', self.producer_id)

        # intorc id-ul noului producator
        return self.producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('producer_id = %d, product = %s', int(producer_id) - 1, str(product))

        # producatorul producer_id adauga un produs nou in buffer-ul sau
        self.producers_products[int(producer_id) - 1].append(product)
        # verific daca adaugarea s-a efectuat cu succes
        if product in self.producers_products[int(producer_id) - 1]:
            # afisez un mesaj de log (pentru partea de logging a temei)
            logging.info('Method publish returns True!\n')
            # returnez True
            return True

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method publish returns False!\n')
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method new_cart does not receive anything!\n')

        new_cart_element = []
        # adaug un nou cos de cumparaturi in lista de cosuri din marketplace
        self.carts_list.append(new_cart_element)

        self.lock_code.acquire()
        # retin noul id
        cart_id = len(self.carts_list) - 1
        self.lock_code.release()

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method new_cart returns cart_id = %d\n', cart_id)
        # intorc id-ul noului cos de cumparaturi
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method add_to_cart receives cartd_id = %d and product = %s',
                     cart_id, str(product))

        # cu aceasta variabila iterez prin lista de produse a fiecarui producator
        index_market = 0
        # aici retin id-ul producatorului din care iau un produs (daca il gasesc)
        id_producer = -1
        nr_of_lists = len(self.producers_products)

        # cat timp nu am terminat de parcurs lista
        while index_market < nr_of_lists:
            if product in self.producers_products[index_market]:
                id_producer = index_market
                break
            index_market = index_market + 1
        # daca nu am gasit produsul la niciun producator, returnez false
        if id_producer == -1:
            # afisez un mesaj de log (pentru partea de logging a temei)
            logging.info('Method add_to_cart returns False!\n')
            return False

        # adaug produsul dorit in cos
        self.carts_list[cart_id].append(product)
        # marchez produsul dorit de la producatorul sau ca fiind "luat"
        self.taken_products[id_producer].append(product)
        # elimin produsul respectiv din lista de produse a prodicatorului sau
        self.producers_products[id_producer].remove(product)

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method add_to_cart returns True!\n')
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method remove_from_cart receives cart_id = %d and product = %s\n',
                        cart_id, str(product))

        # cu aceasta variabila ieterez prin lista de produse restrictionate
        index_market = 0
        # aici retin id-ul producatorului de la care am luat produsul
        producer_id = -1
        self.carts_list[cart_id].remove(product)
        
        # pentru produsul pe care vreau sa il restitui, caut ce producator are
        while index_market < len(self.taken_products):
            if product in self.taken_products[index_market]:
                producer_id = index_market
                break

            index_market = index_market + 1
        
        # elimin produsul din lista de produse luate a producatorului respectiv
        self.taken_products[producer_id].remove(product)
        # restitui produsul
        self.producers_products[producer_id].append(product)

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method remove_from_cart does not return anything!\n')

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method place_order receives cart_id = %d\n', cart_id)

        # folosesc aceasta variabila ca sa iterez prin lista de produse dintr-un cos
        index_market = 0
        nr_of_products = len(self.carts_list[cart_id])

        # afisez produsele din cos
        self.lock_code.acquire()
        if nr_of_products >= 1:
            while index_market < nr_of_products:
                product = self.carts_list[cart_id][index_market]
                print(str(threading.currentThread().getName()) + " bought " + str(product))
                index_market = index_market + 1

        self.lock_code.release()

        # afisez un mesaj de log (pentru partea de logging a temei)
        logging.info('Method place_order returns cart = %s\n', str(self.carts_list[cart_id]))
        return self.carts_list[cart_id]
