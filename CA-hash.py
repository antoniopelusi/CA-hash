#---------------------------------------------------#
#                   Antonio Pelusi                  #
#---------------------------------------------------#

#-------------------- LIBRARIES --------------------#

import numpy as np

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

def bits_hash(bits, hash_length):
    #join the single hex values excluding the 0
    hex_list = ''.join(['%x' % int(bits[i:i+8], 10) for i in range(0, len(bits), 8) if int(bits[i:i+8]) != 0])

    #split in single characters
    hex_list = [c for c in list(hex_list)]

    #select characters randomly to create the final hash with a better entropy
    hashed_text = ''.join([hex_list[np.random.randint(len(hex_list))] for _ in range(hash_length)])

    return hashed_text

#---------------------- MAIN -----------------------#

def CA_hash(plain_text, hash_length=512, iter=100, grid_size=64, print_grid=False):

    #assertions
    if plain_text == "":
        raise ValueError("Empty plain text")
    
    if hash_length > 512 or hash_length <1:
        raise ValueError("Hash length not valid, limits: (1, 512)")
    
    if iter < 0:
        raise ValueError("Game of Life iteration number not valid: can't be a negative number")
    
    if grid_size < 0:
        raise ValueError("grid size not valid: can't be a negative number")

    #key is the decimal hash of the plaintext
    key = list(plain_text.encode('utf-8'))
    print(key)
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

    #sum the grid bits in a string
    bits = str()
    for i in range(pg.size):
        for j in range(pg.size):
            bits += str(pg.grid[i][j])

    #calculate hash of the bits string
    hashed_text = bits_hash(bits, hash_length)

    #print the hashed text
    print(f"Hashed text: {hashed_text}")

#---------------------- TEST -----------------------#

#try the hash function changing the following keyword parameters
CA_hash(input("Plain text: "), hash_length=512, iter=100, grid_size=64, print_grid=True)
