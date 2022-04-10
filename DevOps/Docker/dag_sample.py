from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.models.baseoperator import chain

with DAG('dependencies',
) as dag:

    t0 = DummyOperator(task_id='t0')
    t1 = DummyOperator(task_id='t1')
    t2 = DummyOperator(task_id='t2')
    t3 = DummyOperator(task_id='t3')
    t4 = DummyOperator(task_id='t4')
    t5 = DummyOperator(task_id='t5')
    t6 = DummyOperator(task_id='t6')

    chain(t0, t1, [t2, t3], [t4, t5], t6)

'''new'''
t0 = DummyOperator(task_id='start')

# Start Task Group definition
with TaskGroup(group_id='group1') as tg1:
    t1 = DummyOperator(task_id='task1')
    t2 = DummyOperator(task_id='task2')

    t1 >> t2
    # End Task Group definition

    t3 = DummyOperator(task_id='end')

    # Set Task Group's (tg1) dependencies
    t0 >> tg1 >> t3

'''new'''
import random
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from datetime import datetime
from airflow.utils.trigger_rule import TriggerRule

def return_branch(**kwargs):
    branches = ['branch_0', 'branch_1', 'branch_2']
    return random.choice(branches)

with DAG(dag_id='branch',
start_date=datetime(2021, 1, 1),
max_active_runs=1,
schedule_interval=None,
catchup=False
) as dag:

    #DummyOperators
    start = DummyOperator(task_id='start')
    end = DummyOperator(
    task_id='end',
    trigger_rule=TriggerRule.ONE_SUCCESS
    )

    branching = BranchPythonOperator(
    task_id='branching',
    python_callable=return_branch,
    provide_context=True
    )

    start >> branching

    for i in range(0, 3):
        d = DummyOperator(task_id='branch_{0}'.format(i))
        branching >> d >> end

