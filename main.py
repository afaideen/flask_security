
###references https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
###Install OpenSSL --> https://thesecmaster.com/procedure-to-install-openssl-on-the-windows-platform/
###Generate self-sign certificate param --> cert and key, use below,
        ###>openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
###Note Self-Signed Certificate is used for development and testing purposes

from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/testing")
def hello():
    return "salam sejahtera..."


if __name__ == "__main__":
    ##use '0.0.0.0' to access the server from external ip
    # app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host="127.0.0.1", port=5000)
    app.run(host="0.0.0.0")
    # app.run(host="0.0.0.0", port=5000)
    # app.run(host="192.168.137.1", port=5000)
