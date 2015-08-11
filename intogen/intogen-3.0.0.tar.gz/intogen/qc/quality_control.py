import argparse
import fnmatch
from intogen.generators import PROJECTS_DIR
import os
import logging

ERROR = "ERROR"

WARNING = "WARNING"

qc_identifier = "#QUALITY_CONTROL#"

class QualityControl(object):

    def report(self, entity: str, label: str, value, **kwargs):

        additional = {}
        for key, content in kwargs.items():
            additional[key] = content

        out_string = "{} {}\t{}\t{}\t{}".format(qc_identifier, entity, value, label, additional.__repr__())
        logging.info(out_string)

def scan_project_log(project, task, log_file, entities, tasks, match, verbose):
    has_qc = False
    warn_and_err = len(entities) == 0 or WARNING in entities or ERROR in entities

    for line in log_file:
        if qc_identifier in line:
            time_string, qc_string = line.rstrip().split(qc_identifier)
            time_string = time_string.rstrip(" INFO:")
            entity, value, label, additional = qc_string.split("\t")
            additional = eval(additional)

            if len(entities) > 0 and entity not in entities:
                continue
            if len(tasks) > 0 and task not in tasks:
                continue

            if not has_qc:
                has_qc = True
                if verbose:
                    print(match)
            print("\t".join([time_string, project, task, entity, value, label]))
        elif warn_and_err:
            if not has_qc:
                has_qc = True
                if verbose:
                    print(match)
            if WARNING in line:
                time_string, message = line.rstrip().split(WARNING)
                print("\t".join([time_string, project, task, WARNING, message]))
            elif ERROR in line:
                time_string, message = line.rstrip().split(WARNING)
                print("\t".join([time_string, project, task, ERROR, message]))




def scan_logs(output_dir, entities, tasks, projects, verbose):
    matches = []

    projects = [p.lower() for p in projects]


    for root, dirnames, filenames in os.walk(output_dir):
      for filename in fnmatch.filter(filenames, '*.log'):
          matches.append(os.path.join(root, filename))

    for match in matches:
        dirs = match.split("/")
        if PROJECTS_DIR in dirs:
            project_id = dirs[dirs.index(PROJECTS_DIR) + 1]

            project_id_low = project_id.lower()
            if len(projects) == 0 or project_id_low in projects:
                task = dirs[-1].split("." + project_id.lower())[0]
                scan_project_log(project_id, task, open(match), entities, tasks, match, verbose)
        else:
            if(verbose):
                print("not a project log: {}".format(match))
            continue

def cmdline():

    from intogen.constants.qc import ENTITY_GENE, ENTITY_VARIANTS, ENTITY_TRANSCRIPTS, ENTITY_SAMPLE

    ENTITIES = "|".join([ENTITY_GENE, ENTITY_SAMPLE, ENTITY_VARIANTS, ENTITY_TRANSCRIPTS] + [WARNING, ERROR])

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir')
    parser.add_argument("-e", "--entity", dest="entities", default=[], action="append",
                        help="Only a specific entity. Must be one in: " + ENTITIES)
    parser.add_argument("-t", "--task", dest="tasks", default=[], action="append",
                        help="Only query for quality control in specific tasks of the pipeline")
    parser.add_argument("-p", "--project", dest="projects", default=[], action="append",
                        help="Only query for quality control in specific projects")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
    options = parser.parse_args()

    # Run the command line
    scan_logs(
        options.output_dir,
        options.entities,
        options.tasks,
        options.projects,
        options.verbose
    )

if __name__ == "__main__":
    cmdline()

