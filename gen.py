from PIL import Image
import numpy as np

# Map production rules (current state -> next state)
rules = {
    (True, True, True) : False,
    (True, True, False) : False,
    (True, False, True) : False,
    (True, False, False) : True,
    (False, True, True) : True,
    (False, True, False) : True,
    (False, False, True) : True,
    (False, False, False) : False,
}

# Generage based on rules
def new_state(state):
    # Always pad state with two empty cells on either side
    # This allows any 3 cell rule to be realized
    ns = [False, False] # New state

    for i in range(len(state)-2):
        ns.append( rules[ tuple(state[i:i+3]) ] )

    # End padding
    ns.extend([False, False])

    return ns

# Number of epochs generated, this includes the initial state
NUM_EPOCHS = 200
# Initial state
cur_state = [False, False, True, False, False]
# Create 2D array to store full generation history
states = np.zeros( (NUM_EPOCHS, len(cur_state) + NUM_EPOCHS*2) )

for epoch in range(NUM_EPOCHS):
    # Record state into forever land
    for i in range(len(cur_state)):
        # Translate cells to center image
        states[epoch, i+(NUM_EPOCHS-epoch)] = 255 if cur_state[i] else 0

    # Update
    cur_state = new_state( cur_state )

# Create bitmap image
img = Image.fromarray(states)
img.show()
