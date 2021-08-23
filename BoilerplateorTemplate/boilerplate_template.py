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

default_args = {
	'owner': 'paulcrickard',
	'start_date' : dt.datetime(2021,22,8)
	'retries' : 1,
	'retry_delay' : dt.timedelta(minutes=5),
}


# Setting up the Python Operators to get data from postgres and put into elasticsearch

with DAG('MyDBdag',
		default_args=default_args,
		schedule_interval=timedelta(minutes=5),
							# '0****',

		) as dag:

	getData = PythonOperator(task_id='QueryPostgreSQL',
		python_callable=queryPostgresql)
	insertData = PythonOperator(task_id='InsertDataElasticsearch',
								python_callable=insertElasticsearch)

getData >> insertData

def queryPostgresql():
	conn_string="dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
	conn = db.connect(conn_string)
	df = pd.read_sql("select name,city frm users",conn)
	df.to_csv('postgresqldata.csv')
	print("---------Data Saved-------")

def insertElasticsearch():
	es=Elasticsearch()
	df = pd.read_csv('postgresqldata.csv')
	for i,r in df.iterrows():
		doc = r.to_json()
		res = es.index(index = "frompostgresql",
						doc_type="doc", body=doc)
		print(res)


