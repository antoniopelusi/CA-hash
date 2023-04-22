# CA-hash
**Hash** function based on the irreversible **C**ellular **A**utomata *Game of Life*

>Entropy not tested

## Steps
- generate the key using *SHA-512* on the plain text
- create the random grid using the key as a seed
- execute the non-reversible Game of Life iterations on the grid
- generate the hash of the bits of the grid using *SHA-512*
