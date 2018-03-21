from flask import Flask, render_template

application = Flask(__name__)

@application.route('/source')
@application.route('/source/<pkid>')
def source(pkid=None):
  return render_template('source.html', pkid=pkid)

