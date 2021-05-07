#### Hogwild!
- Feng Niu, Benjamin Recht, Christopher Re and Stephen J. Wright

### Basics
- Communication between processors is quadratic, so if you are running a algorithm that requires lots of processors this can lead to huge slowdowns

- The key idea is to remove the locks mechanism that enabled correct communication between processors while performing SGD

- To get theoretical guarantees it sounds like the dimensionality of the problem (weight vector?) needs to be way bigger than the number of processors.

- The basic idea I believe is that the processors have shared memory and they randomly choose an index and update that index with SGD without any attention to the other product processors no locking or communication

- Works better on sparse data

### Other notes

- Nice test of time talk on (YouTube)[https://www.youtube.com/watch?v=c5T7600RLPc] for NeurlIPS 2020

- It shows up on the Eisner paper on Macaronic texts that uses a CRF

- JB asks: is this really better than batch SGD? I guess implication is that batch is easly to parallelize 

- Amdahl's law?