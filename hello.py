import os
import json, httplib
import urllib
import sys

from flask import Flask, request, redirect, url_for, render_template, session


def increment_counter():
     import json,httplib
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     connection.connect()
     connection.request('PUT', '/1/classes/TestObject/sX4nS3c1KY', json.dumps({
       "roomCounter": {
         "__op": "Increment",
         "amount": 1
       }
     }), {
       "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
       "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK",
       "Content-Type": "application/json"
     })
     result = json.loads(connection.getresponse().read())
     localcounter = result['roomCounter']
     return localcounter


def get_counter():
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     params = urllib.urlencode({"where":json.dumps({"roomCounter":{"$exists":True},"objectId":"sX4nS3c1KY"})})
#     params = urllib.urlencode({"where":json.dumps({"objectId":"sX4nS3c1KY"})})
     connection.connect()
     connection.request('GET', '/1/classes/TestObject?%s' % params, '', {
          "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
          "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
     })
     result = json.loads(connection.getresponse().read())['results'][0]['roomCounter']
     return result

#print increment_counter()
#globalcounter = get_counter()


app = Flask(__name__)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
@app.route('/index')
def hello():
     return render_template('index.html')

@app.route('/signup')
def registerPage():
     return render_template('signup.html')

@app.route('/handsontable', methods = ['GET'])
def handsonrender():
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     params = urllib.urlencode({"order":"-createdAt","limit":1,"where":json.dumps({"questionData2":{"$exists":True},"username":"foo9"})})
     connection.connect()
     connection.request('GET', '/1/classes/GameScore?%s' % params, '', {
          "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
          "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
     })
     result = json.loads(connection.getresponse().read())
     if len(result['results']) == 0:
          return render_template("hello2.html",names=[],username=username)
     filecontents = result['results'][0]['questionData2']
     
     return render_template('handsontest.html',
                            data=json.dumps(filecontents),
                            username=json.dumps('foobar'),
                            roomname='No name',
                            unescapedUsername='foobar')


def render_list(username):
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     params = urllib.urlencode({"order":"-createdAt","keys":"username,roomName,roomNumber","where":json.dumps({"questionData2":{"$exists":True},"roomNumber":{"$exists":True},"username":username})})
     connection.connect()
     connection.request('GET', '/1/classes/GameScore?%s' % params, '', {
          "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
          "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
     })
     result = json.loads(connection.getresponse().read())
     return render_template('list.html',rows=result['results'])
     

@app.route('/listtest', methods = ['GET'])
def listalltest():
     username = request.args.get('username','')
     return render_list(username)

@app.route('/list', methods = ['GET'])
def listall():
     username = session['username']
     return render_list(username)


@app.route('/showtable', methods = ['GET'])
def showtable():
     tableid = request.args.get('tableid','')
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     params = urllib.urlencode({"keys":"questionData2,roomName,roomNumber,pointsToWin,pageUrl,pageTime,randomized","where":json.dumps({"objectId":tableid})})
     connection.connect()
     connection.request('GET', '/1/classes/GameScore?%s' % params, '', {
          "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
          "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
     })
     result = json.loads(connection.getresponse().read())

     pointsToWin = 5
     if 'pointsToWin' in result['results'][0]:
          pointsToWin = result['results'][0]['pointsToWin']

     pageUrl = ""
     if 'pageUrl' in result['results'][0]:
          pageUrl = result['results'][0]['pageUrl']

     pageTime = 0
     if 'pageTime' in result['results'][0]:
          pageTime = result['results'][0]['pageTime']
          
     randomized = False
     if 'randomized' in result['results'][0]:
          randomized = result['results'][0]['randomized']

     return render_template('handsontest.html',
                            data=json.dumps(result['results'][0]['questionData2']),
                            roomNumber=result['results'][0]['roomNumber'],
                            roomname=result['results'][0]['roomName'],
                            pointsToWin=pointsToWin,
                            randomized=randomized,
                            pageUrl=pageUrl,
                            pageTime=pageTime,
                            objectId=tableid,
                            unescapedUsername='foobar')

def strEmpty(str):
     return (str is None) or (str.isspace()) or (len(str) == 0)

