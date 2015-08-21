# intogen-parser options
from intogen.generators import PROJECT_FILE_EXTENSION

MULTIPLE_TIMES = "This option can be indicated multiple times"

DRMAA_QUEUES = "The queue name(s) if you are using a DRMAA cluster. " + MULTIPLE_TIMES

JOBS_PARALLEL = "Allow N jobs (commands) to run simultaneously in parallel."

GROUP_BY = "Group by (combine) results according to an annotation present in the project annotations. This way " \
           "projects results with a same property, such as tumor_type or site, may be aggregated into a more general view. " \
           + MULTIPLE_TIMES

GROUP_BY_ALL = "Same as -g (group by) option, but for all projects"

OUTPUT_TIME_CHECK = "Do not check timestamp of input and output files in order to decide if a job needs to be rerun. Default False"

ANNTOTATION_FILES = "A tabular file (tsv) with annotations for each project. The first column should of the file should be " \
                    "the project ids meanwhile all following columns are annotations. The first line is the key or name of " \
                    "each annotation."

CONFIGURATION_FILES = "A tabular file (tsv) specifying the project-specific configuration. The first column should be the project ids " \
                      "and each column header the configuration key. All the conigurations taken from this file will overwrite the information" \
                      "available in the " + PROJECT_FILE_EXTENSION + " files. The default values are specified in conf/task.conf file. Sections " \
                      "are indicated by dots. " + MULTIPLE_TIMES

INPUT_FILES = "Either a " + PROJECT_FILE_EXTENSION + " file or a directory containing one or more " + PROJECT_FILE_EXTENSION + " files. Also any MAF " \
              "or VCF file (the default parameters will be use). " + MULTIPLE_TIMES
