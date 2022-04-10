#!/bin/bash

cd /Talend/Cloud/latest/TalendJobServersFiles/jobexecutions/logs

job_name = $1

grep -r "$job_name" | awk -F'/' '{print $1}' | sort -u