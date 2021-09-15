import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch

# Specifying arguments for DAG
# NOTE: Start Time should be a day before if we want to run the task daily. (Ask Tim why?)

def cleanScooter():
	df=pd.read_csv('scooter.csv')
	df.drop(columns = ["region_id"], inplace=True)
	df.columns = [x.lower() for x in df.columns]
	df['started_at'] = pd.to_datetime(df['started_at'],format = '%m/%d/%Y %H:%M')
	df.to_csv('cleanscooter.csv')


def filterData():
	df = pd.read_csv('cleanscooter.csv')
	fromd='2019-05-23'
	tod='2019-06-03'
	tofrom=df[(df['started_at']>fromd) & (df['started_at']<tod)]
	tofrom.to_csv('may23-june3.csv')


default_args = {
	'owner': 'KJ',
	'start_date' : dt.datetime(2021,9,13),
	'retries' : 1,
	'retry_delay' : dt.timedelta(minutes=5),
}


# Setting up the Python Operators to get data from postgres and put into elasticsearch

with DAG('CleanData',
		default_args=default_args,
		schedule_interval=timedelta(minutes=5),
							# '0****',

		) as dag:

	cleanData = PythonOperator(task_id='clean',
		python_callable=cleanScooter)
	selectData = PythonOperator(task_id='filter',
								python_callable=filterData)

	copyFile = BashOperator(task_id='copy',
										bash_command = 'cp /home/kkohli/may23-june3.csv /home/kkohli/Desktop')

# NOTE: Very imp to make sure you have the correct permissions to access files and folders.
# NOTE: If multiple processes try to touch the same file or the user tries to access the file it can break the pipeline

cleanData >> selectData >> copyFile


getData >> insertData




