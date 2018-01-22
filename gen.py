from PIL import Image
import numpy as np
import sys

# Map production rules (current state -> next state)
rules = {
    (True, True, True) : False,        #128	<> 128
    (True, True, False) : False,    #64	<> 8
    (True, False, True) : False,    #32 <> 32
    (True, False, False) : True,    #16 <> 2
    (False, True, True) : True,        #8 <>64
    (False, True, False) : True,    #4 <> 4
    (False, False, True) : True,    #2 <>16
    (False, False, False) : False,    #1 <> 1
}
def new_rule(key):
    for x in range(0,2):
        for y in range(0,2):
            for z in range(0,2):
                rules[(x==1,y==1,z==1)] = key%2 == 1
                key = int(round(key / 2 - 0.1))


# Generate based on rules
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
# Initial rule
new_rule(30)


# Create 2D array to store full generation history
states = np.zeros( (NUM_EPOCHS, len(cur_state) + NUM_EPOCHS*2) )
print(sys.argv)
for epoch in range(NUM_EPOCHS):
    #alternate between command line rule arguments successively
    new_rule(int(sys.argv[1+epoch % (len(sys.argv)-1)]))
    # Record state into forever land
    for i in range(len(cur_state)):
        # Translate cells to center image
        states[epoch, i+(NUM_EPOCHS-epoch)] = 255 if cur_state[i] else 0

    # Update
    cur_state = new_state( cur_state )

# Create bitmap image
img = Image.fromarray(states)
img.show()
