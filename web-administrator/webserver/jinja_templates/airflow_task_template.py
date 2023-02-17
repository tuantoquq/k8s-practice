@task(task_id="{{indicator_name}}")
def compute_{{indicator_name}}():
    {{indicator_name}}_miner = {{indicator_name_upper}}Miner(input_tables={{input_tables}}, indicator_name="{{indicator_name}}",
                                       recursive_range={{recursive_range}})
    {{indicator_name}}_miner.execute()
    print("{{indicator_name_upper}} Miner executing...")
    return "{{indicator_name_upper}}_MINER"


{{indicator_name}}_task = PythonOperator(task_id="{{indicator_name}}", python_callable=compute_{{indicator_name}}, dag=indicator_dag)