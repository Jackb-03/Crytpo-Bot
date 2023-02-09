from flask import Flask, session
import coinspot

app = Flask(__name__)
app.secret_key = "1234dfrbh"

api_key = "630e2b3bb27264b9a9c7f684c701abbe"
api_secret = "U853N9EQ5QA3WLLAPYQEHDGCECPDC2QKQL3BDQA5GN27WD6MJCZTD4F6V1WK3QBQ5L57J7VNYYJCF977"

@app.route("/")
def index():

    response = coinspot.check()
    print(response)
    return "hello"




app.run(debug=True)


