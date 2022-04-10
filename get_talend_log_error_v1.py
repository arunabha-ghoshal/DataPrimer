from datetime import datetime
import subprocess as sp
import os
import time
import glob
import json
from subprocess import Popen, PIPE
import sys
sys.path.append("/hadoopData/global_shared/hifi/python")
from utilities.exeCmd import *
from utilities.logger_module import *
from py4j.protocol import Py4JJavaError
from sys import argv
import re


print('Import Success')
v_job_name = argv[1]

v_zeke_log_dir="/TalendData/ZEKE/log/"
v_tmc_log_dir = "/Talend/Cloud/latest/TalendJobServersFiles/jobexecutions/logs/"
v_username = "bupadhy"

def getRunServer(remoteEngID):
    if remoteEngID == "0f42c868-e8c3-4d5b-b448-71afb0d0e768":
        v_remote_server = "lxapptalprd001"
    elif remoteEngID == "04cfd8e6-5434-4ed1-99f3-d3a11e93d3e5":
        v_remote_server = "lxapptalprd002"
    elif remoteEngID == "2518fc9e-8ec3-41ce-88be-82ba8a255c7e":
        v_remote_server = "lxapptalprd003"
    elif remoteEngID == "f60a3fe1-3759-4a83-9280-78e2c9e993b1":
        v_remote_server = "lxapptalprd004"
    elif remoteEngID == "34328dd8-37b8-43d9-b258-9f8a99ab7e84":
        v_remote_server = "lxapptalprd005"
    elif remoteEngID == "8a030dd0-4c2d-4cea-8a2d-67fab1bee1be":
        v_remote_server = "lxapptalprd006"
    elif remoteEngID == "cf563eb3-eb46-457a-b5f8-99410227125e":
        v_remote_server = "lxapptalprd007"
    elif remoteEngID == "250d36b4-00ec-4731-82e6-682818bfcd4a":
        v_remote_server = "lxapptalprd008"
    elif remoteEngID == "c7b17156-d0b6-46d0-be29-138538b5e078":
        v_remote_server = "lxapptalprd009"
    elif remoteEngID == "2599debd-073f-41b3-87a9-e02d1c63a7a6":
        v_remote_server = "lxapptalprd010"
    elif remoteEngID == "c9877d3e-2801-4f70-b30c-8d2f6ebfae12":
        v_remote_server = "lxapptalprd011"
    elif remoteEngID == "76eef063-264d-4f6c-8c65-327b65f1fca4":
        v_remote_server = "lxapptalprd012"
    elif remoteEngID == "ca11a5d1-ae72-4d74-9997-a0b98bf5e5b4":
        v_remote_server = "lxbdiedgeprd001"
    elif remoteEngID == "705ec7bc-586c-4d9f-b251-f197cee0c072":
        v_remote_server = "lxbdiedgeprd002"
    elif remoteEngID == "3763d9a2-2d66-49f5-ac14-7fc5f8a582a7":
        v_remote_server = "lxbdiedgeprd003"
    else:
        print("UNKNOWN Remote Engine.")
        sys.exit(1)
    return v_remote_server


def jobType(jobName):
    jtype_ident = str(jobName).split('_')[0]
    td_iden = str(jobName).split('_')[1][:3]
    if td_iden == 'ITW':
        td_res = 'Teradata - WS'
    elif td_iden == 'ITS':
        td_res = 'Teradata - SA'
    else:
        td_res = 'Non TD'
    #print(f"Job Type Identifier: {jtype_ident}")
    if jtype_ident == "JM":
        return jtype_ident,f"Talend Standarad Job - {td_res}"
    elif jtype_ident == "JMH":
        return jtype_ident,f"Talend Big Data Job - {td_res}"
    elif jtype_ident == "ITW":
        return jtype_ident,"Talend triggered Teradata Job for : WS"
    elif jtype_ident == "ITS":
        return jtype_ident,"Talend triggered Teradata Job for : SA"
    else:
        return jtype_ident,"I have no idea as of now. Meet me at decade's end."

def getJobRunTime(jobName,ls_jobname):
    str_jn = ''
    jobpath = v_zeke_log_dir + jobName
    #print(jobpath)
    #print(len(jobpath)+1)
    #print(ls_jobname)
    #run_time_list = [s for s in ls_jobname if s not in jobName[:-4]]
    #run_time_str = str_jn.join(run_time_list)
    return ls_jobname[:-4][len(jobpath)+1:]


def getErrLogDir(jobName,jobRunTime,remoteServer,userName):
    l_run_time = jobRunTime.split('_')[0].split('-')
    s_run_time = l_run_time[2] + l_run_time[0] + l_run_time[1]
    #print ("String JobRunTime Value: ",s_run_time)
    tmc_log_dir = "/" + v_tmc_log_dir.strip("/")
    shell_cmd = "ssh " + userName + "@" + remoteServer + ' grep -rnw "' + tmc_log_dir + '" -e "' + jobName + '"  | awk -F' + "'/' '{print $8}' | sort -u"
    #print("Command to execute : ",shell_cmd)
    shell_cmd_exec = executeCmd(shell_cmd)
    if shell_cmd_exec.execute():
        if shell_cmd_exec.getcommandoutput():
            log_out = shell_cmd_exec.getcommandoutput()
        else:
            log_out = shell_cmd_exec.getcommanderror()
    else:
        ("ERROR in log dir retrieval.")
        sys.exit(1)
    l_log_dir = log_out.split('\n')

    l_curr_log_dir = [i for i in l_log_dir if i[:8] == s_run_time]

    l_curr_log_dir.sort(key=lambda x:x[:14])

    return l_curr_log_dir[-1]


