#!/bin/bash


echo 'airflow scheduler PID: ' > airflow_saved_pid.txt
nohup airflow scheduler &
echo $! >> airflow_saved_pid.txt
echo " " >> airflow_saved_pid.txt


echo 'airflow webserver PID: ' >> airflow_saved_pid.txt
nohup airflow webserver &
echo $! >> airflow_saved_pid.txt

