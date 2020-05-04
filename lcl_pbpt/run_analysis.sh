#!/usr/bin/env bash

python gen_process_cmds.py --gen

parallel -j 4 < eodd_cmds_lst.sh

python gen_process_cmds.py --check
