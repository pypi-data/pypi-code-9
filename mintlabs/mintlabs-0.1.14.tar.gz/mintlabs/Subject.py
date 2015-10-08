import logging
from datetime import datetime

class Subject:
    """
    Subject class, providing an interface to interact with the subjects
    stored inside a Mint Labs project.

    :param project: an instantiated Project
    :type project: Project
    """

    def __init__(self, subject_name):
        assert subject_name != ""
        self._name = subject_name
        # project to which this subject belongs (instance of Project)
        # by default it's empty
        self.project = None
        # the subject has no id, as it doens't belong to a project yet
        self.subject_id = None

    @property
    def id(self):
        return self.subject_id

    @property
    def name(self):
        """
        The display name of the subject instanciated.

        :return: The name of the subject
        :rtype: String
        """
        return self._name

    @name.setter
    def name(self, new_subject_name):
        """
        Modify the subject name.

        :param subject_name: new name for the subject.

        :type subject_name: String

        :return: True if the modification was successful, False otherwise.
        :rtype: Bool
        """

        metadata = self._get_parameters()

        post_data = {
                     'patient_id': int(metadata['_id']),
                     'secret_name': new_subject_name,
                     'tags': metadata['tags'] or ""
                    }
        for item in filter(lambda x: x.startswith('md_'), metadata):
            item_newname = item.replace('md_', 'last_vals.')
            post_data[item_newname] = metadata[item] or ""

        answer = self.project._account.send_request(
                                           "patient_manager/upsert_patient",
                                           req_parameters=post_data)

        if not answer.get("success", False):
            logging.error("Could not edit subject name: {}".format(
                                                            answer["error"]))
            return False
        else:
            logging.info("Name updated succesfully: {} is now {}".format(
                                self.name, new_subject_name))
            self._name = new_subject_name
            return True

    @property
    def all_data(self):
        """
        All the data in the platform about the instanciated subject. Including
        uploaded files, analysis etc ...

        :return: All the data
        :rtype: Dict[String] -> x
        """
        response = self.project._account.send_request(
                        "patient_manager/get_patient_profile_data",
                        req_parameters={"patient_id": self.subject_id})
        return response["data"]

    @property
    def parameters(self):
        """
        Retrieve all of the the users metadata.

        :return: dictionary of {'parameter_name': 'value'} for the current user.
        :rtype: Dict[String] -> x
        """
        return self.all_data["metadata"]

    @parameters.setter
    def parameters(self, params_dict):
        """
        Set the value of one or more parameters for the current subject.

        :param params_dict: a dictionary with the names of the parameters to
                            set (param_id), and the corresponding values: {'param_id': 'value'}

        :type params_dict: Dict[String] -> Value

        :return: True if the request was successful, False otherwise.
        :rtype: Bool
        """

        data = self.all_data
        metadata = data["metadata"]

        post_data = {
                     "patient_id": self.subject_id,
                     "secret_name": self.name,
                     "tags": data["tags"] or ""
                    }
        # fill dict with current values
        for item in metadata:
            item_newname = "last_vals." + item
            post_data[item_newname] = metadata[item] or ""

        # update values
        for param_id, param_value in params_dict.items():
            post_data['last_vals.' + param_id] = param_value

        # fix dates
        # dates are retrieved as: date -> { '$date': 'timestamp' }, but must
        # be sent as date -> 'day.month.year'
        for param_id, param_value in post_data.items():
            if type(param_value) == dict and '$date' in param_value:
                # accept timestamp in milliseconds...
                try:
                    timestamp = int(param_value['$date'])
                    readable_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
                # but also in seconds
                except ValueError:
                    timestamp = int(str(param_value['$date'])[:-3])
                    readable_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
                post_data[param_id] = readable_date

        answer = self.project._account.send_request(
                                           "patient_manager/upsert_patient",
                                           req_parameters=post_data)

        if not answer.get("success", False):
            logging.error("Could not edit subject parameters: {}".format(
                                                            answer["error"]))
            return False
        else:
            logging.info("Parameters updated succesfully")
            return True

    @property
    def input_containers(self):
        """
        Retrieves a list of conatiners with the reference to the data uploaded
        for that user.

        :return: List of dictionaries with the conatiners info.
        :rtype: List(Dict)
        """
        all_containers = self.project.list_input_containers(limit=10000000)
        result = [a for a in all_containers if
                                       a["patient_secret_name"] == self._name]
        for r in result:
            del r['patient_secret_name']
        return result

    @property
    def analysis(self):
        """
        Retrieve all analysis data.

        :return: List of dictionaries with the data of each analysis performed.
        :rtype: List
        """
        all_analysis = self.project.list_analysis(limit=10000000)
        return [a for a in all_analysis if
                                       a["patient_secret_name"] == self._name]

    def upload_mri(self, path):
        """
        Upload mri data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self.project.upload_mri(path, self.name)

    def upload_gametection(self, path):
        """
        Upload gametection data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self.project.upload_gametection(path, self.name)

    def upload_result(self, path):
        """
        Upload result data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self.project.upload_result(path, self.name)

    def start_analysis(self, script_name, in_container_id, analysis_name=None,
                       analysis_description=None):
        """
        Starts an analysis on a subject.

        :param script_name: name of the script to be run. One of: 'volumetry',
                            'parkinson_gametection', 'morphology',
                            'morphology_new', '3d_wires', 'dti_fa_files',
                            '2d_wires' or 'morphology_infant'.
        :type script_name: String

        :param in_container_id: The id of the container to get the data from.
        :type in_container_id: Int

        :param analysis_name: name of the analysis (optional)
        :type analysis_name: String

        :param analysis_description: description of the analysis (optional)
        :type analysis_description: String

        :return: True if correctly started, False otherwise.
        :rtype: Bool
        """

        post_data = {
            "script_name": script_name,
            "in_container_id": in_container_id
        }
        # name and description are optional
        if analysis_name:
            post_data["name"] = analysis_name
        if analysis_description:
            post_data["description"] = analysis_description
        response = self.project._account.send_request(
                     "project_manager/project_registration",
                     req_parameters=post_data)

        if not response.get("success", False):
            logging.error("Unable to start the analysis.")
            return False
        if "has_to_ask" in response:
            files = response["files"]
            files_T1 = [f for f in files if f["metadata"]["modality"] == "T1"]
            # sort files by size (sort in python > 2.2 is stable)
            files_T1 = sorted(files_T1, key=lambda f: f["size"], reverse=True)
            file_ = files_T1[0]
            modality = file_["metadata"]["modality"]
            filename = file_["name"]
            post_data["c_files"] = "{};{}".format(modality, filename)
            response = self.project._account.send_request(
                        "project_manager/project_registration",
                        req_parameters=post_data)
            if not response.get("success", False):
                logging.error("Unable to start the analysis.")
                return False
            else:
                return True
