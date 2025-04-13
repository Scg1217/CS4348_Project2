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
        print("Teller {} []: Ready to serve".format(self.teller_id))
        global served_customers, TOTAL_CUSTOMERS
        while True:
            # Wait for a customer to be available.
            customer = None
            with customer_condition:
                print("Teller {} []: waiting for a customer".format(self.teller_id))
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
            if customer:
                customer.served_by = self.teller_id
                print("Customer {} [Teller {}]: selects teller".format(customer.customer_id, self.teller_id))
                print("Customer {} [Teller {}] introduces itself".format(customer.customer_id, self.teller_id))
                print("Teller {} [Customer {}]: serving a customer".format(self.teller_id, customer.customer_id))
                print("Teller {} [Customer {}]: asks for transaction".format(self.teller_id, customer.customer_id))
                time.sleep(0.01)  # Simulate small delay
                print("Customer {} [Teller {}]: asks for {} transaction".format(customer.customer_id, self.teller_id, customer.transaction_type))
                print("Teller {} [Customer {}]: handling {} transaction".format(self.teller_id, customer.customer_id, customer.transaction_type))
                if customer.transaction_type == "withdraw":
                    print("Teller {} [Customer {}]: going to the manager".format(self.teller_id, customer.customer_id))
                    manager_sem.acquire()
                    print("Teller {} [Customer {}]: getting manager's permission".format(self.teller_id, customer.customer_id))
                    time.sleep(random.uniform(0.005, 0.03))
                    print("Teller {} [Customer {}]: got manager's permission".format(self.teller_id, customer.customer_id))
                    manager_sem.release()
                print("Teller {} [Customer {}]: going to safe".format(self.teller_id, customer.customer_id))
                safe_sem.acquire()
                print("Teller {} [Customer {}]: enter safe".format(self.teller_id, customer.customer_id))
                time.sleep(random.uniform(0.01, 0.05))
                print("Teller {} [Customer {}]: leaving safe".format(self.teller_id, customer.customer_id))
                safe_sem.release()
                if customer.transaction_type == "deposit":
                    print("Teller {} [Customer {}]: finishes deposit transaction.".format(self.teller_id, customer.customer_id))
                else:
                    print("Teller {} [Customer {}]: finishes withdrawal transaction.".format(self.teller_id, customer.customer_id))
                print("Teller {} [Customer {}]: wait for customer to leave.".format(self.teller_id, customer.customer_id))
                customer.served_event.set()   # Signal customer that transaction is complete.
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
        self.served_by = None

    def run(self):
        # Wait a random time (simulate arrival delay).
        time.sleep(random.uniform(0.0, 0.1))
        # Acquire the bank door semaphore (only 2 customers allowed inside).
        print("Customer {} []: wants to perform a {} transaction".format(self.customer_id, self.transaction_type))
        print("Customer {} []: going to bank.".format(self.customer_id))
        door_sem.acquire()
        print("Customer {} []: entering bank.".format(self.customer_id))
        print("Customer {} []: getting in line.".format(self.customer_id))
        print("Customer {} []: selecting a teller.".format(self.customer_id))
        print("Customer {}: Entered the bank (Transaction: {})".format(self.customer_id, self.transaction_type))
        with customer_condition:
            customer_queue.append(self)
            customer_condition.notify()
        # Wait until a teller signals that the transaction is complete.
        self.served_event.wait()
        print("Customer {} [Teller {}]: leaves teller".format(self.customer_id, self.served_by))
        print("Customer {} []: goes to door".format(self.customer_id))
        door_sem.release()
        print("Customer {} []: leaves the bank".format(self.customer_id))

def main():
    global TOTAL_CUSTOMERS
    # Create 50 customer threads.
    customer_list = [Customer(i) for i in range(50)]
    TOTAL_CUSTOMERS = len(customer_list)
    
    # Create and start teller threads.
    tellers = [Teller(i) for i in range(3)]
    for teller in tellers:
        teller.start()

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
    print("Teller 0 []: leaving for the day")
    print("Teller 1 []: leaving for the day")
    print("Teller 2 []: leaving for the day")
    print("The bank closes for the day.")

if __name__ == "__main__":
    main()
