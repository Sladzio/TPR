#!/usr/bin/env python2
from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

a_size = 3
recvdata = numpy.zeros(a_size, dtype=numpy.int)
senddata = (rank + 1) * numpy.arange(a_size, dtype=numpy.int)
comm.Reduce(senddata, recvdata, root=0, op=MPI.SUM)
print 'on task', rank, 'after Reduce:    data = ', recvdata
