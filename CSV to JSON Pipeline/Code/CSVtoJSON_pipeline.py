# Libraries to schedule the DAG

import datetime as datetime
from datetime import timedelta

# Libraries to build the DAG using Bash and Python Operators

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Pandasrequired to convert CSV to JSOn

import pandas as pd

# print names and save file as JSON

def CSVToJSON():
	df=pd.read_csv("C:\\Users\\Kulraj\\Documents\\GitHub\\Data Engineering with Python\\Writing Files\\Files\\data.csv")
	for i,r in df.iterrows():
		print(r['name'])
	df.to_JSON("C:\\Users\\Kulraj\\Documents\\GitHub\\Apache-Airflow\\CSV to JSON Pipeline\\Files\\fromAirflow.JSON",orient='records')


# specifying arguments passed to DAG()

default_args = {
	'owner':'KSK',
	'start_date': dt.datetime(2021,07,11)
	'retries':1,
	'retry_delay':dt.timedelta(minutes=5)
}


# Creating the DAG

with DAG('MyCSVDAG',
	default_args=default_args,
	schedule_interval = timedelta(minutes=5),
	#'0****',
	) as dag:

