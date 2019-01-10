import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 12, 20, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('streaming_jobs_dag',
         catchup=False,
         default_args=default_args,
         # Set for testing purpose to run in every 2 minutes
         schedule_interval='40 5 * * *' ,
         # Should run daily at 11:00 pm
         # schedule_interval='0 30 23 * * ?',
         ) as dag:



    opr_init_msg = BashOperator(task_id='init_msg',
                             bash_command='echo "Streaming_process_Started!!"')

    opr_create_kinesis_streams_shell = BashOperator(task_id='create_kinesis_streams',
                             bash_command='cd $stock_sentiment_analysis_PATH && sh start_streams.sh ')

    opr_sleep_60 = BashOperator(
        task_id='sleep_60_secs',
        bash_command='sleep 60')

    opr_start_kinesis_streams_jobs = BashOperator(task_id='start_kinesis_streams_jobs',
                             bash_command='cd $stock_sentiment_analysis_PATH sh run.sh ')


opr_init_msg >> opr_create_kinesis_streams_shell >> opr_sleep_60 >> opr_start_kinesis_streams_jobs