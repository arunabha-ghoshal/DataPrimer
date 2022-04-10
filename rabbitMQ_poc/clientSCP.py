from clientMQ import sendRequest
import sys
import os
import json



class SCP(object):
    def __init__(self,deploy_type,spark_app,rdbms,exec_mem,driv_mem,num_exec,exec_core,arguements=None,job_name=None,conf=None):
        self.deploy_type = deploy_type
        self.spark_app = spark_app
        self.arguements = arguements
        self.conf = conf
        self.queues = {
            'standalone' : 'SSQE',
            'yarn' : 'HPQE',
            'k8s' : 'HPK8'
        }
        self.msg_body = {}
        self.queue = self.queues.get(self.deploy_type,'unknown')
        self.mq = sendRequest(self.queue)
        self.job_name = job_name
        self.rdbms = rdbms
        self.exec_mem = exec_mem
        self.driv_mem = driv_mem
        self.num_exec = num_exec
        self.exec_core = exec_core


    def display_process(self):
        if self.mq.printQueue():
            print('SUCCESS')
        else:
            print('FAILED.')


    def executeSCP(self):
        self.msg_body['spark_master'] = self.deploy_type
        self.msg_body['job_name'] = self.job_name
        self.msg_body['spark_app'] = self.spark_app
        self.msg_body['rdbms'] = self.rdbms
        self.msg_body['executor-memory'] = self.exec_mem
        self.msg_body['driver-memory'] = self.driv_mem
        self.msg_body['num-executors'] = self.num_exec
        self.msg_body['executor-cores'] = self.exec_core
        print(" [x] Sending Spark Submit Request: ")
        response = self.mq.callMQ(json.dumps(self.msg_body))
        print(f" [.] Ack : Execution command :  {response.decode()}")


