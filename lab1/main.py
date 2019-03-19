#!/usr/bin/env python2
from mpi4py import MPI
import numpy as np
import json
import sys


def run():
    if len(sys.argv) < 2:
        print ("Provide output json file name")
    test_bandwidth_and_latency("send", lambda x: comm.send(x, dest=1))
    test_bandwidth_and_latency("ssend", lambda x: comm.ssend(x, dest=1))
    if rank == 0:
        print_to_json()


def print_to_json():
    with open(sys.argv[1], 'w') as fp:
        json.dump(result, fp)


def get_payload_lengths():
    x = 50
    while x < max_payload_size:
        yield int(x)
        x *= 1.05


def test_bandwidth_and_latency(comm_type, send):
    test_result = {"latency": [], "bandwidth": [], "payload_size": []}
    for payload_size in get_payload_lengths():
        payload = np.random.bytes(payload_size)
        comm.Barrier()
        t1 = MPI.Wtime()
        for _ in range(iterations):
            if rank == 0:
                send(payload)
            elif rank == 1:
                recv()
        t2 = MPI.Wtime()

        latency = convert_to_milliseconds((t2 - t1) / iterations)
        test_result["latency"].append(latency)
        test_result["payload_size"].append(payload_size)
        test_result["bandwidth"].append(MBIT_FACTOR * (payload_size * iterations) / (t2 - t1))

    result[comm_type] = test_result


def convert_to_milliseconds(seconds):
    return seconds * 1000


def recv():
    comm.recv(source=0)


MBIT_FACTOR = 8.0 / (1024 * 1024)
result = {}
max_payload_size = 10 ** 6
iterations = 100
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
run()
