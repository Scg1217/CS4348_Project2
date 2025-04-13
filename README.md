# CS4348_Project2
# Bank Simulation Project

## Overview

This project simulates a bank where:
- **3 Teller threads** serve **50 Customer threads**.
- Customers are not allowed to enter the bank before it is open. The bank door permits only 2 customers at a time.
- Customers perform either deposit or withdrawal transactions.
- Withdrawal transactions require manager permission (only 1 teller may interact with the manager at a time).
- Transactions occur in the safe (only 2 tellers allowed in at once).
- Each thread prints detailed messages following the format: THREAD_TYPE ID [Related THREAD_TYPE ID]: MESSAGE
For example:
- `Teller 0 []: ready to serve`
- `Customer 0 []: wants to perform a deposit transaction`
- `Customer 0 [Teller 0]: selects teller`

## Files

- **bank_simulation.py**:  
Contains the complete simulation code implemented in Python 2.7.5 using the `threading` module and semaphores for synchronization.

- **devlog.md**:  
A development log documenting the progress and design decisions throughout the project.

- **README.md**:  
This file, describing the project, instructions for running the simulation, and an overview of the design.

## How to Run

This project is designed to run on the CS server (which has Python 2.7.5).

To run the simulation, navigate to the project directory on the CS server and execute:
python bank_simulation.py