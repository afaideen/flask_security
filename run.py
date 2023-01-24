

#ref
#1. https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

from flask_socketio import SocketIO
from werkzeug.serving import WSGIRequestHandler

from flaskapp import create_app
# from flaskapp import socketio
from threading import Lock
from flask_session import Session

from flaskapp.bg import background_thread
global thread

app = create_app()
thread = None
thread_lock = Lock()
# sess = Session(app)

if __name__ == '__main__':
    # sess.init_app(app)
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)

    # WSGIRequestHandler.protocol_version = "HTTP/1.1"
    # app.run(host="0.0.0.0", debug=True, port=5000)
    # socketio.run(app, debug=False, port=5000, host="0.0.0.0")
    ##use '0.0.0.0' to access the server from external ip
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host="0.0.0.0", port=5000, ssl_context=('mchp_cert_test/cert.pem', 'mchp_cert_test/key.pem'))
    # app.run(host="0.0.0.0",ssl_context='adhoc')
    # app.run(ho192.168.0.101st="127.0.0.1", port=5000)
    # app.run(host="0.0.0.0")
    # app.run(host="0.0.0.0", port=5000)
    # app.run(host="192.168.137.1", port=5000)
