from pyscrape               import Session
from pyscrape.driver.webkit import Driver

email    = 'white57@gmx.net'
password = 'queeNg0o'

# set up a web scraping session
sess = Session(driver   = Driver(),
               base_url = 'http://facebook.com')

# we don't need images
sess.set_attribute('auto_load_images', False)

# visit homepage and log in
sess.visit('/')
email_field    = sess.at_css('#email')
password_field = sess.at_css('#pass')
email_field.set(email)
password_field.set(password)
print "logging in..."
email_field.form().submit()

# save a screenshot of the web page
print "Writing screenshot to 'facebook.png'"
sess.render('facebook.png')
