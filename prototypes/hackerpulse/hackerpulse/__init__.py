from flask import Flask
import settings

app = Flask('hackerpulse')
app.config.from_object('hackerpulse.settings')

import views
import filters