from flaskapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    ##use '0.0.0.0' to access the server from external ip
    # app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host="127.0.0.1", port=5000)
    # app.run(host="0.0.0.0")
    # app.run(host="0.0.0.0", port=5000)
    # app.run(host="192.168.137.1", port=5000)
