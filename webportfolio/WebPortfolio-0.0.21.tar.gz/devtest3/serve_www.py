"""
::WebPortfolio::

serve_www.py

This is the entry point of the application.


"""

from webportfolio import WebPortfolio, get_env

# Import the application's views
import application.www.views

# The directory containing your views/webportfolio/templates
app_dir = "application/www"

# The project config object
app_config = "application.config.%s" % get_env()

# WebPortfolio
# init() returns a flask object instance
WP = WebPortfolio()
app = WP.init(__name__, directory=app_dir, config=app_config)

if __name__ == "__main__":
    app.run(debug=True)
