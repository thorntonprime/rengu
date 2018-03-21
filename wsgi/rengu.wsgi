from flask import Flask, render_template

app = Flask(__name__)

@app.route('/source')
@app.route('/source/<pkid>')
def source(pkid=None):
  return render_template('source.html', pkid=pkid)

