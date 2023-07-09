#---------------------------------------------------#
#                   Antonio Pelusi                  #
#---------------------------------------------------#

#-------------------- LIBRARIES --------------------#

import numpy as np
import matplotlib.pyplot as plt

#--------------------- CLASSES ---------------------#

class randomgrid():
    def __init__(self, grid_size, key=0):
        self.size = grid_size
        
        if key != 0:
            np.random.seed(key)
            
            self.grid = np.random.randint(2, size=(self.size, self.size))
        else:
            self.grid = np.zeros(dtype=int, shape=(self.size, self.size))

    def __repr__(self):
        str_pg = str()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[j][i] == 1:
                    str_pg += "██"
                else:
                    str_pg += "  "
            str_pg += "\n"
        return str_pg        

    def _count_neighbors(self, i, j):
        counter = int(
                    self.grid[i, (j-1)%self.size]
                  + self.grid[i, (j+1)%self.size]
                  + self.grid[(i-1)%self.size, j]
                  + self.grid[(i+1)%self.size, j]
                  + self.grid[(i-1)%self.size, (j-1)%self.size]
                  + self.grid[(i-1)%self.size, (j+1)%self.size]
                  + self.grid[(i+1)%self.size, (j-1)%self.size]
                  + self.grid[(i+1)%self.size, (j+1)%self.size]
                )
        
        return counter

    def next_iteration(self): #Game of Life rules
        #create new iteration grid
        new_iteration = randomgrid(self.size)

        for j in range(self.size):
            for i in range(self.size):

                #count neighbors
                livingneighbors = self._count_neighbors(i, j)

                #case >3: reproduction
                if self.grid[i][j] == 0:
                    if livingneighbors == 3:
                        new_iteration.grid[i][j] = 1
                
                elif self.grid[i][j] == 1:
                    #case ==2 or ==3: continue to live
                    if (livingneighbors == 2) or (livingneighbors == 3):
                        new_iteration.grid[i][j] = 1
                    #case <2 or >3: death
                    elif (livingneighbors < 2) or (livingneighbors > 3):
                        new_iteration.grid[i][j] = 0
                    
        return new_iteration

#------------------- FUNCTIONS ---------------------#

def bits_hash(pg):
    #sum the grid bits in a string
    bits = str()
    for i in range(pg.size):
        for j in range(pg.size):
            bits += str(pg.grid[j][i])
    
    #remove strings of "0" with a length of 5, usually created during Game Of Life iterations
    bits = bits.replace("0"*5, "")

    #bits shuffle
    bits = list(bits)
    np.random.shuffle(bits)
    bits = "".join(bits)

    #convert groups of 4 binary bits into hexadecimal values
    hex_bits = [hex(int(bits[n:n+4], 2))[2:].upper() for n in range(0, len(bits), 4)]
    
    #hash shuffle
    np.random.shuffle(hex_bits)
    hex_bits = "".join(hex_bits)

    return hex_bits

#---------------------- MAIN -----------------------#

def CA_hash(plain_text, hash_length=512, iter=5, grid_size=128, print_grid=False):

    #assertions
    if plain_text == "":
        raise ValueError("Empty plain text")
    
    if hash_length < 0:
        raise ValueError("Hash length not valid: can't be a negative number")
    
    if iter < 0:
        raise ValueError("Game of Life iteration not valid: can't be a negative number")
    
    if grid_size < 0:
        raise ValueError("Grid size not valid: can't be a negative number")

    #key is the decimal hash of the plaintext
    key = list(plain_text.encode('utf-8'))

    #create random grid using the key as a seed
    pg = randomgrid(grid_size, key)

    if print_grid:
        print("\n")
        print("Initial grid:")
        print(pg)

    #execute the non-reversible Game of Life iterations
    for _ in range(iter):
        pg = pg.next_iteration()

    if print_grid:
        print(f"After {iter} iterations:")
        print(pg)

    #calculate hash of the bits string
    hashed_text = bits_hash(pg)

    #check if there is enough entropy to get the hash with the desired size
    if hash_length > len(hashed_text):
        raise ValueError(f"Not enough entropy to get an hash of {hash_length} characters")

    #trim the hash to the desired size
    if hash_length != 0:
        hashed_text = hashed_text[:hash_length]

    #return hashed text
    return hashed_text

#----------------------- USE -----------------------#

#-------------------#
#       modes       #
#-------------------#
# - hash:       0   #
# - bias_test:  1   #
#-------------------#
mode = 0
#-------------------#


if mode == 0:
    #try the hash function changing the following keyword parameters
    hashed_text = CA_hash(input("\nPlain text:\n"), hash_length=512, iter=5, grid_size=128, print_grid=False)

    #print the hashed text
    print(f"\nHashed text:\n{hashed_text}")
    print(f"\nHash length:\n{len(hashed_text)}")

elif mode == 1:
#-----------------------#
    n_iteration = 10
#-----------------------#

    count = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}

    total_count = 0

    for n in range(n_iteration):
        hashed_text = CA_hash(str(n), hash_length=512, iter=5, grid_size=128)
        for c in hashed_text:
            count[c] += 1

        total_count += len(hashed_text)

    print(count)

    plt.figure(figsize=(10,5))
    plt.bar(list(count.keys()), list(count.values()))
    plt.title("Total count:" + str(total_count))
    plt.xlabel('Value')
    plt.ylabel('Count')

    plt.show()
