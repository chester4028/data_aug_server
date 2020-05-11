import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from translate_google import any_to_any_translate_back, GoogleToken
from augment_constant import language_short_google
from threading import Thread


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True, ping_timeout=300000, ping_interval=300000)
worker_dict = {}

class Worker(object):
    switch = False

    def __init__(self, socketio, sid):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = True
        self.sid = sid

    def SentenceGenerator(self, sid, sentence):
        aug_sentence = set()
        print("start sentence augment")
        for language_short_google_one in language_short_google:
            if not self.switch :
                break
            text_translate = any_to_any_translate_back(GoogleToken(), sentence, from_='zh-TW', to_=language_short_google_one)
            # print(text_translate)
            aug_sentence.add(text_translate)
            socketio.emit('newsentence', {'sentence': text_translate}, namespace='/sentence', room=sid)
            socketio.sleep(3)
        result = "結束  共" + str(len(aug_sentence)) +"句擴寫"
        socketio.emit('newsentence', {'sentence': result}, namespace='/sentence', room=sid)

    def stop(self):
        """
        stop the loop
        """
        self.switch = False

@socketio.on('connect')
def test_connect():
    global worker_dict
    # worker for each client
    worker_dict[request.sid] = Worker(socketio, request.sid)
    # print( str(request.sid) + ' Client connected')


@socketio.on('close_job', namespace='/sentence')
def close_job():
    worker = worker_dict[request.sid]
    print("get worker : " + worker.sid)
    worker.stop()


@socketio.on('gen_sentence', namespace='/sentence')
def gen_sentence(message):
    sentence = message['sentence']
    print( "get :" + sentence )
    print("Starting Thread")
    worker = worker_dict[request.sid]
    thread = socketio.start_background_task(worker.SentenceGenerator(request.sid, sentence))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
