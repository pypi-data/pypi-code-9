import os
import unittest
import responses

from primer_designer import PrimerDesigner


TEST_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data')
ALIGNMENT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data', 'Ca2.fst')
RESPONSE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Data', 'response_Ca2.fst.html')


class PrimerDesignerTest(unittest.TestCase):
    def setUp(self):
        self.pd = PrimerDesigner(
            folder=TEST_FOLDER,
            tm="55",
            min_amplength="200",
            max_amplength="500",
            gencode="universal",
            mode="primers",
            clustype="protein",
            amptype="dna_GTRG",
            email="youremail@email.com",
        )

    def tearDown(self):
        output_html_file = '{0}.html'.format(ALIGNMENT)
        if os.path.isfile(output_html_file):
            os.remove(output_html_file)

    @responses.activate
    def test_request_primers(self):
        url = "http://floresta.eead.csic.es/primers4clades/primers4clades.cgi"
        with open(RESPONSE, 'r') as handle:
            response_html_body = handle.read()

        responses.add(responses.POST, url,
                      body=response_html_body,
                      status=200,
                      content_type='application/text',
                      )
        resp = self.pd.request_primers(ALIGNMENT)
        assert resp.content.decode('ascii') == response_html_body

    def test_process_response(self):
        self.pd.process_response(ALIGNMENT, open(RESPONSE).read())
        self.assertTrue('gayaaytaygahytdaargaagaaytdggvaargghgc' in
                        [str(seq.seq) for seq in self.pd.designed_primers])
