#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import threading
import time
import random

# Global shared resources:
# Only 2 customers can be in the bank at one time.
door_sem = threading.Semaphore(2)
# Only 2 tellers are allowed in the safe concurrently.
safe_sem = threading.Semaphore(2)
# Only 1 teller may interact with the manager at one time.
manager_sem = threading.Semaphore(1)

# A condition to coordinate waiting customers.
customer_condition = threading.Condition()
# Global queue to hold waiting customers.
customer_queue = []

# Global counters for served customers.
served_customers = 0
served_lock = threading.Lock()
TOTAL_CUSTOMERS = 0  # Will be set in main()

# Teller thread class
class Teller(threading.Thread):
    def __init__(self, teller_id):
        threading.Thread.__init__(self)
        self.teller_id = teller_id

    def run(self):
        # Print that the teller is ready to serve
        print("Teller {}: Ready to serve".format(self.teller_id))
        global served_customers, TOTAL_CUSTOMERS
        while True:
            # Wait for a customer to be available.
            customer = None
            with customer_condition:
                while len(customer_queue) == 0:
                    # If all customers have been served, exit the loop.
                    with served_lock:
                        if served_customers >= TOTAL_CUSTOMERS:
                            break
                    customer_condition.wait(0.1)
                # Check if a customer is available.
                if len(customer_queue) > 0:
                    customer = customer_queue.pop(0)
                else:
                    # Double-check if served customers equal total.
                    with served_lock:
                        if served_customers >= TOTAL_CUSTOMERS:
                            break
                    continue

            # Start processing the customer.
            print("Teller {} [Customer {}]: Starting transaction".format(self.teller_id, customer.customer_id))
            
            # For a withdrawal, interact with the manager.
            if customer.transaction_type == "withdraw":
                print("Teller {} [Customer {}]: Waiting for manager permission".format(self.teller_id, customer.customer_id))
                manager_sem.acquire()
                print("Teller {} [Customer {}]: Got manager permission".format(self.teller_id, customer.customer_id))
                time.sleep(random.uniform(0.005, 0.03))  # Simulate manager interaction delay.
                manager_sem.release()
                print("Teller {} [Customer {}]: Released manager".format(self.teller_id, customer.customer_id))

            # Access the safe.
            print("Teller {} [Customer {}]: Waiting for safe access".format(self.teller_id, customer.customer_id))
            safe_sem.acquire()
            print("Teller {} [Customer {}]: In safe, processing transaction".format(self.teller_id, customer.customer_id))
            time.sleep(random.uniform(0.01, 0.05))  # Simulate transaction time.
            print("Teller {} [Customer {}]: Exiting safe".format(self.teller_id, customer.customer_id))
            safe_sem.release()
            
            # Signal the customer that the transaction is complete.
            print("Teller {} [Customer {}]: Transaction complete".format(self.teller_id, customer.customer_id))
            customer.served_event.set()

            # Update the count of served customers.
            with served_lock:
                served_customers += 1
            print("Teller {}: Finished serving Customer {}".format(self.teller_id, customer.customer_id))
        
        print("Teller {}: No more customers, ending session".format(self.teller_id))

# Customer thread class
class Customer(threading.Thread):
    def __init__(self, customer_id):
        threading.Thread.__init__(self)
        self.customer_id = customer_id
        # Randomly choose transaction type: deposit or withdraw.
        self.transaction_type = random.choice(["deposit", "withdraw"])
        # Event to be set when the transaction is complete.
        self.served_event = threading.Event()


    def run(self):
        # Simulate customer arrival with a random delay (0 to 0.1 seconds)
        time.sleep(random.uniform(0.0, 0.1))
        door_sem.acquire()
        print("Customer {}: Entered the bank (Transaction: {})".format(self.customer_id, self.transaction_type))
        # Enter the waiting line.
        with customer_condition:
            customer_queue.append(self)
            print("Customer {}: Waiting in line".format(self.customer_id))
            customer_condition.notify()
        # Wait until a teller signals that the transaction is complete.
        self.served_event.wait()
        print("Customer {}: Transaction complete, leaving the bank".format(self.customer_id))
        # Release the door semaphore as the customer leaves.
        door_sem.release()

def main():
    global TOTAL_CUSTOMERS
    # Create and start 3 teller threads
    tellers = [Teller(i) for i in range(3)]
    for teller in tellers:
        teller.start()

    # Create 50 customer threads.
    customer_list = [Customer(i) for i in range(50)]
    TOTAL_CUSTOMERS = len(customer_list)
    for customer in customer_list:
        customer.start()

    # Wait for all customers to finish.
    for customer in customer_list:
        customer.join()

    # Notify any waiting teller threads (in case they are waiting in the condition).
    with customer_condition:
        customer_condition.notifyAll()

    # Wait for all teller threads to finish.
    for teller in tellers:
        teller.join()

if __name__ == "__main__":
    main()
