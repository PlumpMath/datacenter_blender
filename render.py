#!/usr/bin/env python
import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='webserver.local'))
channel = connection.channel()

channel.queue_declare(queue='render')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    bodylist = body.split()
    project = bodylist[0]
    frame = bodylist[1]
    os.system("/usr/bin/rsync -r webserver.local:~/projects/%s ~/%s" % (project, project))
    os.system("/usr/bin/blender -b /home/rhodin/projects/%s/%s.blend -o /home/rhodin/renders/%s/ -F JPEG -x %s -f %s" % (project,project,project,frame,frame))
    os.system("/usr/bin/scp /home/rhodin/renders/%s/%s webserver.local:/home/rhodin/renders/%s/" % (project, frame.zfill(4), project))

channel.basic_consume(callback,
                      queue='render',
                      no_ack=True)

channel.start_consuming()
