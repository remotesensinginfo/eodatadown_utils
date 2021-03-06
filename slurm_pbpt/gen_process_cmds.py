from pbprocesstools.pbpt_process import PBPTGenProcessToolCmds
import os.path
import logging

logger = logging.getLogger(__name__)

class CreateEODataDownCmds(PBPTGenProcessToolCmds):

    def gen_command_info(self, **kwargs):
        import eodatadown.eodatadownrun
        scns = eodatadown.eodatadownrun.get_scenes_need_processing_date_order(kwargs['config_file'], kwargs['sensors'])
        for scn in scns:
            c_dict = dict()
            c_dict['scn_info'] = scn
            self.params.append(c_dict)

    def run_gen_commands(self):
        self.gen_command_info(config_file='/scratch/a.pfb/gmw_monitoring/scripts/eodd_config_east_africa/EODataDownConfig_psql.json',
                              sensors=['LandsatGOOG', 'Sentinel2GOOG', 'Sentinel1ASF'])
        self.write_cmd_files()
        self.create_slurm_sub_sh(jobname='eodd_gmw_process',
                                 mem_per_core_mb=8192,
                                 account_name='scw1376',
                                 log_dirs='/scratch/a.pfb/gmw_monitoring/logs',
                                 prepend='singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif ')

    def run_check_outputs(self):
        process_tools_mod = 'exe_scn_processing'
        process_tools_cls = 'ProcessEODDScn'
        time_sample_str = self.generate_readable_timestamp_str()
        out_err_file = 'processing_errs_{}.txt'.format(time_sample_str)
        out_non_comp_file = 'non_complete_errs_{}.txt'.format(time_sample_str)
        self.check_job_outputs(process_tools_mod, process_tools_cls, out_err_file, out_non_comp_file)


if __name__ == "__main__":
    py_script = os.path.abspath("exe_scn_processing.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    create_tools = CreateEODataDownCmds(cmd=script_cmd, cmds_sh_file="./eodd_cmds_lst.sh",
                                        out_cmds_base="./ind_cmds/cmd_eodd_file")
    create_tools.parse_cmds()