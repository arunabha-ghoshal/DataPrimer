import pika
import re
import pandas as pd
from dotenv import load_dotenv
import sys
import os
import json

#loading environment variable
load_dotenv('./.env')

v_mq_user = str(os.getenv('MQUSER'))
v_mq_passd = str(os.getenv('MQPASSD'))
v_mq_hosts = str(os.getenv('MQHOST')).split(',')
v_mq_port = str(os.getenv('MQPORT'))
v_ss_queue = str(os.getenv('QUEUE_STN'))

#print(f'the queue for ss is : {v_ss_queue} and the mq hosts : {v_mq_hosts}')

#establishing MQ connection
credentials = pika.PlainCredentials(v_mq_user, v_mq_passd)
parameters = pika.ConnectionParameters(host=v_mq_hosts[0], port=v_mq_port, credentials=credentials)
connection = pika.BlockingConnection(parameters)

if connection.is_open:
    print('MQ Connection : SUCCESS')
else:
    print('MQ Connection : FAILED')
    raise Exception('MQ connection could not be establshed. Please check with your MQ broker.')


#declaring channel for queue:

channel = connection.channel()
channel.queue_declare(queue='SSQE',durable=True)
message = ' '.join(sys.argv[1:]) or "Hello World"
msg = {"name": message.split(' ')[0],"ve": message.split(' ')[1]}
if isinstance(msg,dict):
    print(f'proceeding with the message : \n {msg}')
    channel.basic_publish(exchange='',routing_key='SSQE',body=json.dumps(msg), properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
    print(" [x] Sent %r" % msg)
else:
    raise Exception('Only json messages are allowed for sending.')


connection.close()

