#---------------------------------------------------#
#                   Antonio Pelusi                  #
#---------------------------------------------------#

#-------------------- LIBRARIES --------------------#

import numpy as np
import hashlib

#--------------------- CLASSES ---------------------#

class randomgrid():
    def __init__(self, size, key=0):
        self.size = size

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

#---------------------- MAIN -----------------------#

def CA_hash(plain_text, size=50, iter=100, stdout=False):
    #key is the decimal hash of the plaintext
    key = int(hashlib.sha512(plain_text.encode('utf-8')).hexdigest(), 16) % 10**8

    #create random grid using the key as a seed
    pg = randomgrid(size, key)

    if stdout:
        print("\n")
        print("Initial grid:")
        print(pg)

    #execute the non-reversible Game of Life iterations
    for _ in range(iter):
        pg = pg.next_iteration()

    if stdout:
        print(f"After {iter} iterations:")
        print(pg)

    #sum the matrix bits in a string
    bits = str()
    for i in range(pg.size):
        for j in range(pg.size):
            bits += str(pg.grid[i][j])

    #calculate hash of the bits string
    hashed_text = hashlib.sha512(bits.encode('utf-8')).hexdigest()

    print(f"Hashed text: {hashed_text}")

CA_hash(input("Plain text: "))