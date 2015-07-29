RESOURCE_TMPL = {
    'Cpu': 1200,
    'Memory': 12000 
}

TASK_TMPL = {
    'PackageUri': 'oss://your_bucket/test_path/uploaded_package.tar.gz',
    'ProgramName': 'main_worker.py',
    'ProgramType': 'python',
    'InstanceCount': 1,
    'Timeout': 1000,
    'StdoutRedirectPath': 'oss://your_bucket/log_path',
    'StderrRedirectPath': 'oss://your_bucket/log_path',
    'EnvironmentVariables': {},
    'ImageId': '',
    'ResourceDescription': RESOURCE_TMPL 
}

JOB_TMPL = {
    'JobName': 'test_job',
    'ZoneId': "",
    'JobTag': "batch",
    'TaskDag': {
        'TaskDescMap': {
            'Task1': TASK_TMPL 
        },
        'Dependences': {}
    }
}
