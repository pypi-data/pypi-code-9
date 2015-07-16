import requests
import json
import glob
import time
import os
import logging

# FIXME: Turning off SSL unverified warnings probably isn't the best idea.
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('spittalpond')

class SpittalBase():
    """ A base class that contains generic spittal functions

    Classes such as SpittalModel and SpittalExposure will import this one.
    """


    # TODO: Maybe have individual type definition for each sub class?
    # Each subclass only really needs to know about itself.
    types = {
        """ This dictionary defines Oasis "types" that we use internally.

        This creates a standard that is both easier to type and is not
        dependant on the Oasis API. Mainly these types are used as keys in the
        data_dict, but also the values should be used for creating URL API
        call strings.
        """

        # correlations is special, it's just a file, that's all!
        "version_correlation": None,
        "dict_areaperil": "AreaPerilDict",
        "dict_damagebin": "DamageBinDict",
        "dict_event": "EventDict",
        "dict_exposure": "ExposureDict",
        "dict_hazardintensitybin": "HazardIntensityBinDict",
        "dict_vuln": "VulnDict",
        "dict_random": "RandomNumberTable",
        "version_exposure": "ExposureVersion",
        "version_hazfp": "HazFPVersion",
        "version_vuln": "VulnVersion",
        "version_random": "RandomNumberTableVersion",
        "instance_exposure": "ExposureInstance",
        "instance_vuln": "VulnInstance",
        "instance_hazfp": "HazFPInstance",
        "instance_random": "RandomNumberTableInstance",
        "kernel_benchmark": "Benchmark",
        "kernel_cdf": "CDF",
        "kernel_cdfsamples": "CDFSamples",
        "kernel_gul": "GUL",
        "kernel_pubgul": "PubGUL",
    }

    def __init__(self, base_url, pub_user):
        """ Initiating instance.

        Args:
            base_url (str): server's domain name and/or port (without final slash).
            pub_usr (str): the public user used to name certain things.
        """
        self.base_url = base_url
        self.pub_user = pub_user
        self.is_logged_in = False
        self.cookies = None
        # Each instance with have it's own data_dict
        self.data_dict = {}

    def do_request(self, url, in_data=None, in_file_dict=None):
        """ Makes a post request.

        Also automatically passes self.cookies to the post request.
        This authenticates each request.

        Args:
            url (str): the url to make a post request to. Ensureu that you
                specify a schema i.e. http://, ftp:// etc...
            in_data (dict): optional, used if data needs to be passed.
            in_file_dict (dict): optional, passes file dict to server.

        Returns:
            HttpResponse: server's response
        """
        url_string=url
        logger.debug(
            "do_request request string: {string}".format(string=url_string)
        )
        response=requests.post(
            url_string,
            data=in_data,
            files=in_file_dict,
            cookies=self.cookies,  #For Authentication!
            verify=False
        )
        return response

    def do_login(self, password):
        """ Logs into Oasis Django mid-tier.

        Also, set self.cookies to the return session ID.
        This allows for future authentication.

        Args:
            password (str): server Djanger user password.
        """
        # Creating JSON string with authentication credentails.
        in_data = ('{{ "username":"{username}",'
                    '"password":"{password}" }}'
                    ).format(
                    username=self.pub_user,
                    password=password
        )

        url = self.base_url + "/oasis/login"
        response = self.do_request(url, in_data)
        json_response = json.loads(response.content)

        if json_response["success"] == False:
            print("Invalid user id or password")
        else:
            self.cookies = dict(sessionid=response.cookies['sessionid'])
            print("You are logged into Mid-tier")

        logger.info( 'Log in response ' + str(response.content))

    def create_file_upload(self, upload_filename,
                            pub_user, module_supplier_id):
        """ Creates a file upload object and returns the ID

        Args:
            upload_filename (str): what the filename will be on the server.
            pub_usr (str): the public user used to name certain things.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict

        Returns:
            int: file upload id.
        """
        up_response = self.do_request(
            self.base_url +
            "/oasis/createFileUpload/" +
            pub_user + "/" +
            upload_filename + "/" +
            str(module_supplier_id) + "/"
        )
        logger.debug("createFileUpload respons: {resp}".format(
            resp=up_response.content
        ))
        up_id = int(json.loads(up_response.content)['taskId'])
        return up_id

    def create_file_download(self, upload_filename,
                            pub_user, module_supplier_id):
        """ Creates a file download object and returns the ID

        Args:
            upload_filename (str): not to sure where this name is actually used.
            pub_usr (str): the public user used to name certain things.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict

        Returns:
            int: file download id
        """
        down_response = self.do_request(
            self.base_url +
            "/oasis/createFileDownload/" +
            pub_user + "/" +
            upload_filename + "/" +
            str(module_supplier_id) + "/"
        )
        logger.debug(
            "createFileDownload respons: {resp}".format(
                resp=down_response.content
            )
        )
        down_id = int(json.loads(down_response.content)['taskId'])
        return down_id

    def upload_file(self, local_absolute_filepath, upload_filename):
        """ Uploads a file to the server.

        Uploads a local file that is renamed on the server side to
        the upload_filename argument.

        Args:
            local_absolute_filepath (str): path to the file we need to upload.
            upload_filename (str): the name for the server-side file.

        Returns:
            HttpResponse: server's response.
        """
        url = self.base_url + "/oasis/doTaskUploadFileHelper/"

        with open(local_absolute_filepath) as f:
            in_file = f
            response = self.do_request(
                url,
                in_file_dict={upload_filename:in_file}
            )
            return response

    def download_file(self, download_id):
        response = self.do_request(
            self.base_url +
            "/oasis/doTaskDownloadFileHelper/" +
            str(download_id) + "/"
        )
        return response


    def create_timestamps(self):
        """ Create timestamp for destination files

        Returns:
            str: a timestamnp of the current time.
        """
        str_now = time.strftime("%Y%m%d_%H%M%S_", time.localtime())
        return str_now

    def check_status(self, job_id, config_id=1):
        """ Get the status of the respective job.

        Args:
            job_id (str): id of the job to check status of.
            config_id (int): UNKNOWN

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/statusAsync/" +
            str(config_id) + "/" +
            str(job_id) + "/"
        )
        return response

    def do_task(self, task_type, upload_id, sys_config=1):
        """ Creates a task on the job queue.

        Args:
            task_type (str): type of task to be added to the queue.
            upload_id (int): upload_id of the file to create task for.
            sys_config (int): defines where and how to load the data.

        Returns:
            HttpResponse: server's response.

        """
        response = self.do_request(
            self.base_url +
            "/oasis/doTask" + task_type + "/" +
            str(sys_config) + "/" +
            str(upload_id) + "/"
        )
        return response

    def create_dict(self, dict_type, upload_id, download_id,
                    pub_user, module_supplier_id):
        """ Creates a dict with the upload and download IDs.

        Args:
            dict_type (str): defines the type of dictionary to upload.
            upload_id (int): the id returned from create_file_upload().
            download_id (int): the id returned from create_file_download().
            pub_usr (str): the public user used to name certain things.
            module_supplier_id (int): id of the module that supplies the
                python and SQL code for this file.
                See /oasis/django/oasis/app/scripts/Dict

        Returns:
            HttpResponse: server's response.
        """
        response = self.do_request(
            self.base_url +
            "/oasis/create" + self.types[dict_type] + "/" +
            pub_user + "/" +
            str(module_supplier_id) + "/" +
            str(upload_id) + "/" +
            str(download_id) + "/"
        )
        return response

    # TODO: Phase out this method. we should use config ui instead.
    def upload_directory(self, directory_path, do_timestamps=True, pkey=1):
        """ Upload an entire directory of files.

        In order to achieve this I created a file naming convention.
        This naming convention splits the name into three parts separated
        by underscores and appended with a .csv extension:

            1. The file's type. Either dictionary or version corresponding
               to it's Oasis profile type.
            2. The specific name below the type. Must be any of the below:
                - areaperil
                - damagebin
                - event
                - exposure
                - hazardintensitybin
                - vuln
                - hazfp
            3. Lastly, for now, the module supplier will be hard coded into the
               name of each file. Really the main reason for this is because we
               do not have a config file to specify all of this.
               TODO: Create a config file to run everything automatically!

        Args:
            directory_path (str): path to the directory to upload from.
            do_timestamps (bool): optional, timestamps files or not?
            module_supplier_id (int): overall module supplier for uploading.
            pkey (int): UNKNOWN
        """

        # The data_dict stores all the information on uploaded files
        # and there respective structures.
        # TODO: Think of a better name for the data_dict.
        files_to_upload = glob.glob(directory_path + "*")
        timestamp = self.create_timestamps()
        # For all files in directory.
        for pathname in files_to_upload:
            filename = os.path.basename(pathname)

            # Split the '.'s as well cause they are file extensions.
            # We just want to get the first two parts of the name.
            splitname = filename.replace(".", "_").split("_")
            data_name = splitname[0] + "_" + splitname[1]
            module_supplier_id = splitname[2]

            assert len(splitname) == 4,\
                "Bad file name in folder: {filename}".format(filename=filename)
            assert data_name in self.types.keys(),\
                    ("File type {filetype} does not have proper type format. "
                    "Are you sure you spelt it right?").format(
                            filetype=data_name
                    )

            # Timestamp files if nessecary.
            if do_timestamps:
                upload_filename = timestamp + filename


            # Create the file upload and get ID.
            up_id = self.create_file_upload(
                upload_filename,
                self.pub_user,
                module_supplier_id
            )
            assert type(up_id) == int,\
                "Bad upload ID response: Not an integer!"

            # Create the file download and get ID.
            down_id = self.create_file_download(
                upload_filename,
                self.pub_user,
                module_supplier_id
            )
            assert type(down_id) == int,\
                "Bad download ID response: Not an integer!"

            # Actually upload the file to the server.
            self.upload_file(
                pathname,
                upload_filename
            )

            # Save the data for later use.
            # Update data_dict.
            self.data_dict[data_name] = {
                'filepath': pathname,
                'upload_name': upload_filename,
                'upload_id': up_id,
                'download_id': down_id,
                'module_supplier_id': module_supplier_id,
            }

        print("Uploaded directory")

    def prepare_file(self, data_name, pathname, module_supplier_id,
                     do_timestamps=True):
        """ Combines a few webservices for upload a file.

        "Prepare" is a term genrally meaning:
            - Creating the file upload and download id's.
            - And then actually uploading the file.

        Args:
            data_name (str): name from self.types dictionary.
            pathname (str): path to file to prepare.
            module_supplier_id (int): overall module supplier for uploading.
            do_timestamps (bool): whether to prepend timestamps on upload.
        """

        filename = os.path.basename(pathname)
        timestamp = self.create_timestamps()
        # Timestamp files if nessecary.
        if do_timestamps:
            upload_filename = timestamp + filename

        # Create the file upload.
        up_id = self.create_file_upload(
            upload_filename,
            self.pub_user,
            module_supplier_id
        )
        assert type(up_id) == int,\
            "Bad upload ID response: Not an integer!"

        # Create the file download.
        down_id = self.create_file_download(
            upload_filename,
            self.pub_user,
            module_supplier_id
        )
        assert type(down_id) == int,\
            "Bad download ID response: Not an integer!"

        # Actually upload the file to the server.
        self.upload_file(
            pathname,
            upload_filename
        )

        # Save the data for later use.
        # Update data_dict.
        self.data_dict[data_name] = {
            'filepath': pathname,
            'upload_name': upload_filename,
            'upload_id': up_id,
            'download_id': down_id,
            'module_supplier_id': module_supplier_id,
        }


    # TODO: Appropriately name this method.
    def load_models(self):
        """ Do tasks, load up models.

        Adds all the tasks in the data_dict to the job queue.
        """
        logger.info('Loading {name} data'.format(name=self.__class__.__name__))
        for type_name, type_ in self.data_dict.iteritems():
            # An exclude for correlations. Isn't created nor has an ID.
            if type_name == "version_correlation":
                continue
            task_response = self.do_task(
                self.types[type_name],
                type_['taskId']
            )
            self.data_dict[type_name]['job_id'] = json.loads(
                task_response.content
            )['JobId']
            logger.info(
                'Load {name} response: '.format(name=type_name) +
                task_response.content
            )

        print("Loaded model")


    def wait_until_done(self, job_id, status_check_interval, timeout,
                        init_wait_time=0, config_id=1):
        """ Waits until the specified job is complete.

        This is used because some jobs depend on others.
        Therfore we must wait until some jobs are completed.

        Args:
            job_id (int): ID of the job to wait for.
            status_check_interval (int, optional): seconds to wait between each
                async status check.
            timeout (int, optional): seconds to wait before timing out and
                raising an exception. If set to 0 there will be no timeout.
                Default value is 0.
            init_wait_time (int, optional): seconds to initially wait.
            config_id (int, optional): config that the job was created with.

        Returns:
            None
        """
        status = False
        i = 0
        start_seconds = time.time()
        time.sleep(init_wait_time)
        timed_out = False
        # Do until job finishes or max iters is reached.
        while status == False and timed_out == False:
            resp = self.check_status(job_id, config_id)
            logger.debug("Waiting for response " + resp.content)
            job_status = json.loads(resp.content)['status']
            job_progress = json.loads(resp.content)['progress']
            if job_progress == "FINISHED":
                logger.info("Previous, job done! " + resp.content)
                status = True
            elif job_status == 'done':
                logger.info("Previous, job done! " + resp.content)
                status = True
            # If the job fails stop everything and raise exception.
            elif job_status == "FAILED":
                raise Exception(
                    "FATAL: Job {num} failed with a response of: {resp}".format(
                        num=job_id,
                        resp=resp.content
                    )
                )
            elif job_status == "job dequeued":
                raise Exception(
                    "FATAL: Job {num} was dequeued with a response"
                    "of: {resp}".format(
                        num=job_id,
                        resp=resp.content
                    )
                )
            i += 1
            time.sleep(status_check_interval)

            # Only calculate if timeout isn't 0 (disabled).
            if timeout is not 0:
                timed_out = (time.time() - start_seconds) > timeout
        # If we hit the task timeout.
        if status == False:
            raise Exception(
                ("Job Load Timeout!\n"
                 "Job {job_id} timed-out after {timeout} seconds "
                 "before finishing. "
                 "Try setting a longer timeout time."
                ).format(job_id=job_id, timeout=timeout)
            )

    def queue_task(self, task_name):
        """ Simple add the specified task in the job queue.

        This is simple queuing the task only adding it to the queue.
        As opposed to do the job when we wait for it to complete.
        """
        task_response = self.do_task(
            self.types[task_name],
            self.data_dict[task_name]['taskId']
        )
        self.data_dict[task_name]['job_id'] = json.loads(
            task_response.content
        )['JobId']
        logger.info(
            'Queued {name} task response: '.format(name=task_name) +
            task_response.content
        )

    def do_job(self, task_name, status_check_interval=0.001, timeout=0):
        """ Wait until the job has been done on the job queue. """
        self.queue_task(task_name)
        self.wait_until_done(
            self.data_dict[task_name]['job_id'],
            status_check_interval=status_check_interval,
            timeout=timeout
        )

    def do_jobs(self, job_list,  status_check_interval=1, timeout=0):
        """ Do all dependant jobs in the given list. """
        for task_name in job_list:
            self.do_job(
                task_name,
                status_check_interval=status_check_interval,
                timeout=timeout
            )

    def easy_request(self, *args):
        """ Formats arguments passed into URL and makes the http request.

        Also prepends the base URL and a "/oasis/" so that all the users have
        to pass is just the strings that would otherwise be separated by
        slashes (/).

        Args:
            args (string list): List of strings to format into URL.

        Returns:
            HttpResponse: server's response
        """
        response = self.do_request(
            self.base_url +
            "/oasis/" +
            "/".join(map(str, args)) +
            "/"
        )
        return response

    def select_type(self, type_):
        """ Provides interface to select "type objects" on the Oasis server.

        This is mainly useful for the purpose of selecting a model for use with custom
        exposures. It is such a trivial task once we consider that an Oasis model
        consists of 5 or so different dictionaries and we must find the IDs for each
        one in order to create GUL results with manual exposures.

        Args:
            type_ (string):

        Return:
            int: The ID of the selected type object.
        """
        # Display a list of the Oasis objects.
        response = self.easy_request("list" + self.types[type_])
        type_list = json.loads(response.content)
        print "Please choose a {type} from the list below: ".format(
            type=self.types[type_]
        )
        for line in type_list:
            read_status = "Readable" if line['canRead'] else "Unreadable"
            job_status = "Successfully Ran" if line['success'] else "Failed Run"
            print line['optionValue'] + " " + line['optionDisplay'] +\
                "  Details: " + job_status + " and " + read_status

        # Ask user to select a displayed option, repeat until a valid option is
        # given.
        option = None
        options = map(lambda x: str(x['optionValue']), type_list) 
        while True:
            option = raw_input("What number? ")
            if option in options:
                break
            else:
                print ("Invalid number was selected. Please input a number that is "
                        "displayed above."
                      )
        return option
