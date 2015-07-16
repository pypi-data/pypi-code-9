from spittalbase import SpittalBase
import json
import logging

logger = logging.getLogger('spittalpond')

class SpittalRun(SpittalBase):
    """ Handles everything related to running the data processs

    This is where all of the data and .csv files are created.
    """

    def create_cdf(self, name, benchmark_id, exposure_instance_id):
        """ Creates the CDF Django object.

        Args:
            name (str): A user-friendly name.
            benchmark_id (int): the id returned from create_benchmark().
            exposure_instance_id (int): id returned from create_exposure_instance().

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/createCDF/" +
            name + "/" +
            benchmark_id + "/" +
            exposure_instance_id + "/"
        )
        return response

    def create_cdf_samples(self, name, cdf_id, number_of_samples,
                           random_number_table_instance):
        """ Create the CDF samples Django object.

        Args:
            name (str): A user-friendly name.
            cdf_id (int): id returned from create_cdf()
            number_of_samples(int): number of cdf samples to create.
            sample_type (int): UNKNOWN

        Returns:
            HttpResponse: server's response.
        """

        response = self.do_request(
            self.base_url +
            "/oasis/createCDFSamples/" +
            name + "/" +
            str(cdf_id) + "/" +
            str(number_of_samples) + "/" +
            str(random_number_table_instance) + "/"
        )
        return response

    def create_gul(self, name, cdf_samples_id, loss_threshhold=0):
        """ Creates the ground up loss.

        Args:
            name (str): A user-friendly name.
            cdf_samples_id (int): id returned from create_cdf_samples().
            loss_threshhold (int): UNKNOWN

        Returns:
            HttpResponse: server's response.
        """

        response = self.do_request(
            self.base_url +
            "/oasis/createGUL/" +
            name + "/" +
            str(cdf_samples_id) + "/" +
            str(loss_threshhold) + "/"
        )
        return response

    def create_pub_gul(self, name, gul_id, download_file_id):
        """ Create the publish ground up loss.

        Args:
            name (str): A user-friendly name.
            gul_id (int): id returned from create_gul().
            download_file_id: id returned from create_file_download().

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/createPubGUL/" +
            name + "/" +
            str(gul_id) + "/" +
            str(download_file_id) + "/"
        )
        return response

    def update_file_download(self, download_id, name, module_supplier_id, filename):
        """ Much like the create_file_download method but instead updates.

        Args:
            download_id (int): id returned from create_file_download.
            name (str): A user-friendly name.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict
            filename (str): name of the new file download.

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/updateFileDownload/" +
            str(download_id) + "/" +
            name + "/" +
            str(module_supplier_id) + "/" +
            filename + "/"
        )
        return response


    def create_random_number_instance(self, random_number_table_name,
                                      random_number_table_version_id,
                                      number_of_chunks,
                                      number_of_rows_per_chunk,
                                      number_of_pages,
                                      number_of_samples_per_page):
        """ Creates a random number table instance.

        Args:
            random_number_table_name (str): A user friendly name for the task.
            number_of_chunks (int, optional): Self descriptive.
            number_of_rows_per_chunk (int, optional):
            number_of_pages (int, optional):
            number_of_samples_per_page (int, optional):

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/createRandomNumberTableInstance/" +
            random_number_table_name + "/" +
            str(random_number_table_version_id) + "/" +
            str(number_of_chunks) + "/" +
            str(number_of_rows_per_chunk) + "/" +
            str(number_of_pages) + "/" +
            str(number_of_samples_per_page) + "/"
        )
        logger.debug(
            "createRandomNumberTableInstance respones: {resp}".format(
                resp=response.content
            )
        )
        return response

    def auto_create_random_numbers(self, random_number_table_name="rand_nums",
                                   number_of_chunks=10,
                                   number_of_rows_per_chunk=1000,
                                   number_of_pages=10,
                                   number_of_samples_per_page=20):
        """ Generate random numbers with the default Random Number Table Version.

        Much of the time we just want to run Oasis without worry about these
        "random" (computers can only generate pseudo-random numbers anyways)
        numbers.

        Use this method to quickly generate them for ease of use.

        Note to Users: At the time of R1.3 there is, by default, a random
        number table version with the ID of 2. This can be used to avoid
        having to upload a random number table and create the version
        manually.

        Args:
            random_number_table_name (str): A user friendly name for the task.
            number_of_chunks (int, optional): Self descriptive.
            number_of_rows_per_chunk (int, optional):
            number_of_pages (int, optional):
            number_of_samples_per_page (int, optional):

        Returns:
            None: Until we figure out something more contructive to return.
        """

        logger.info("Auto-creating random numbers.")

        # Check if we need to create the data_dict keys.
        for key in ["version_random", "instance_random"]:
            if not key in self.data_dict:
                self.data_dict[key] = {}
        # Below, 2 is the default version.
        # Setup the version in the data_dict accordingly.
        self.data_dict["version_random"]["taskId"] = 2

        # Setup the instance in the data_dict accordingly.
        instance_resp = self.create_random_number_instance(
            random_number_table_name,
            self.data_dict["version_random"]["taskId"],
            number_of_chunks,
            number_of_rows_per_chunk,
            number_of_pages,
            number_of_samples_per_page
        )
        self.data_dict["instance_random"]["taskId"] =\
            json.loads(instance_resp.content)['taskId']

        # Run both of the jobs in order.
        self.do_jobs(["version_random", "instance_random"])

        return None

    def create_gul_data(self, gul_name, benchmark_id, exposure_instance):
        """ Create the ground up loss data based on our exposure instance.

        Args:
            gul_name (str): the user friendly name of the gul to create
            benchmark_id (int): the id returned from create_benchmark().
            exposure_instance_id (int): id from create_exposure_instance().

        Returns:
            HttpResponse: server's response.
        """

        # Create the cdf Django kernel object.
        self.data_dict['kernel_cdf'] = {}
        resp = self.create_cdf(gul_name, benchmark_id, exposure_instance)
        logger.info('Create cdf response: ' + resp.content)

        self.data_dict['kernel_cdf']['taskId'] = json.loads(
            resp.content
        )['taskId']

        # Create the cdf_samples Django kernel object.
        self.data_dict['kernel_cdfsamples'] = {}
        resp = self.create_cdf_samples(
            gul_name,
            self.data_dict['kernel_cdf']['taskId'],
            10,
            self.data_dict['instance_random']['taskId']
        )
        logger.info('Create cdf_samples response: ' + resp.content)

        self.data_dict['kernel_cdfsamples']['taskId'] = json.loads(
            resp.content
        )['taskId']

        # Create the GUL Django kernel object.
        self.data_dict['kernel_gul'] = {}
        resp = self.create_gul(
            gul_name,
            self.data_dict['kernel_cdfsamples']['taskId'],
        )
        logger.info('Create kernel gul response: ' + resp.content)

        self.data_dict['kernel_gul']['taskId'] = json.loads(
            resp.content
        )['taskId']

        print("Created GUL data")

    def get_gul_data(self, gul_name, filename, module_supplier_id):
        """ Get the GUL data from the server.

        Args:
            gul_name (str): The user friendly name of the GUL to create
            filename (str): the name of file to create and download.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict

        Returns:
            HttpResponse: server's response.
            This response also contains all the data from the GUL creation.
        """

        # Create a new file download.
        self.data_dict['kernel_pubgul'] = {}
        download_id = self.create_file_download(
            filename,
            self.pub_user,
            module_supplier_id
        )
        logger.info(
            'Create kernel GUL file download response, ' + str(download_id)
        )
        self.data_dict['kernel_pubgul']['download_id'] = download_id

        # Create the publish GUL.
        resp = self.create_pub_gul(
            gul_name,
            self.data_dict['kernel_gul']['taskId'],
            self.data_dict['kernel_pubgul']['download_id']
        )
        logger.info('Create kernel publish GUL response , ' + resp.content)

        self.data_dict['kernel_pubgul']['taskId'] = json.loads(
            resp.content
        )['taskId']

        # Update the file download.
        self.update_file_download(
            self.data_dict['kernel_pubgul']['download_id'],
            filename,
            module_supplier_id,
            filename,
        )
        logger.info("update kernel publish GUL download, " + resp.content)

        self.data_dict['kernel_pubgul']['download_id_2'] = json.loads(
            resp.content
        )['taskId']

        jobs_to_do = [
            'kernel_cdf',
            'kernel_cdfsamples',
            'kernel_gul',
            'kernel_pubgul',
        ]
        self.do_jobs(jobs_to_do, status_check_interval=1)
        # This has to be done like at the very last!!
        # self.load_models()

        # A makeshift save of the data.
        response1 = self.do_request(
            self.base_url +
            "/oasis/saveFilePubGUL/" +
            str(1) + "/" +
            str(self.data_dict['kernel_pubgul']['taskId']) + "/"
        )

        logger.info("Save pub GUL response " + response1.content)

        # Do the pubgul task again.
        self.do_jobs(["kernel_pubgul"], status_check_interval=1)

        # Actually download the file.
        resp = self.download_file(
            self.data_dict['kernel_pubgul']['download_id']
        )
        logger.info("Download Herlp gul response " + resp.content)

        return resp
