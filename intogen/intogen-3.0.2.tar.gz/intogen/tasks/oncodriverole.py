import argparse
import os
from intogen import utils
from intogen.tasks.intogen_task import IntogenTask
import pandas

CLUSTERS_MISS_VS_PAM = 'MUTS_clusters_miss_VS_pam'

TRUNC_MUTFREQ = 'MUTS_trunc_mutfreq'


class OncodriveRoleTask(IntogenTask):

    @staticmethod
    def get_configuration_definitions():
        return {
            #'oncodriverole_path': 'dir'
        }



    def run(self, input_file, output_file, samples_threshold=None):

        # Load input file
        data_in = pandas.read_csv(input_file, sep='\t')
        exec_config = self.get_exec_config()

        temp_output_folder = utils.get_temp_folder()

        oncodriverole_path = exec_config['oncodriverole_path']

        rinput_file = os.path.join(temp_output_folder, 'features.tsv')
        rinput_file = os.path.join(oncodriverole_path, 'example-input')

        routput_file = os.path.join(temp_output_folder, 'classification')
        routput_file = 'output-test'

        classifier_file = "nonredundant.nocna.OncodriveROLE.RData"
        rscript = '''library("randomForest")
            testset <- read.delim("{}")
            rownames(testset) <- testset$SYMBOL
            load("{}")
            result <- oncodriveROLE.classify(testset)
            result$GENE <- testset$GENE
            write.table(result,file="{}", sep="\t",quote=F,col.names=T,row.names=T)'''.format(rinput_file,
                                                                                          classifier_file,
                                                                                          routput_file)
        #r=robjects.r
        r=''
        r(rscript)
        classified_df = pandas.read_csv(routput_file, sep='\t')
        #TODO: RENAME columns
        classified_df.rename(columns= {TRUNC_MUTFREQ: TRUNC_MUTFREQ.upper(),
                                       CLUSTERS_MISS_VS_PAM: CLUSTERS_MISS_VS_PAM.upper()})

        # Store output file
        classified_df.to_csv(output_file, sep='\t', na_rep='')


def cmdline():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file')
    parser.add_argument('-o', dest='output_file')
    parser.add_argument('--oncodriveclust', dest='oncodriveclust')
    parser.add_argument('--recurrences', dest='recurrences')
    parser.add_argument('--samples_threshold', dest='samples_threshold')
    options = parser.parse_args()

    # Run the command line
    task = OncodriveRoleTask()
    task.run(
        options.input_file,
        options.output_file,
        samples_threshold=options.samples_threshold
    )


if __name__ == "__main__":
    cmdline()
