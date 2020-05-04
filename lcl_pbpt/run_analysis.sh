#!/usr/bin/env bash

python gen_process_cmds.py

parallel -j 4 < eodd_cmds_lst.sh

