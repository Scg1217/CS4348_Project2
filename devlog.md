## [2025-04-12 4:23]
**Thoughts so far:**
- Reviewed the project requirements for the bank simulation.
- The simulation will involve 3 teller threads and 50 customer threads interacting through shared resources.
- Key shared resources include:
  - The bank door (only 2 customers allowed concurrently),
  - The safe (only 2 tellers at a time),
  - The bank manager (only one teller at a time for withdrawal transactions).
- Each thread prints detailed messages to indicate its state and actions.

**Plan for this session:**
- Initialize a new local Git repository.
- Create the `devlog.md` file in the repository root.
- Create an initial project file (e.g., `bank_simulation.py`).
- Record this planning phase in the devlog.
- Commit the devlog and initial project files.

## [2025-04-12 5:10]
**Thoughts so far:**
- Created the initial `bank_simulation.py` file with skeleton classes for Teller and Customer.
- Defined basic behavior:
  - Each Teller prints a “ready” message and later an “ending session” message.
  - Each Customer simulates arrival, waits in line, and then prints a leaving message.
- The initial test with 3 Teller threads and 5 Customer threads produced the expected output.

**Plan for this session:**
- Verify that the simulation runs without errors on Python 2.7.5.
- Prepare to add shared resources (semaphores) and basic interaction between the threads in the next session.
