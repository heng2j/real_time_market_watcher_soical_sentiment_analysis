import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 12, 20, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('stop_streaming_jobs_dag',
         catchup=False,
         default_args=default_args,
         # Set for testing purpose to run in every 2 minutes
         schedule_interval='30 16 * * *' ,
         # Should run daily at 11:00 pm
         # schedule_interval='0 30 23 * * ?',
         ) as dag:



    opr_init_msg = BashOperator(task_id='init_msg',
                             bash_command='echo Stopping Streaming_processes!! ')

    opr_kill_kinesis_streams_jobs = BashOperator(task_id='kill_kinesis_streams_jobs',
                             bash_command='cd $stock_sentiment_analysis_PATH && bash kill_streaming_jobs.sh ')

    opr_sleep_5 = BashOperator(
        task_id='sleep_5_secs',
        bash_command='sleep 5')

    opr_stop_kinesis_streams = BashOperator(task_id='stop_kinesis_streams',
                             bash_command='cd $stock_sentiment_analysis_PATH && sh stop_streams.sh ')


opr_init_msg >> opr_kill_kinesis_streams_jobs >> opr_sleep_5 >> opr_stop_kinesis_streams