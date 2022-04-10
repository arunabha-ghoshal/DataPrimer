from  clientSCP import SCP
import os
import sys
import json

v_attr_lst = './sample_param.json'
try:
    with open(v_attr_lst,'r') as attr_conf:
        attr_map = json.load(attr_conf)
except Exception as e:
    tb = sys.exc_info()[2]
    lineno = tb.tb_lineno
    print(f'The process failed due to invalid Attribute list config Json: {e}')
    exit(1)  

spark_master = attr_map['spark_master']
spark_app = attr_map['spark_app']
param_attributes = attr_map['arguments']
rdbms = attr_map['rdbms']


exec_mem = attr_map['executor-memory']
driv_mem = attr_map['driver-memory']
num_exec = attr_map['num-executors']
exec_core = attr_map['executor-cores']


create_process = SCP(spark_master,spark_app,rdbms,exec_mem,driv_mem,num_exec,exec_core,param_attributes)

#create_process.display_process()

create_process.executeSCP()

