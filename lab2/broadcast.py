#!/usr/bin/env python2
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank

if rank == 0:
    data = "broadcasting message"
else:
    data = None

data = comm.bcast(data, root=0)
print 'rank',rank,data
