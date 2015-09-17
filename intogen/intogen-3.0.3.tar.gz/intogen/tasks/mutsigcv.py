import argparse
import subprocess
import time
import logging
from intogen.mutsig.mutsigfiles import MutsigMAF, MutsigResult, MutsigFileUtils
import socket
from intogen.tasks.intogen_task import IntogenTask
from intogen import utils
import os


class MutsigCVTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {
            "mutsig_enabled": "boolean(default=False)",
            "matlab_mcr": "dir",
            "mutsig_path": "dir",
            "mutsig_hg19_path": "dir",
            "mutsig_covariates": "file",
            "mutsig_exome_coverage": "file",
            "mutsig_vep_dictionary": "file",
            "mutsig_sym2gene_file": "file",
            "consequence_rankings": "file",
            "temporal_dir": "string"
        }


    def run(self, input_file, output_file, gene_filter_path=None, use_fast_version=True):
        '''
        Reading a text file containing variants containing the necessary data columns   defined in the MutsigMAF class.
        MutsigCV ouput go to a temp folder and just the results are being maintained.
        The variants file maf-like formatted is also included in the output folder.
        '''
        start_time = time.time()

        exec_config = self.get_exec_config()

        logging.info("Running task on {}".format(socket.gethostname()))

        '''
        Variables/ constants declaration
        '''
        sep = ''.join(['='] * 10)
        matlab_mcr = exec_config["matlab_mcr"]

        mutsig_main_folder = exec_config["mutsig_path"]
        hg_folder = exec_config["mutsig_hg19_path"]
        mutsig_covars_file = exec_config["mutsig_covariates"]
        mutsig_fullcoverage_file = exec_config["mutsig_exome_coverage"]
        mutsig_muttype_dict_file = exec_config["mutsig_vep_dictionary"]

        temp_output_folder = utils.get_temp_folder()
        temp_output_basename = os.path.join(temp_output_folder, 'MutSigCV_output')

        '''
        1) reformat the variants file
        '''
        analysis_name = os.path.basename(input_file)
        sym2gene_file = exec_config["mutsig_sym2gene_file"]
        mutsigMAF = MutsigMAF(input_file, temp_output_folder,
                              exec_config["consequence_rankings"],
                              sym2gene_file,
                              mutsig_muttype_dict_file,
                              sample_prefix=analysis_name)
        mutsigMAF_file = mutsigMAF.get_filename()
        logging.info(mutsigMAF_file)

        if not mutsigMAF.enough_muts:
            logging.warning("Not enough mutations to run MutSigCV. {}".format(mutsigMAF.get_effect_counts()))
            self.finish_up(mutsigMAF, output_file, temp_output_basename, temp_output_folder, gene_filter_path)
            return



        # Create a coverage file for this project
        coverage_file = os.path.join(temp_output_folder, 'coverage.txt')

        if use_fast_version:

            # FAST version (STEP 1)
            # this is our way to run MutsigCV in two steps first only the preproccess
            # and then a second step the Mutsig run phase. We have tested that the
            # results are the same for MutsigCV v1.4

            # We will preprocess the full coverage to only load the genes and effects
            # that we need.
            mutsigMAF.collapse_coverage(mutsig_fullcoverage_file, coverage_file)

            # This is an empty file to force mutsigCV to fail after preprocess
            covariate_file = utils.get_temp_file()[1]

        else:

            # SLOW version
            # this is the normal way to run MutsigCV, but it's incredibly slow parsing
            # a big coverage file (and spends lots of memory)
            coverage_file = mutsig_fullcoverage_file
            covariate_file = mutsig_covars_file

        cmd = ' '.join(['sh', os.path.join(mutsig_main_folder, 'run_MutSigCV.sh'), matlab_mcr,
                        mutsigMAF_file, coverage_file, covariate_file, temp_output_basename,
                        mutsig_muttype_dict_file, hg_folder])

        logging.info('{0}\nExecuting cmd: \n{1}\n{2}'.format(sep, cmd, sep))

        retcode = subprocess.call(cmd, shell=True)

        if retcode != 0:
            if use_fast_version:
                # If we are running the fast version we force MutSigCV to give an error after the
                # preprocess. Now we will expand the collapsed coverage file and run it again
                MutsigFileUtils.expand_coverage(
                    mutsig_fullcoverage_file,
                    temp_output_basename + ".categs.txt",
                    temp_output_basename + ".coverage.txt",
                    coverage_file
                )

                # The mutations file with the calculated categs
                mutations_file = temp_output_basename + ".mutations.txt"
                # Remove no-category genes "---" and check if enough mutations - else abort
                enough_muts, effect_counts = MutsigFileUtils.curate_mutations(mutations_file)

                if enough_muts:

                    # Now we use the correct covariate file because we don't want mutsig to fail
                    covariate_file = mutsig_covars_file

                    # Run again without preprocess
                    cmd = ' '.join(['sh', os.path.join(mutsig_main_folder, 'run_MutSigCV.sh'), matlab_mcr,
                                    mutations_file, coverage_file, covariate_file, temp_output_basename,
                                    mutsig_muttype_dict_file, hg_folder, '0'])

                    logging.debug(cmd)
                    retcode = subprocess.call(cmd, shell=True)
                    if retcode != 0:
                        logging.error("Running MutSigCV '{0}'".format(cmd))
                        exit(1)

                else:
                    logging.warning("Not enough mutations to run MutSigCV. {}".format(effect_counts))
            else:
                logging.error("Running MutSigCV '{0}'".format(cmd))
                exit(1)

        '''
        3) re-convert & clean-up
        '''

        self.finish_up(mutsigMAF, output_file, temp_output_basename, temp_output_folder, gene_filter_path)


    def finish_up(self, mutsigMAF, output_file, temp_output_basename, temp_output_folder, gene_filter_path):
        temp_output_results_file = temp_output_basename + ".sig_genes.txt"
        results = MutsigResult(mutsigMAF, temp_output_results_file, gene_filter_path)
        results.convert_and_write(output_file)
        subprocess.call(" ".join(["mv", temp_output_folder, os.path.join(os.path.dirname(output_file), "temp")]),
                        shell=True)

def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--gene_filter_path', dest='gene_filter_path', default=None)
    parser.add_argument('--cores', dest='cores', default=2, type=int)
    options = parser.parse_args()

    # Run the command line
    task = MutsigCVTask()
    task.run(
        options.input_file,
        options.output_file,
        options.gene_filter_path
    )


if __name__ == "__main__":
    cmdline()