import json
from spittalbase import SpittalBase
import logging

logger = logging.getLogger('spittalpond')

class SpittalModel(SpittalBase):
    """ Handles everything model related. """

    def create_version(self, version_type, version_name, module_supplier_id,
                       upload_id, model_key):
        """ Creates a generic version.

        With `generic` currently meaning the vuln and hazfp versions, as the
        exposure version is handled differently and needs different
        parameters.

        Args:
            version_type (str): defines the type of version to upload.
            version_name (str): A user-friendly name for this version.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict
            upload_id (int): the id returned from create_file_upload().
            model_key (string): The model key.

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/create" + self.types[version_type] + "/" +
            version_name + "/" +
            str(module_supplier_id) + "/" +
            str(upload_id) + "/" +
            model_key + "/"
        )
        return response

    def create_exposure_version(self, version_type, version_name,
                                module_supplier_id, exposure_upload_id,
                                correlations_upload_id):
        """ TODO: Document this function. Should be similar to above. """
        response = self.do_request(
            self.base_url +
            "/oasis/create" + self.types[version_type] + "/" +
            version_name + "/" +
            str(module_supplier_id) + "/" +
            str(exposure_upload_id) + "/" +
            str(correlations_upload_id) + "/"
        )
        return response

    def create_model_structures(self):
        """ Creates supporting module structure from the data_dict.

        Args:
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict
        """
        ##### Create the Model Structures ####
        logger.info('Creating the model structures.')
        for type_name, type_ in self.data_dict.iteritems():
            splitname = type_name.replace(".", "_").split("_")

            # For dictionary types.
            if splitname[0] == 'dict':
                creation_response = self.create_dict(
                    type_name,
                    type_['upload_id'],
                    type_['download_id'],
                    self.pub_user,
                    type_['module_supplier_id'],
                )
                logger.info(
                    'Create dict {dict_} response: '.format(dict_=type_name) +
                    str(creation_response.content)
                )

            # For version types.
            elif splitname[0] == 'version':
                # Vuln and Haz version are handled the same.
                if splitname[1] in ['vuln', 'hazfp']:
                    creation_response = self.create_version(
                        type_name,
                        type_name,
                        type_['module_supplier_id'],
                        type_['upload_id'],
                        # TODO FIXME: Get rid of this hard coding.
                        "ModelKey",
                    )

                # Exposure is a special version.
                elif splitname[1] == 'exposure':
                    creation_response = self.create_exposure_version(
                        type_name,
                        type_name,
                        type_['module_supplier_id'],
                        type_['upload_id'],
                        self.data_dict['version_correlation']['upload_id'],
                    )
                logger.info(
                    'Create version {version} response: '
                    .format(version=type_name) +
                    str(creation_response.content)
                )
            type_['taskId'] = json.loads(
                creation_response.content
            )['taskId']


        print('Finished creating model strutures.')

    # TODO: Finish creating this method.
    def get_model(self, model_name):
        """ Return a previously uploaded model from the database.

        Args:
            model_name -- The name that the model was uploaded with.
        """
        pass

    def model_do_jobs(self):
        self.do_jobs(
            [
                'dict_areaperil',
                'dict_event',
                'dict_vuln',
                'dict_damagebin',
                'dict_hazardintensitybin',
                'version_hazfp',
                'version_vuln'
            ]
        )


    def select_manually(self):
        """ Alow user to select the necassary parts of the model manually.

        This is an alternative way of populting the data_dict (as opposed to
        use the config interface).

        """
        types_to_ask_for = [
            "dict_areaperil",
            "dict_event",
            "dict_vuln",
            "dict_damagebin",
            "dict_hazardintensitybin",
            "version_vuln",
            "version_hazfp"
        ]
        for type_name in types_to_ask_for:
            type_id = self.select_type(type_name)
            # TODO: Probably not the best to reset the dictionary here... But
            # works for now.
            self.data_dict[type_name] = {}
            self.data_dict[type_name]['taskId'] = type_id

        print self.data_dict
