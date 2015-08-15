"""punter-cli - Simple CLI for the Email Hunter API.

The command line interface provides commands for initially setting and
updating the required API key and executing searches on either domains
or email addresses.

The API key can be set or retrieved depending on whether a key is
passed to the `key` command. Example usage is as follows:

    $ punter key d08d2ba22218d1b59df239d03fc5e66adfaec2b2
    $ punter key
    d08d2ba22218d1b59df239d03fc5e66adfaec2b2

Executing a domain search:

    $ punter search lamppostgroup.com
    {
    "status": "success",
    "pattern": "{first}.{last}",
    "results": 4,
    "webmail": false,
    "offset": 0,
    "emails": [{
        "sources": [
            {
                "domain": "chugalug.org",
                "extracted_on": "2015-01-25",
                "uri": "http://chugalug.org/widget/2550/who"
            },
        ...
    ...
    ]}

"""


__title = 'punter-cli'
__author__ = 'Joshua Goodlett'
__version__ = '0.0.3'
__license__ = 'MIT'
