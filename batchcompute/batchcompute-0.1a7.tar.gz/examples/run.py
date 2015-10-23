#encoding=utf-8
import sys
import time

from batchcompute import (
    Client, ClientError, CN_QINGDAO, JobDescription, TaskDescription, TaskDag
)

IMAGE_ID = 'img-00000000558D1D5A000079FA0000001F' #这里填写您的BatchCompute镜像
ENDPOINT = CN_QINGDAO  # 这里填写region
ACCESS_KEY_ID = 'to4EvA0jcsHBI1aj' # 'your AccessKeyId'  这里填写您的AccessKeyId
ACCESS_KEY_SECRET = 'BUPG8izU7JSz6BlW0uyFX6RPBPXbCe' # 'your AccessKeySecret'  这里填写您的AccessKeySecret
WORKER_PATH = 'oss://annoroad-test/find-prime/worker.tar.gz' # 'oss://your-bucket/find-prime/worker.tar.gz'  这里填写您上传的worker.tar.gz的OSS存储路径
LOG_PATH = 'oss://annoroad-test/find-prime/logs'  # 'oss://your-bucket/find-prime/logs' 这里填写您创建的错误反馈和task输出的OSS存储路径

def get_job_desc():
    job_desc = JobDescription()
    find_task = TaskDescription()

    find_task.PackageUri = WORKER_PATH
    find_task.ProgramName = 'Find.py'
    find_task.ProgramType = 'python'
    find_task.ImageId = IMAGE_ID
    find_task.InstanceCount = 3
    find_task.Timeout = 3000
    find_task.StdoutRedirectPath = LOG_PATH
    find_task.StderrRedirectPath = LOG_PATH

    sort_task = TaskDescription(find_task)
    sort_task.ProgramName = 'Sort.py'
    sort_task.InstanceCount = 1

    task_dag = TaskDag()
    task_dag.add_task(task_name='Find', task=find_task)
    task_dag.add_task(task_name='Sort', task=sort_task)
    task_dag.Dependencies = {
        'Find': ['Sort']
    }

    job_desc.TaskDag = task_dag
    job_desc.JobName = 'PythonSDK_demo'
    job_desc.Priority = 1
    return job_desc

def main():
    client = Client(ENDPOINT, ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    job_desc = get_job_desc()
    
    job = client.create_job(job_desc)

    t = 10
    print('Sleep %s second, please wait.' % t)
    time.sleep(t)

    # Wait for job terminated.
    while(True):
        s = client.get_job(job)
        if s.State in ['Waiting', 'Running']:
            print('Job %s is now %s' % (job, s.State))
            time.sleep(3)
            continue
        else:
            # 'Failed', 'Stopped', 'Finished'
            print('Job %s is now %s' % (job, s.State))
            break

if __name__ == '__main__':
    sys.exit(main())
