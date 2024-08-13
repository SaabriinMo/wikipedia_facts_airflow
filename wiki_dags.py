from wikipedia_facts_beautiful_soup import get_today_events, desktop_dir 
from airflow.models import DAG
from airflow.models import Variable
from datetime import datetime
from datetime import timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'sabs',
    'depends_on_past': False,
    'email': ['saabriinm123@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2024, 8, 13), # If you set a datetime previous to the curernt date, it will try to backfill
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2024, 10, 18)
}


github_repo_url = Variable.get("git_repo_url")

with DAG(
    dag_id='wiki_url',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['test']
) as dag:
    
    get_wiki_facts = PythonOperator(
        task_id='wiki_data',
        python_callable=get_today_events,
        op_args=['https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today', desktop_dir],
        dag=dag
    )

    add_task = BashOperator(
        task_id='add_files',
        bash_command=f'cd {desktop_dir} && git add .',
        dag=dag)
    commit_task = BashOperator(
        task_id='commit_files',
        bash_command=f'{desktop_dir} && git commit -m "Update date"',
        dag=dag)
    push_task = BashOperator(
        task_id='push_files',
        bash_command=f'{desktop_dir} && git push',
        dag=dag)