from datetime import datetime
import ast
startTime = datetime.now().strftime("%Y%m%d_%H%M%S")
now = time.time()


old_print = print
def timestamped_print(*args, **kwargs):
    logTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    printheader = logTime + " " + "Talend" + " " + "Log Scraper" + " - "
    old_print(printheader, *args, **kwargs)
print = timestamped_print


print(f"The Input Zeke Job Name : {str(v_job_name).strip()}")

get_job_cmd="ls -lrth /TalendData/ZEKE/log/*" + str(v_job_name).strip() + "* | tail -1 | awk -F' ' '{print $9}'"


get_job_cmd_exec = executeCmd(get_job_cmd)

if get_job_cmd_exec.execute():
    if get_job_cmd_exec.getcommandoutput():
        log_out = get_job_cmd_exec.getcommandoutput()
        #print(f"log out from the successful completion of get_job_cmd_exec: {log_out}")
        v_job_name = log_out.split('/')[4].split('-')[0]
    else:
        log_out = get_job_cmd_exec.getcommanderror()
        print(f"error out from the successful completion of get_job_cmd_exec: {log_out}")
else:
    if get_job_cmd_exec.getcommandoutput():
        log_out = get_job_cmd_exec.getcommandoutput()
        print(f"log out from the failed get_job_cmd_exec: {log_out}")
    else:
        log_out = get_job_cmd_exec.getcommanderror()
        print(f"error out from the failed get_job_cmd_exec: {log_out}")


v_job_type = jobType(str(v_job_name).strip())[1]
print(f"The Talend Job Name: {v_job_name}")
print(f"Job Type: {v_job_type}")
v_latest_run_time = getJobRunTime(v_job_name,log_out)
print(f"The latest Talend Job Run time: {v_latest_run_time}")

print(f"Capturing the Remote Engine ID from zeke log for the latest run of the job: {v_job_name}")

get_remote_id_cmd = "cat " + log_out + " | grep 'remoteEngineId' | head -1 | awk -F',' '{print $11}' | awk -F':' '{print $2}'"

get_remote_id_cmd_exec = executeCmd(get_remote_id_cmd)

if get_remote_id_cmd_exec.execute():
    if get_remote_id_cmd_exec.getcommandoutput():
        log_out = get_remote_id_cmd_exec.getcommandoutput()
        #print(f"log out from the successful completion of get_remote_id_cmd_exec: {log_out}")
        v_remote_id = str(log_out).strip().strip('"')
    else:
        log_out = get_remote_id_cmd_exec.getcommanderror()
        print(f"error out from the successful completion of get_remote_id_cmd_exec: {log_out}")
else:
    if get_remote_id_cmd_exec.getcommandoutput():
        log_out = get_remote_id_cmd_exec.getcommandoutput()
        print(f"log out from the failed get_job_cmd_exec: {log_out}")
    else:
        log_out = get_remote_id_cmd_exec.getcommanderror()
        print(f"error out from the failed get_job_cmd_exec: {log_out}")


print(f"The last Remote Engine ID where the Job has run : {v_remote_id}")

v_job_run_server = getRunServer(v_remote_id)
print(f"The latest job run server: {v_job_run_server}")


v_list_logDir = getErrLogDir(v_job_name,v_latest_run_time,v_job_run_server,v_username)

print(f"Latest Job Run Log Directory : {v_list_logDir}")



err_capture_cmd = "ssh " + v_username + "@" + v_job_run_server + " cat " + v_tmc_log_dir + v_list_logDir + "/stdOutErr_*.log | grep 'ERROR\|Error\|Failed\|failed'"



#print("The Error Capture Command: ",err_capture_cmd)

err_capture_cmd_exec = executeCmd(err_capture_cmd)

if err_capture_cmd_exec.execute():
    if err_capture_cmd_exec.getcommandoutput():
        print("################################################################################################")
        print("Final Job Status: Failed.")
        print("################################################################################################")
        error_msg = err_capture_cmd_exec.getcommandoutput()
        print("Job Error Message: \n",error_msg)
        print("################################################################################################")
        det_error_cmd = "ssh " + v_username + "@" + v_job_run_server + " cat " + v_tmc_log_dir + v_list_logDir + "/stdOutErr_*.log | tail -40"
        det_error_cmd_exec = executeCmd(det_error_cmd)
        if det_error_cmd_exec.execute():
            if det_error_cmd_exec.getcommandoutput():
                det_error_msg = det_error_cmd_exec.getcommandoutput()
                print("Detailed Error Log:\n ",det_error_msg)

    else:
        print("Final Job Status: Success.")

else:
    print("Final Job Status: Success.")



