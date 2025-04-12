#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import threading
import time
import random

# Teller thread class
class Teller(threading.Thread):
    def __init__(self, teller_id):
        threading.Thread.__init__(self)
        self.teller_id = teller_id

    def run(self):
        # Print that the teller is ready to serve
        print("Teller {}: Ready to serve".format(self.teller_id))
        # For now, we simply simulate that the teller is waiting for customers.
        # In the future, code to wait for and process customer transactions will go here.
        time.sleep(0.1)  # Simulate minimal work
        print("Teller {}: Ending session".format(self.teller_id))

# Customer thread class
class Customer(threading.Thread):
    def __init__(self, customer_id):
        threading.Thread.__init__(self)
        self.customer_id = customer_id

    def run(self):
        # Simulate customer arrival with a random delay (0 to 0.1 seconds)
        time.sleep(random.uniform(0.0, 0.1))
        print("Customer {}: Arrived at the bank".format(self.customer_id))
        # Simulate the customer waiting in line
        time.sleep(random.uniform(0.05, 0.2))
        print("Customer {}: Waiting in line".format(self.customer_id))
        # Simulate the customer leaving after being served
        print("Customer {}: Leaving the bank".format(self.customer_id))

def main():
    # Create and start 3 teller threads
    tellers = [Teller(i) for i in range(3)]
    for teller in tellers:
        teller.start()

    # Create and start a few customer threads
    customers = [Customer(i) for i in range(5)]
    for customer in customers:
        customer.start()

    # Wait for all teller threads to complete
    for teller in tellers:
        teller.join()

    # Wait for all customer threads to complete
    for customer in customers:
        customer.join()

if __name__ == "__main__":
    main()
