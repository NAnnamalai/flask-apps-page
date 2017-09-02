#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask
app = Flask(__name__)

#GET REQUEST
@app.route('/')
def homepage():
  return "Hello, you have reached the home page"

#GET REQUEST
@app.route('/getrequest')
def getRequestHello():
  return "Hello, got your GET Request!"

#POST REQUEST
@app.route('/postrequest', methods = ['POST'])
def postRequestHello():
  return "I see you sent a POST message :-)"

#UPDATE REQUEST
@app.route('/updaterequest', methods = ['PUT'])
def updateRequestHello():
  return "Sending Hello on an PUT request!"

#DELETE REQUEST
@app.route('/deleterequest', methods = ['DELETE'])
def deleteRequestHello():
  return "I received a DELETE request!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000)

