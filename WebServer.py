import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug import secure_filename
import pika

UPLOAD_FOLDER = '/home/rhodin/projects/'
ALLOWED_EXTENSIONS = set(['zip'])

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='render')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# To upload a project
# Project should be in format:
# Zip file should be named <project_name>.zip
# Root directory should be named <project_name>
# .blend file in root directory
@app.route('/upload', methods=['POST'])
def upload_file():
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          rawprojectname = filename.rsplit('.', 1)[0]
          os.system('rm -rf /home/rhodin/projects/%s' % (rawprojectname))
          os.system('unzip -d /home/rhodin/projects /home/rhodin/projects/%s' % (filename))
          os.system('rm /home/rhodin/projects/%s' % (filename))
          os.system('mkdir /home/rhodin/renders/%s' % (rawprojectname))
          return '%s added to database.\n' % (filename)
      return 'Please upload a .zip file containing a Blender project.\n'

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
    return send_file("/home/rhodin/renders/%s/%s.jpg" % (project, frame.zfill(4)),
                     attachment_filename='logo.png',
                     mimetype='image/png')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
