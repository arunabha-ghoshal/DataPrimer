#!/bin/bash





##################################################################################
# Global Name: tpttbuild.sh #
# Job Description: Script to execute tpt tbuild control statements #
# Author: EIS Informatica Adminis #
# Date Created: July 7, 2013 #
##################################################################################
##################################################################################
# Version : 2 #
# Updates : Script update with Directory structure & PAM integration #
# for Password. #
# Author: Bharath KN (ETL PLatform Admin #
# Date Created: June 1, 2020 #
##################################################################################


###########################################################################
# Checking the Start Time #
###########################################################################





export currentTimeStamp=`date '+%Y-%m-%d_%H-%M-%S'`





###########################################################################
# Script Usage #
###########################################################################





if test $# -gt 2
then
{
echo -e "\nUSUAGE: sh tpttbuild.sh <tbuildControlSript> <tbuildLog> \n"
exit 1;
}
fi


###########################################################################
# Checking the script executing user #
###########################################################################





if [ `whoami` != "talend" ];
then
{
echo -e "\nThis script should execute through talend user only\n"
exit 1
}
fi


###########################################################################
# Generating the tpttbuild.sh log ($tptExecutionLog) #
###########################################################################





export object=`echo $1 | awk -F'.' '{print $1}'`
export tptRootDir=/TalendData/Teradata
export tptExecutionLog=$tptRootDir/LogFiles/tptexecution.log
export TPTCheckpointDir=/TalendData/${2}/checkpoint
export TPTParameter=/TalendData/Teradata/config/tptparameter.txt
export TPTParameterFile=/TalendData/Teradata/config/${object}_$currentTimeStamp
export TPTLogDir=/TalendData/${2}/LogFiles
export TPTCTL=/TalendData/${2}/ctlFiles/$1
echo $currentTimeStamp ${object} - $1 $2 >> $tptExecutionLog





###########################################################################
# Fetch Credentials from PAM - Parameter File generation #
###########################################################################





. /TalendData/Teradata/Scripts/generateTPTParameterFile.sh
if [ $? != 0 ];
then
echo "TPTParameterFile generation Failure"
exit 4;
fi

##################################################################3##########################################################
# Checkpoint Processing (including Time-driven, User-driven, and Operator-driven checkpoints) and Removing Checkpoint Files #
#############################################################################################################################





if [ -f $TPTCheckpointDir/${object}* ]; then
echo "$currentTimeStamp ${object} :Checkpoint file found and deleted " >> $tptExecutionLog
rm $TPTCheckpointDir/${object}*
fi





###########################################################################
# tbuild control script invocation #
###########################################################################





tbuild -v $TPTParameterFile -r $TPTCheckpointDir -L $TPTLogDir -f $TPTCTL -j ${object}
rc=$?


###########################################################################
# Readable tbuild log generation #
###########################################################################





if [ -f $TPTLogDir/${object}*.out ]; then
echo "$currentTimeStamp ${object} :Converting the ${object}.out to ${object}_$currentTimeStamp.log file " >> $tptExecutionLog
tlogview -l $TPTLogDir/${object}*.out > $TPTLogDir/${object}_$currentTimeStamp.log





if [ -f $TPTLogDir/${object}_$currentTimeStamp.log ]; then
echo "$currentTimeStamp ${object} :Removed the ${object}.out file " >> $tptExecutionLog
rm $TPTLogDir/${object}*.out
chmod 775 $TPTLogDir/${object}_$currentTimeStamp.log
echo "$currentTimeStamp ${object} :Cleanup older log Files" >> $tptExecutionLog
ls -lhtr "${TPTLogDir}/${object}"* | awk '{ print $NF}' | head -n -7 | while read file;do echo "Deleting File: $file";rm $file;done;
echo "$currentTimeStamp ${object} :Cleanup completed " >> $tptExecutionLog
echo "$currentTimeStamp ${object} : Removing TPTParameterFile" >> $tptExecutionLog
rm $TPTParameterFile;
fi
fi





exit $rc



