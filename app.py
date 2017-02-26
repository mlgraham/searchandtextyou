from flask import Flask, request, render_template
from twilio import twiml
from twilio.rest import TwilioRestClient
import sqlite3, sys

app = Flask(__name__, static_folder='static', static_url_path='')

def postRecord(phone, message):
    details = message.split(';')
    victimid = details[0]
    latitude = details[1]
    longitude = details[2]
    status = details[3]
    try:
        con = sqlite3.connect('searchandtextyou.db')
        cur = con.cursor()
        cur.execute('insert into victims (phone, victimid, latitude, longitude, status) values ('+str(phone)+','+str(victimid)+','+str(latitude)+','+str(longitude)+',\''+str(status)+'\')')
        con.commit()
        # print 'written to db'
        account_sid = "XXXXXXXXXX"
        auth_token = "XXXXXXXXXX"
        client = TwilioRestClient(account_sid, auth_token)
        responderalert = client.messages.create(to="+1XXXXXXXXXX", from_="+1XXXXXXXXXX", body=message)
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()

def fetchRecords():
    try:
        con = sqlite3.connect('searchandtextyou.db')
        cur = con.cursor()    
        cur.execute('select * from victims')
        results = []
        for each in cur:
            results.append(each)
        return results
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()

@app.route("/", methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        number = request.form['From']
        message_body = request.form['Body']

        postRecord(number, message_body)

        # resp = twiml.Response()
        # resp.message('Hello {}, you said: {}'.format(number, message_body))
        # return str(resp)
    victims = fetchRecords()
    return render_template('index.html', victims=victims)

@app.route('/rest/')
def rest():
    postRecord('13210001234', request.query_string)
    return request.query_string

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

