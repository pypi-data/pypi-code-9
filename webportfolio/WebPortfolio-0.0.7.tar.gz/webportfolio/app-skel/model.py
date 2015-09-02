"""
WebPortfolio

model.py

You may place your models here.
"""

from active_alchemy import SQLAlchemy
import config
from webportfolio import WebPortfolio, get_env_config
from webportfolio.module import user, cms

# The config
conf = get_env_config(config)

# Connect the DB
db = SQLAlchemy(conf.SQL_URI)

# Bind the DB connection to WebPortfolio
WebPortfolio.bind(db.init_app)

# ------------------------------------------------------------------------------

# User Model
User = user.model(db)

# Post Model
Cms = cms.model(User)

# A simple my not example table
class MyNote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.User.id))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    user = db.relationship(User.User, backref="notes")
