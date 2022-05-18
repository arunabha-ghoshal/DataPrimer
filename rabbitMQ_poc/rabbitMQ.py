#all class files for connectivity to Rabbit MQ
#Biswadeep Upadhyay

import pika
import sys
import os
import json



class connectMQ(object):
    def __init__(self,user,passd,host,port):
        self.user = user
        self.passd = passd
        self.host = host
        self.port = port

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.passd )
        if isinstance(self.host,list):
            hostname = self.host[0]
        else:
            hostname = self.host
        parameters = pika.ConnectionParameters(host=hostname, port=self.port, credentials=credentials)
        connection = pika.BlockingConnection(parameters)

        if connection.is_open:
            print('MQ Connection : SUCCESS')
        else:
            print('MQ Connection : FAILED')
            raise Exception('MQ connection could not be establshed. Please check with your MQ broker.')

        return connection

    def setQueue(self,conn,queue_name):
        channel = conn.channel()
        if queue_name == 'SSQE':
            channel.queue_declare(queue=queue_name,durable=True)
        else:
            channel.queue_declare(queue=queue_name,durable=False)

        return channel

    def setExclusiveQueue(self,conn):
        channel = conn.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        exc_queue = result.method.queue

        return channel,exc_queue

    def publishMQ(self,channel_name, queue_name, pub_msg):
        try:
            if isinstance(pub_msg,dict):
                channel_name.basic_publish(exchange='',routing_key=queue_name,body=json.dumps(pub_msg),properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
                return True
            else:
                print('Only JSON message body is accepted.')
                return False
        except Exception as e:
            print(f'Failed to publish message with error : {e}')
            return False

    def receiveMQ(self,channel_name, queue_name, callback_fn,auto_ackn=False):
        channel_name.basic_qos(prefetch_count=1)
        channel_name.basic_consume(queue=queue_name, on_message_callback=callback_fn,auto_ack=auto_ackn)

        print(" [x]  [*] Waiting for messages. To exit press CTRL+C")
        channel_name.start_consuming()
