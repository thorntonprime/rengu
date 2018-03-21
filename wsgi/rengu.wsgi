#!/usr/bin/python3

import os
import sys
import getpass


from flask import Flask, render_template
app = Flask(__name__)

import prajna.rengu.config

@app.route('/s/')
@app.route('/s/<pkid>')
def get_source(pkid=None):
  from prajna.rengu.source import Source

  try:
    s = Source.fetch(pkid)
  except:
    s = Source({ 'Title': 'NONE' })

  return render_template('source.html', pkid=s.get("Title"))


if __name__ == '__main__':
    app.run()

