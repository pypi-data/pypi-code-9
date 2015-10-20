"""cubicweb-datacat unit tests for hooks"""

from datetime import datetime

from cubicweb.devtools.testlib import CubicWebTC

from utils import create_file, produce_file


class DataProcessWorkflowHooksTC(CubicWebTC):

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            ds = cnx.create_entity('Dataset', title=u'Test dataset')
            di = cnx.create_entity('Distribution', of_dataset=ds)
            cnx.commit()
            self.dataset_eid = ds.eid
            self.distribution_eid = di.eid

    def _setup_and_start_dataprocess(self, cnx, process_etype, scriptcode):
        inputfile = create_file(cnx, 'data',
                                file_distribution=self.distribution_eid)
        script = cnx.create_entity('Script',
                                   name=u'%s script' % process_etype)
        create_file(cnx, scriptcode, reverse_implemented_by=script.eid)
        with cnx.security_enabled(write=False):
            process = cnx.create_entity(process_etype,
                                        process_script=script)
            cnx.commit()
        process.cw_clear_all_caches()
        iprocess = process.cw_adapt_to('IDataProcess')
        self.assertEqual(process.in_state[0].name,
                         iprocess.state_name('initialized'))
        process.cw_set(process_input_file=inputfile)
        cnx.commit()
        process.cw_clear_all_caches()
        return process

    def test_data_process_autostart(self):
        with self.admin_access.repo_cnx() as cnx:
            script = cnx.create_entity('Script', name=u'v')
            create_file(cnx, '1/0', reverse_implemented_by=script)
            with cnx.security_enabled(write=False):
                process = cnx.create_entity('DataValidationProcess',
                                            process_script=script)
                cnx.commit()
            self.assertEqual(process.in_state[0].name,
                             'wfs_dataprocess_initialized')
            inputfile = create_file(cnx, 'data',
                                    file_distribution=self.distribution_eid)
            # Triggers "start" transition.
            process.cw_set(process_input_file=inputfile)
            cnx.commit()
            process.cw_clear_all_caches()
            self.assertEqual(process.in_state[0].name,
                             'wfs_dataprocess_error')

    def test_data_process(self):
        with self.admin_access.repo_cnx() as cnx:
            for ptype in ('transformation', 'validation'):
                etype = 'Data' + ptype.capitalize() + 'Process'
                process = self._setup_and_start_dataprocess(cnx, etype, 'pass')
                self.assertEqual(process.in_state[0].name,
                                 'wfs_dataprocess_completed')
                process.cw_delete()
                cnx.commit()
                process = self._setup_and_start_dataprocess(cnx, etype, '1/0')
                self.assertEqual(process.in_state[0].name,
                                 'wfs_dataprocess_error')

    def test_data_process_output(self):
        with self.admin_access.repo_cnx() as cnx:
            self._setup_and_start_dataprocess(
                cnx, 'DataTransformationProcess',
                open(self.datapath('cat.py')).read())
            rset = cnx.execute(
                'Any X WHERE EXISTS(X produced_by S)')
            self.assertEqual(len(rset), 1)
            stdout = rset.get_entity(0, 0)
            self.assertEqual(stdout.read(), 'data\n')

    def test_data_validation_process_validated_by(self):
        with self.admin_access.repo_cnx() as cnx:
            script = cnx.create_entity('Script', name=u'v')
            create_file(cnx, 'pass', reverse_implemented_by=script)
            with cnx.security_enabled(write=False):
                process = cnx.create_entity('DataValidationProcess',
                                            process_script=script)
                cnx.commit()
            inputfile = create_file(cnx, 'data',
                                    file_distribution=self.distribution_eid)
            # Triggers "start" transition.
            process.cw_set(process_input_file=inputfile)
            cnx.commit()
            process.cw_clear_all_caches()
            self.assertEqual(process.in_state[0].name,
                             'wfs_dataprocess_completed')
            validated = cnx.find('File', validated_by=process).one()
            self.assertEqual(validated, inputfile)

    def test_data_process_dependency(self):
        """Check data processes dependency"""
        with self.admin_access.repo_cnx() as cnx:
            vscript = cnx.create_entity('Script', name=u'v')
            create_file(cnx, 'pass', reverse_implemented_by=vscript)
            with cnx.security_enabled(write=False):
                vprocess = cnx.create_entity('DataValidationProcess',
                                             process_script=vscript)
                cnx.commit()
            tscript = cnx.create_entity('Script', name=u't')
            create_file(cnx,
                        ('import sys;'
                         'sys.stdout.write(open(sys.argv[1]).read())'),
                        reverse_implemented_by=tscript)
            with cnx.security_enabled(write=False):
                tprocess = cnx.create_entity('DataTransformationProcess',
                                             process_depends_on=vprocess,
                                             process_script=tscript)
                cnx.commit()
            inputfile = create_file(cnx, 'data',
                                    file_distribution=self.distribution_eid)
            vprocess.cw_set(process_input_file=inputfile)
            tprocess.cw_set(process_input_file=inputfile)
            cnx.commit()
            vprocess.cw_clear_all_caches()
            tprocess.cw_clear_all_caches()
            assert vprocess.in_state[0].name == 'wfs_dataprocess_completed'
            self.assertEqual(tprocess.in_state[0].name,
                             'wfs_dataprocess_completed')
            rset = cnx.find('File', produced_by=tprocess)
            self.assertEqual(len(rset), 1, rset)
            output = rset.one()
            self.assertEqual(output.read(), inputfile.read())

    def test_data_process_dependency_validation_error(self):
        """Check data processes dependency: validation process error"""
        with self.admin_access.repo_cnx() as cnx:
            vscript = cnx.create_entity('Script', name=u'v')
            create_file(cnx, '1/0', reverse_implemented_by=vscript)
            with cnx.security_enabled(write=False):
                vprocess = cnx.create_entity('DataValidationProcess',
                                             process_script=vscript)
                cnx.commit()
            tscript = cnx.create_entity('Script', name=u't')
            create_file(cnx, 'import sys; print open(sys.argv[1]).read()',
                        reverse_implemented_by=tscript)
            with cnx.security_enabled(write=False):
                tprocess = cnx.create_entity('DataTransformationProcess',
                                             process_depends_on=vprocess,
                                             process_script=tscript)
                cnx.commit()
            inputfile = create_file(cnx, 'data',
                                    file_distribution=self.distribution_eid)
            # Triggers "start" transition.
            vprocess.cw_set(process_input_file=inputfile)
            tprocess.cw_set(process_input_file=inputfile)
            cnx.commit()
            vprocess.cw_clear_all_caches()
            tprocess.cw_clear_all_caches()
            assert vprocess.in_state[0].name == 'wfs_dataprocess_error'
            self.assertEqual(tprocess.in_state[0].name,
                             'wfs_dataprocess_initialized')


