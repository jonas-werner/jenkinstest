import os
import redis
import json
import uuid
from flask import Flask, render_template, redirect, request, url_for, make_response

if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
else:
    r = redis.Redis(host='192.168.11.97', port='6379')


app = Flask(__name__)
my_uuid = str(uuid.uuid1())


@app.route('/')
def survey():
    resp = make_response(render_template('survey.html'))
    return resp

@app.route('/results')
def results():

    TOP = """
        <!DOCTYPE html>
        <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!-- Latest compiled and minified CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
            <link rel="stylesheet" href="static/stylesheet.css">
          </head>
          <body>
      """

    div1 = """
        <div class="container-fluid">
            <div class="col-sm-12" id="topdiv">
                <h1>Tech Summit 2019</h1>
                <h2>Best presales conference on the planet</h2>
            </div>
            <div class="col-sm-6">
                <h1>Agenda</h1>
                <h2>This will help you plan your day</h2>
                <img src="static/agenda icon.png">
            </div>
            <div class="col-sm-6">

     """

    feedback = TOP + div1

    for key in r.keys("feedback-form*"):
        print(r.hgetall(key))

        feedback = feedback + "<table padding=1 border=1 width=400><tr>"
        feedback = feedback + "<td width=120>Affiliation</td><td width=60>State</td><td width=120>Feedback</td></tr><tr>"
        feedback = feedback + "<td>" + r.hget(key,'affiliation') + "</td>"
        feedback = feedback + "<td>" + r.hget(key,'state') + "</td>"
        feedback = feedback + "<td>" + r.hget(key,'feedback') + "</td>"
        feedback = feedback + "</tr></table><br>"


    BOTTOM = """
                </div>
                <div class="col-sm-12">
                     <br>
                     <a href="/">Main menu</a>
                     <br>
                     Hi, I'm GUID: {}<br>
                 </div>
             </div>
        </body>
    </html>
    """.format(my_uuid)

    return feedback


@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():

    counter = r.incr('new_counter')

    ## This is how you grab the contents from the form
    affiliation = request.form['affiliation']
    state       = request.form['state']
    feedback    = request.form['feedback']

    ## Now you can now do someting with variable "f"
    print "The feedback received was:"
    print("Affiliation: %s" % affiliation)
    print("State: %s" % state)
    print("Feedback: %s" % feedback)

    key = "feedback-form-" + str(counter)

    r.hmset(key, {'affiliation': affiliation, 'state': state, 'feedback': feedback})


    resp = """
    <h3> - THANKS FOR TAKING THE SURVEY - </h3><br>
    <p>Your feedback:</p>
    <ul>
        <li>Affiliation: {}</li>
        <li>State: {}</li>
        <li>Feedback: {}</li>
    </ul>
    <a href="/"><h3>Back to main menu</h3></a>
    """.format(affiliation, state, feedback)

    return resp

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
