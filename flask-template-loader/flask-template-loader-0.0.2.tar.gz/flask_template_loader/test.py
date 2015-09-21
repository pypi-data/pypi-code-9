import flask
from . import FlaskTemplateLoader



def main():
    app = flask.Flask(__name__)
    app.config['TEMPLATE_LOADERS'] = [
        'testdir.loader',
    ]
    
    loader = FlaskTemplateLoader(app)


    with app.test_request_context():
        print flask.render_template('x')


