import os
from flask import Flask, request, redirect, url_for, send_file
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='render')

app = Flask(__name__)

# To request a render
@app.route("/render/<project>/<start>/<end>")
def render(project, start, end):
   for i in range(int(start), int(end) + 1):
      info = project + ' ' + str(i)
      channel.basic_publish(exchange='',
                         routing_key='render',
                         body=info) 
   return 'Added frames ' + start + ' to ' + end + ' from project ' + project + '.\n'

# To fetch an image
@app.route('/image/<project>/<frame>')
def image(project, frame):
    return send_file("/home/rhodin/projects/%s/render/%s.jpg" % (project, frame.zfill(4)),
                     attachment_filename='logo.png',
                     mimetype='image/png')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
