"""
::WebPortfolio::

run_www.py

To run the server
"""

from webportfolio import WebPortfolio, get_env

# Import the application's views
import application.www.views

# The directory containing your views/webportfolio/templates
app_dir = "application/www"

# The project config object
app_config = "application.config.%s" % get_env()

WP = WebPortfolio()

# WebPortfolio.init returns Flask instance
app = WP.init(__name__, directory=app_dir, config=app_config, compress_html=False)


if __name__ == "__main__":
    import os
    import os.path as path
    extra_dirs = ['../webportfolio',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(debug=True, extra_files=extra_files)
