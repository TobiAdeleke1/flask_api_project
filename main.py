from flask import Flask
from orders import orders_pages
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.register_blueprint(orders_pages)



if __name__ == "__main__":
    http_server = WSGIServer(("127.0.0.1", 8000), app)
    http_server.serve_forever()
    