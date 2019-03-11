#!/usr/bin/env python2
from mpi4py import MPI


def scatter(data, root=0):
    for i in range(size):
        payload = []
        if (rank == 0):
            comm.send(data[i], i)
        comm.recv(payload, 0)
        print 'Rank', rank, 'has data:', payload


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [(x + 1) ** x for x in range(size)]
    print 'we will be scattering:', data
else:
    data = None

    scatter(data, root=0)
