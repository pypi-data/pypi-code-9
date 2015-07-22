from nose.tools import assert_equal

from ckan import model
import ckan.lib.search as search

def check_search_results(terms, expected_count, expected_packages=[]):
    query = {
        'q': unicode(terms),
    }
    result = search.query_for(model.Package).run(query)
    pkgs = result['results']
    count = result['count']
    assert_equal(count, expected_count)
    for expected_pkg in expected_packages:
        assert expected_pkg in pkgs, '%s : %s' % (expected_pkg, result)
