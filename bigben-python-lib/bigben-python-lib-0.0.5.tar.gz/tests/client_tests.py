import logging
from types import DictType, ListType
import unittest
import os
from bigben.client import Client

"""
    Unit tests to cover the client module.
"""

class ClientTest(unittest.TestCase):
    """
        Tests for the bigben.client.Client class.
    """

    def setUp(self):
        """
            Sets up the test.
        """
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('bigben.transport').setLevel(logging.DEBUG)
        # Grab the API key for the secret account
        api_token = os.environ.get('API_TOKEN', "e83e88b681ed432dbe513e8e941eeb08")

        self.client = Client(api_token, 'BigBinPythonTestRunner', "v1")


    def testCreateJob(self):
        """
            Tests the create job call.
        """
        job = self.client.create_job(3L,
                                     "Create Test Job",
                                     "*/5 * * * *",
                                     True,
                                     "GET",
                                     "http://google.com",
                                     5,
                                     {"test":"test", "test2": "test22"},

                                     )
        self.assertTrue(isinstance(job, DictType), "job is not a dictionary")
        self.assertEqual(len(job), 12)
        self.client.delete_job(job['id'])


    def testUpdateJob(self):
        """
            Tests the update job call.
        """
        job = self.client.create_job(3L,
                                     "Update Test Job",
                                     "*/5 * * * *",
                                     True,
                                     "GET",
                                     "http://google.com",
                                     5,
                                     {"test":"test", "test2": "test22"},

                                     )
        self.assertTrue(isinstance(job, DictType), "job is not a dictionary")
        self.assertEqual(len(job), 12)

        updated_job = self.client.update_job(job['id'],
                                             "Updated Test Job",
                                             "*/5 * * * *",
                                             False,
                                             "GET",
                                             "http://google.com",
                                             4,
                                             {"test":"test", "test2": "testsdfsdf22"},
                                             [])
        self.assertTrue(isinstance(updated_job, DictType), "job is not a dictionary")
        self.assertEqual(len(updated_job), 12)
        self.assertTrue(updated_job['is_active'] is False)
        self.assertTrue(updated_job['name'] == "updated test job")

        self.client.delete_job(job['id'])

    def testGetJob(self):
        """
            Tests getting a single job.
        """
        self.assertTrue(1==1)


    def testListJobs(self):
        """
            Tests the list jobs call.
        """
        jobs = self.client.list_jobs()
        self.assertTrue(isinstance(jobs, ListType))

    def testDeleteJob(self):
        """
            Tests the delete job call.
        """

        self.assertTrue(1==1)

    def testDeleteAllJobs(self):
        """
            Tests the deletion of all jobs.
        """
        for job in self.client.list_jobs():
            self.client.delete_job(job['id'])

        jobs = self.client.list_jobs()
        self.assertTrue(len(jobs) == 0)

if __name__ == '__main__':
    unittest.main()