@app.route('/json/save.json', methods = ['POST'])
def handsonsave():
     print request.form
     dat = json.loads(request.form['data'])
     roomNumber = request.form['roomNumber']
     objectId = request.form['objectId']
     username = session['username']
     pageUrl = request.form['pageUrl']
     pageTime = request.form['pageTime']
     randomized = request.form['randomized'] == 'true'
     cleandata = []
     pointsToWin = 5
     try:
          pointsToWin = int(request.form['pointsToWin'])
     except Exception:
          pointsToWin = 5
          
     for i in range(0, len(dat)):
          if strEmpty(dat[i][1]): continue
          cleanrow = [dat[i][0], dat[i][1]]
          for j in range(2, len(dat[i])):
               if(not(strEmpty(dat[i][j]))): cleanrow.append(dat[i][j])
          if(len(cleanrow) < 3): continue
          cleandata.append(cleanrow)
     if len(objectId) == 0:
          counter = increment_counter()
          connection = httplib.HTTPSConnection('api.parse.com', 443)
          connection.connect()
          connection.request('POST', '/1/classes/GameScore', json.dumps({
               "questionData2": cleandata,
               "username": username,
               "roomName": request.form['roomName'],
               "roomNumber":counter,
               "randomized": randomized,
               "pointsToWin": pointsToWin,
               "pageUrl": pageUrl,
               "pageTime": pageTime
          }), {
               "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
               "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK",
               "Content-Type": "application/json"
          })
          raw = json.loads(connection.getresponse().read())
          raw['roomNumber']=counter
          return json.dumps(raw)
     else:
          connection = httplib.HTTPSConnection('api.parse.com', 443)
          connection.connect()
          connection.request('PUT', '/1/classes/GameScore/'+objectId, json.dumps({
               "questionData2": cleandata,
               "roomName": request.form['roomName'],
               "randomized": randomized,
               "pointsToWin": pointsToWin,
               "pageUrl": pageUrl,
               "pageTime": pageTime

          }), {
               "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
               "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK",
               "Content-Type": "application/json"
          })
          raw = connection.getresponse().read()
          return raw

@app.route('/newtable', methods=['GET'])
def newtable():
     username = session['username']
     return render_template("handsontest.html",
                            objectId="",
                            roomNumber=-1,
                            pointsToWin=5,
                            data=json.dumps([["what is 1+1","2","7","3","1"]]),
                            unescapedUsername=username)


     
def render_table(username):
     connection = httplib.HTTPSConnection('api.parse.com', 443)
     params = urllib.urlencode({"order":"-createdAt","limit":1,"where":json.dumps({"questionData2":{"$exists":True},"username":username})})
     connection.connect()
     connection.request('GET', '/1/classes/GameScore?%s' % params, '', {
          "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
          "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
     })
     result = json.loads(connection.getresponse().read())
     if len(result['results']) == 0:
          return render_template("handsontest.html",
                                 objectId="",
                                 roomNumber=-1,
                                 pointsToWins=5,
                                 pageUrl="",
                                 randomized=false,
                                 pageTime=0,
                                 data=json.dumps([["what is 1+1","2","7","3","1"]]),
                                 username=json.dumps(username),
                                 unescapedUsername=username)
     filecontents = result['results'][0]['questionData2']
     pointsToWin = 5
     pageUrl = ""
     pageTime = 0
     randomized = false
     
     if 'pointsToWin' in result['results'][0]:
          pointsToWin = result['results'][0]['pointsToWin']

     if 'pageUrl' in result['results'][0]:
          pageUrl = result['results'][0]['pageUrl']

     if 'pageTime' in result['results'][0]:
          pageTime = result['results'][0]['pageTime']

     if 'randomized' in result['results'][0]:
          randomized = result['results'][0]['randomized']


     print "RAND randomized: " + randomized
     return render_template('handsontest.html',
                            roomNumber=result['results'][0]['roomNumber'],
                            objectId=result['results'][0]['objectId'],
                            roomname=result['results'][0]['roomName'],
                            pageUrl=pageUrl,
                            pageTime=pageTime,
                            pointsToWin=pointsToWin,
                            randomized=randomized,
                            data=json.dumps(filecontents),
                            unescapedUsername=username,
                            username=json.dumps(username))

@app.route('/dologin', methods=['POST'])
def dologin():
    username = request.form['username']
    password = request.form['password']
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"username":username,"password":password})
    connection.connect()
    connection.request('GET', '/1/login?%s' % params, '', {
        "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
        "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK"
    })
    result = json.loads(connection.getresponse().read())
    if 'error' in result:
         return result['error']
    session['username'] = username
    return render_list(username)
#    return render_table(username)
        
@app.route('/dosignup', methods=['POST'])
def dosignup():
    username = request.form['usernamesignup']
    email = request.form['emailsignup']
    password = request.form['passwordsignup']
    password2 = request.form['passwordsignup_confirm']
    if password != password2:
        return 'passwords do not match'
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/users', json.dumps({
        "username": username,
        "password": password,
        "email": email
    }), {
        "X-Parse-Application-Id": "yPGzvFZLtw2kKMEWchlYrchGDHucdFaYVaKuLnX4",
        "X-Parse-REST-API-Key": "itEwnIvz7KMatN4bTkxtYzl5EDPixTELbx2UvfnK",
        "Content-Type": "application/json"
    })
    result = json.loads(connection.getresponse().read())
    if 'error' in result:
         return result['error']
    session['username'] = username
    return render_list(username)
#    return render_table(username)




if __name__ == '__main__':
    app.run(debug=True, host=sys.argv[1], port=int(sys.argv[2]))
