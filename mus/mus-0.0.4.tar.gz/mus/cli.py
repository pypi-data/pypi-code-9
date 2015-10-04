
import leip

def dispatch():
    """
    Run the mus app
    """
    app.run()


app = leip.app(name='mus')
app.discover(globals())
