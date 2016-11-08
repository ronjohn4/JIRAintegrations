from JIRAdataactive import *
from JIRAdatacomplete import *
from flask import Flask
from flask import render_template


#web output
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    # flash('New entry was successfully posted')
    # flash('This is a second flash')
    return render_template('home.html')


@app.route('/active')
def show_active():
    sorted_display_list = epics_active()
    return render_template('epicsactive.html', entries=sorted_display_list)
    # print(dataprint.to_string(sorted_display_list, comments=None, comment_lead=''))


@app.route('/complete')
def show_complete():
    sorted_display_list = epics_complete()
    return render_template('epicscomplete.html', entries=sorted_display_list)
    # print(dataprint.to_string(sorted_display_list, comments=None, comment_lead=''))


if __name__ == '__main__':
    app.debug = True

    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    app.run(port=5001)

