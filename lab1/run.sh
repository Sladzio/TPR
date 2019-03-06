#!/usr/bin/env bash

set -x

mpiexec  -machinefile ./single-node -np 2 ./main.py shared_mem.json
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec  -machinefile ./single-node -np 2 ./main.py network.json
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec  -machinefile ./two-nodes-same-machine -np 2 ./main.py same_machine.json
MPIR_CVAR_CH3_NOLOCAL=1 mpiexec  -machinefile ./two-nodes-different-machines -np 2 ./main.py diff_machines.json