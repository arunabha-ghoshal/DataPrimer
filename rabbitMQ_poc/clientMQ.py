#!/usr/bin/env python
import pika
import uuid
import re
import pandas as pd
from dotenv import load_dotenv
import sys
import os
import json
from rabbitMQ import connectMQ

#loading environment variable
load_dotenv('./.env')



class sendRequest(object):
    def __init__(self,queue_name):
        self.v_mq_user = str(os.getenv('MQUSER'))
        self.v_mq_passd = str(os.getenv('MQPASSD'))
        self.v_mq_hosts = str(os.getenv('MQHOST')).split(',')
        self.v_mq_port = str(os.getenv('MQPORT'))
        self.v_ss_queue = str(queue_name)
        self.connection = connectMQ(self.v_mq_user,self.v_mq_passd,self.v_mq_hosts,self.v_mq_port).connect()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def printQueue(self):
        if self.v_ss_queue == 'unknown':
            print('Invalid Queue selected for processing.')
            return False
        print(f'The queue selected : {self.v_ss_queue} for the mqhost {self.v_mq_hosts}')
        return True

    def callMQ(self, json_body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.v_ss_queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json_body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


'''
class sendRequest(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
'''