class ResourceFeedHooksTC(CubicWebTC):

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            ds = cnx.create_entity('Dataset', title=u'Test dataset')
            cnx.commit()
            self.dataset_eid = ds.eid

    def test_distribution_created(self):
        with self.admin_access.repo_cnx() as cnx:
            resourcefeed = cnx.create_entity(
                'ResourceFeed', url=u'a/b/c',
                data_format=u'text/blah',
                resource_feed_of=self.dataset_eid)
            cnx.commit()
            self.assertTrue(resourcefeed.resourcefeed_distribution)
            dist = resourcefeed.resourcefeed_distribution[0]
            self.assertEqual(dist.format, u'text/blah')
            self.assertEqual([x.eid for x in dist.of_dataset],
                             [self.dataset_eid])

    def test_resourcefeed_cwsource(self):
        with self.admin_access.repo_cnx() as cnx:
            resourcefeed = cnx.create_entity(
                'ResourceFeed', url=u'a/b/c',
                resource_feed_of=self.dataset_eid)
            cnx.commit()
            source = resourcefeed.resource_feed_source[0]
            self.assertEqual(source.url, resourcefeed.url)
            resourcefeed.cw_set(url=u'c/b/a')
            cnx.commit()
            source.cw_clear_all_caches()
            self.assertEqual(source.url, u'c/b/a')
            resourcefeed1 = cnx.create_entity(
                'ResourceFeed', url=u'c/b/a',
                resource_feed_of=self.dataset_eid)
            cnx.commit()
            self.assertEqual(resourcefeed1.resource_feed_source[0].eid,
                             source.eid)

    def test_linkto_dataset(self):
        with self.admin_access.repo_cnx() as cnx:
            inputfile = create_file(cnx, 'data')
            script = cnx.create_entity('Script', name=u'script')
            create_file(cnx, 'pass', reverse_implemented_by=script.eid)
            resourcefeed = cnx.create_entity('ResourceFeed', url=u'a/b/c',
                                             resource_feed_of=self.dataset_eid,
                                             transformation_script=script)
            cnx.commit()
            produce_file(cnx, resourcefeed, inputfile)
            rset = cnx.execute('Any X WHERE X file_distribution D, D eid %s' %
                               resourcefeed.resourcefeed_distribution[0].eid)
            self.assertEqual(len(rset), 1, rset)
            outdata = rset.get_entity(0, 0).read()
            self.assertEqual(outdata, 'plop')

    def test_file_replaced(self):
        with self.admin_access.repo_cnx() as cnx:
            script = cnx.create_entity('Script', name=u'script')
            create_file(cnx, 'pass', reverse_implemented_by=script.eid)
            resourcefeed = cnx.create_entity('ResourceFeed', url=u'a/b/c',
                                             resource_feed_of=self.dataset_eid,
                                             transformation_script=script)
            cnx.commit()
            outfile1 = produce_file(cnx, resourcefeed,
                                    create_file(cnx, 'data'))
            outfile2 = produce_file(cnx, resourcefeed,
                                    create_file(cnx, 'data 2'))
            outfile3 = produce_file(cnx, resourcefeed,
                                    create_file(cnx, 'data 3'))
            rset = cnx.execute('Any F1,F2 WHERE F1 replaces F2')
            self.assertEqual(rset.rowcount, 2)
            self.assertIn([outfile2.eid, outfile1.eid], rset.rows)
            self.assertIn([outfile3.eid, outfile2.eid], rset.rows)
            rset = cnx.execute(
                'Any X WHERE X file_distribution D, D eid %(d)s',
                {'d': resourcefeed.resourcefeed_distribution[0].eid})
            self.assertEqual(rset.rowcount, 1)
            self.assertEqual(rset[0][0], outfile3.eid)


