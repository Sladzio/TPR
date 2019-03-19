import random
from mpi4py import MPI
import sys


def compute_points_in_circle(iterations):
    result = 0
    for i in range(iterations):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x ** 2 + y ** 2 <= 1:
            result += 1
    return result


def compute_pi_parralel(iterations):
    comm.barrier()
    start = MPI.Wtime()
    if scalable:
        points_in_circle = compute_points_in_circle(iterations)
    else:
        points_in_circle = compute_points_in_circle(iterations / worker_count)
    results = comm.gather(points_in_circle, root=0)
    if is_leader_worker:
        end = MPI.Wtime()
        duration_in_sec = end - start
        gathered_points_in_circle = sum(results)
        all_points_count = iterations
        if scalable:
            all_points_count *= worker_count
        pi = gathered_points_in_circle * 4.0 / all_points_count

        print(str(iterations) + "," + str(pi) + "," + str(worker_count) + "," + str(duration_in_sec))


comm = MPI.COMM_WORLD
rank = comm.rank()
is_leader_worker = rank is 0
argv = sys.argv[1:]
iter_count = int(argv[0])
scalable = str(argv[1]) is 'scalable'

worker_count = comm.Get_size()

compute_pi_parralel(iter_count)
