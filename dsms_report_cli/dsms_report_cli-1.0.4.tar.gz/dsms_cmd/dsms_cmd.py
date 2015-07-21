import os
import requests
import logging
import jinja2 as j2
import iso8601

logger = logging.getLogger(name=__name__)
logging.basicConfig(level=logging.WARN)

isodatelog = logging.getLogger("iso8601.iso8601")
isodatelog.setLevel(logging.WARN)

URL_TOKEN = "/token/new.json"
URL_SEARCH = "/api/v1/target/search/"

MAX_FETCHES = 1000


def _get_setting(key, fail_on_missing=True):
    val = os.environ.get(key, None)

    if fail_on_missing and not val:
        raise ValueError("Missing {} from environment settings".format(key))
    elif not val:
        return
    return val


def _str_to_datetime(date_iso8601_str):
    try:
        return iso8601.parse_date(date_iso8601_str)
    except:
        return None


class DSMSReporter(object):
    """
    DSMSReporter authenticates to a DSMS server, run a query, then transforms
    and outputs those results based on a Jinja2 template.

    ignore_ssl_errs: set True to ignore any SSL certificate errors (e.g. self
                     signed certs)
    do_auth:         default: True. Set False to avoid authenticating to a
                     DSMS server (speeds up certain operations)
    """
    def __init__(self, ignore_ssl_errs=False, do_auth=True):
        self.server = _get_setting("DSMS_SERVER")
        self.username = _get_setting("DSMS_USER")
        self.password = _get_setting("DSMS_PASS")
        self.user_id = None
        self.token = None
        self.ignore_ssl_errs = ignore_ssl_errs
        self.do_auth = do_auth

        if do_auth:
            self._create_session()

    def _create_session(self):
        """
        Authenticate to a DSMS server, get a token and user_id
        """
        params = {'username': self.username, 'password': self.password}

        try:
            resp = requests.post("{0}{1}".format(self.server, URL_TOKEN),
                                 data=params,
                                 verify=not self.ignore_ssl_errs)
            jresp = resp.json()

            if jresp.get("success"):
                self.token = jresp["token"]
                self.user_id = jresp["user"]
                logger.debug("Created session")
            else:
                raise RuntimeError("DSMS login failed")
        except (requests.ConnectionError, requests.RequestException) as e:
            raise RuntimeError("Error during login: {}".format(str(e)))
        except KeyError:
            raise RuntimeError("Couldn't get username or token from response")

    def fetch_page(self, search, page):
        """
        Run a single query to the DSMS web API and return the JSON results.
        Raises RuntimeError if we hit any problems, e.g. server down or results
        aren't JSON.
        """
        get_params = {
            'target_filter': search,
            'page': page,
        }
        post_data = {
            'user': self.user_id,
            'token': self.token,
        }

        try:
            resp = requests.post("{0}{1}".format(self.server, URL_SEARCH),
                                 params=get_params,
                                 data=post_data,
                                 verify=not self.ignore_ssl_errs)
            return resp.json()
        except (requests.ConnectionError, requests.RequestException) as e:
            raise RuntimeError("Couldn't establish session with DSMS: {}"
                               .format(e))
        except ValueError as e:  # JSON parse error
            raise RuntimeError("Error during data fetch: {}".format(e))

    def query_data(self, search):
        """
        Based on a DSMS search query, search, ask DSMS for matching records.
        Loops over each page of results returned by the DSMS API, and returns
        a concatenated list of dicts containing all results.

        Limited to fetching result pages MAX_FETCHES times.
        """
        logger.debug("Searching for {}".format(search))
        page = None
        next_page_num = 1
        last_page_num = 0
        fetch = True
        fetch_count = 0

        results = []

        while fetch:
            if last_page_num == next_page_num:
                raise RuntimeError("We've fetched the same page of results "
                                   "twice: something has gone wrong.")

            page = self.fetch_page(search, page)

            for result in page.get("results", []):
                result["added"] = _str_to_datetime(result.get("added", ""))
                results.append(result)

            last_page_num = next_page_num
            if page.get("next_page"):
                next_page_num = page.get("next_page")
            else:
                fetch = False

            fetch_count += 1

            if fetch_count > MAX_FETCHES:
                logger.warn("Exceeded maximum number of API fetches at {}, "
                            "truncating results".format(MAX_FETCHES))
                fetch = False

        return results

    def list_templates(self, template_dir=None):
        """
        Return a list of templates found in the default and any custom template
        directories. Strips the '.j2' path from the end, to present in format
        ready for inclusion in --template argument.
        """
        loader = self._get_template_loader(
            template_dir=template_dir)
        jenv = j2.Environment(loader=loader)
        return [f.replace(".j2", "") for f in jenv.list_templates()]

    def _get_template_loader(self, template_dir=None):
        """
        Returns a jinja2 template loader with the default template path and
        a custom template path if one has been supplied.

        This is passed into a jinja2 Environment later on for template
        discovery.
        """
        template_paths = [os.path.join(os.path.dirname(__file__), "templates")]

        if template_dir:
            template_paths.append(template_dir)

        return j2.FileSystemLoader(template_paths)

    def output(self, data, template="text_urls", template_dir=None):
        """
        Given a list of dicts containing DSMS records, pass this to a template
        supplied by the template parameter. Return the rendered result.

        data: list of dicts to be passed to template
        template: name of jinja2 template to use with extension removed
        template_dir: optional search path for templates.
        """
        loader = self._get_template_loader(
            template_dir=template_dir)
        jenv = j2.Environment(loader=loader)

        try:
            template_file = "{}.j2".format(template)
            logger.debug("Using template file {}".format(template_file))
            template = jenv.get_template(template_file)
            return template.render(records=data)
        except IOError as e:
            raise RuntimeError("Couldn't open template file {0}: {1}"
                               .format(template, e))
        return data
