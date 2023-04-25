# CA-hash 🛡️
**Experimental hash function** based on the non-reversible **C**ellular **A**utomata [*Game of Life*](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Parameters
- **hash_length**: the length of the final hash
- **iter**: number of the Game of Life iterations applied to the initial grid
- **grid_size**: size of the grid used to apply Game of Life iterations
- **print_grid**: if *True*, print the initial grid and final grid to terminal

# Usage information
- this hash function do not use any external library apart from *numpy* for the generation of the random grid
- the entropy has not been tested
- since the Game of Life is non-reversible (there are multiple pre-configurations for every grid configuration)
- small **grid_size** value == less entropy == faster generation of the hash
- small **iter** value == less entropy == faster generation of the hash
- don't use small **iter** values, the inverse process of Game of Life could be calculated with a bruteforce attack
- don't use huge **iter** values, there could be recursions in the Game of Life grid

## Steps
- generate the key converting the input into a list of the input characters econded in *utf-8*
- create the random grid using the key as seed
- execute the non-reversible Game of Life iterations on the grid
- generate the hexadecimal hash of the linearized final grid joining the hexadecimal values of the bits and getting them randomly to increare entropy