class FileDistributionRelationHooksTC(CubicWebTC):

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            ds = cnx.create_entity('Dataset', identifier=u'ds', title=u'ds')
            self.distribution_eid = cnx.create_entity(
                'Distribution', of_dataset=ds, title=u'THE distr',
                description=u'one and only').eid
            cnx.commit()

    @staticmethod
    def create_file(cnx, **kwargs):
        """Simplified version of utils.create_file"""
        return create_file(cnx, data_name=u"foo.txt", data="xxx", **kwargs)

    def create_distribution_file(self, cnx, **kwargs):
        """Create a file link to self.distribution_eid"""
        return self.create_file(cnx, file_distribution=self.distribution_eid)

    def test_update_file_of_distribution(self):
        with self.admin_access.repo_cnx() as cnx:
            file_v1 = self.create_distribution_file(cnx)
            cnx.commit()
            distr = cnx.find('Distribution', eid=self.distribution_eid).one()
            self.assertEqual(distr.reverse_file_distribution[0], file_v1)
            file_v2 = self.create_file(cnx, replaces=file_v1)
            cnx.commit()
            distr = cnx.find('Distribution', eid=self.distribution_eid).one()
            self.assertEqual(distr.reverse_file_distribution[0], file_v2)
            self.assertEqual(file_v2.replaces[0], file_v1)

    def test_update_distribution_on_create_filedistribution(self):
        with self.admin_access.repo_cnx() as cnx:
            distr = cnx.entity_from_eid(self.distribution_eid)
            self.assertIsNone(distr.byte_size)
            self.assertIsNone(distr.format)
            self.assertIsNone(distr.download_url)
            distr_file = self.create_distribution_file(cnx)
            cnx.commit()
            self.assertEqual(distr.byte_size, distr_file.size())
            self.assertEqual(distr.format, distr_file.data_format)
            self.assertEqual(distr.download_url,
                             distr_file.cw_adapt_to("IDownloadable").download_url())

    def test_update_distribution_on_create_and_on_update(self):
        """Test the value of issued and modified
            - when no file is defined : issued = modified = None
            - when a file is added : issued ~= modified = time when the file is added
            - when a new file is added : issued ~= modified = time when the new file is added
            - when the last file is updated : issued = time when the file was added,
                                              modified = time when the file was updated
            - when an older file is updated : nothing change
        """
        with self.admin_access.repo_cnx() as cnx:
            distr = cnx.entity_from_eid(self.distribution_eid)
            self.assertIsNone(distr.issued)
            self.assertIsNone(distr.modified)
            file_v1 = self.create_distributionfile_and_check_date(cnx)
            file_v2 = self.create_distributionfile_and_check_date(cnx)
            self.update_file_and_check_date(cnx, file_v2, current_file=True)
            self.update_file_and_check_date(cnx, file_v1, current_file=False)

    def create_distributionfile_and_check_date(self, cnx):
        before = datetime.now()
        distr_file = self.create_distribution_file(cnx)
        after = datetime.now()
        cnx.commit()
        distr = cnx.entity_from_eid(self.distribution_eid)
        for date in [distr.issued, distr.modified]:
            self.assertLess(before, date)
            self.assertLess(date, after)
        return distr_file

    def update_file_and_check_date(self, cnx, distr_file, current_file):
        before_update = datetime.now()
        distr_file.cw_set(data_name=u'bar.txt')
        after_update = datetime.now()
        cnx.commit()
        distr = cnx.entity_from_eid(self.distribution_eid)
        issued, modified = distr.issued, distr.modified
        self.assertTrue(issued < before_update)
        if current_file:
            self.assertLess(before_update, modified)
            self.assertLess(modified, after_update)
        else:
            self.assertLess(modified, before_update)

    def test_set_title_description(self):
        with self.admin_access.repo_cnx() as cnx:
            distr_file = self.create_distribution_file(cnx)
        self.assertEqual(distr_file.title, 'THE distr')
        self.assertEqual(distr_file.description, 'one and only')


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
