import logging


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
        self._project = None
        # the subject has no id, as it doens't belong to a project yet
        self._id = None

    @property
    def name(self):
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

        answer = self._project._account.send_request(
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
    def subject_id(self):
        return self._id

    @subject_id.setter
    def subject_id(self, subject_id):
        self._id = subject_id

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, project):
        """
        Set the project to which this user belongs.

        :param project: project to which this user belongs.
        :type project: Project
        """

        self._project = project

    @property
    def all_data(self):
        response = self._project._account.send_request(
                        "patient_manager/get_patient_profile_data",
                        req_parameters={"patient_id": self._id})
        return response["data"]

    @property
    def parameters(self):
        """
        Retrieve all of the the user metadata.

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
                     "patient_id": self._id,
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
        all_containers = self._project.list_input_containers(limit=10000000)
        result = [a for a in all_containers if a["patient_secret_name"] == self._name]
        for r in result:
            del r['patient_secret_name']
        return result

    @property
    def analysis(self):
        all_analysis = self._project.list_analysis(limit=10000000)
        return [a for a in all_analysis if a["patient_secret_name"] == self._name]

    def upload_mri(self, path):
        """
        Upload mri data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self._project.upload_mri(path, self.name)

    def upload_gametection(self, path):
        """
        Upload gametection data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self._project.upload_gametection(path, self.name)

    def upload_result(self, path):
        """
        Upload result data to this subject.

        :param path: path to a zip containing the data.
        :type path: String

        :return: True if correctly uploaded, False otherwise.
        :rtype: Bool
        """

        return self._project.upload_result(path, self.name)

    def start_analysis(self, script_name, in_container_id):
        post_data = {"name": self._name, "script_name": script_name, "in_container_id": in_container_id}
        response = self._project._account.send_request("project_manager/project_registration",
                                                       req_parameters=post_data)

        if response.get("success", False):
            logging.info("Successfully started analysis.")
            return True, response["success"]
        else:
            logging.error("Unable to start the analysis.")
            return False