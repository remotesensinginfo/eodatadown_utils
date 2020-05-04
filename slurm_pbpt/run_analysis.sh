#!/usr/bin/env bash

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_process_cmds.py

sh ./gen_exe_hpccmds.sh

