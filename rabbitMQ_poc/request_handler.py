#!/usr/bin/env python
#utility : $ python3 request_handler.py <queue_name>

import pika
import re
import pandas as pd
from dotenv import load_dotenv
import sys
import os
import json
import time
from rabbitMQ import connectMQ
from serverSCP import DeploySCP


def main():
    queue_name = sys.argv[1]

    #loading environment variable
    load_dotenv('/hadoopData/platform_services/spark_compute_platform/properties/.env')

    v_mq_user = str(os.getenv('MQUSER'))
    v_mq_passd = str(os.getenv('MQPASSD'))
    v_mq_hosts = str(os.getenv('MQHOST')).split(',')
    v_mq_port = int(os.getenv('MQPORT'))

    print(f'Queue selected : {queue_name}')

    mq = connectMQ(v_mq_user,v_mq_passd,v_mq_hosts,v_mq_port)
    connection = mq.connect()
    channel = mq.setQueue(connection,queue_name)




    def spark_process(conf,choice):
        '''
        v_attr_lst = '/hadoopData/platform_services/spark_compute_platform/properties/prototype_conf.json'
        try:
            with open(v_attr_lst,'r') as attr_conf:
                attr_map = json.load(attr_conf)
        except Exception as e:
            tb = sys.exc_info()[2]
            lineno = tb.tb_lineno
            print(f'The process failed due to invalid Attribute list config Json: {e}')
            exit(1)  
        '''

        if isinstance(conf,dict):
            deploy = DeploySCP.Execute(deploy_type=choice)
            #deploy = DeploySCP.Execute()
            print(deploy.print_deploy_mode())
            spark_submit_command = deploy.prepare_spark_submit(conf)
            print(spark_submit_command)
            return spark_submit_command
        else:
             return 'Process FAILED. Received message body is expected to be JSON.'




    def on_request(ch, method, props, body):
        #json_body = json.loads(str(body.decode()))
        json_body = json.loads(body)
        print(" [x] Received %r" % json_body)
        #print(f" [x] type of message : {type(json_body)}")
        if isinstance(json_body,dict):
            print(f"the name : {json_body['spark_master']}")

        if queue_name == 'SSQE':
            choice = 'standalone'
        elif queue_name == 'HPQE':
            choice = 'yarn'
        else:
            choice = 'k8s'
        response = spark_process(json_body,choice)
        print(" [x] Done")

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    mq.receiveMQ(channel,queue_name,on_request)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted. Shutting down the consumer Daemon.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)