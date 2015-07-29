from batchcompute.utils import (partial, add_metaclass, CamelCasedClass)
from batchcompute.utils.jsonizable import Jsonizable
from batchcompute.utils.constants import (STRING, NUMBER, TIME)

class ResourceDescription(Jsonizable):
    '''
    Description class about the task's resource(cpu, memory) needs.
    '''
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'Cpu': int,
        'Memory': int
    }

    def __init__(self, dct={}):
        super(ResourceDescription, self).__init__(dct)
        if 'Cpu' not in self._d:
            self.setproperty('Cpu', 800)
        if 'Memery' not in self._d:
            self.setproperty('Memory', 2000)

    def validate(self):
        pass
ResourceDescription = add_metaclass(ResourceDescription, CamelCasedClass)


class TaskDescription(Jsonizable):
    '''
    Description class for task.

    Task in batchcompute is an unit which deal with the same logic work.
    '''
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'PackageUri': STRING,
        'ProgramName': STRING,
        'ProgramType': STRING,
        'ProgramArguments': STRING,
        'EnvironmentVariables': dict,
        'StdoutRedirectPath': STRING,
        'StderrRedirectPath': STRING,
        'ResourceDescription': (ResourceDescription, dict),
        'InstanceCount': NUMBER,
        'Timeout': NUMBER,
        'ImageId': STRING,
        'OssMapping': dict,
        'OssMappingLock': bool,
        'OssMappingLocale': STRING,
    }

    def __init__(self, dct={}):
        super(TaskDescription, self).__init__(dct)
        if 'ProgramType' not in self._d:
            self.setproperty('ProgramType', 'python')
        if 'InstanceCount' not in self._d:
            self.setproperty('InstanceCount', 1)
        if 'EnvironmentVariables' not in self._d:
            self.setproperty('EnvironmentVariables', dict())
        if 'ResourceDescription' not in self._d:
            self.setproperty('ResourceDescription', ResourceDescription())

    def setproperty(self, key, value):
        super_set = super(TaskDescription, self).setproperty
        if key == 'ResourceDescription' and isinstance(value, dict):
            new_value = ResourceDescription(value)
        elif key == 'EnvironmentVariables':
            for env in value:
                if not isinstance(value[env], STRING):
                    value[env] = str(value[env])
            new_value = value
        else:
            new_value = value
        super_set(key, new_value)

    def validate(self):
        pass
TaskDescription = add_metaclass(TaskDescription, CamelCasedClass)


class TaskDag(Jsonizable):
    '''
    Description class for TaskDag.

    TaskDag in batchcompute descripts the tasks and dependencies between each
    other.
    '''
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'TaskDescMap': dict,
        'Dependencies': dict,
    }

    def __init__(self, dct={}):
        super(TaskDag, self).__init__(dct)
        if 'TaskDescMap' not in self._d:
            self.setproperty('TaskDescMap', dict())
        if 'Dependencies' not in self._d:
            self.setproperty('Dependencies', dict())

    def setproperty(self, key, value):
        super_set = super(TaskDag, self).setproperty
        if key == 'TaskDescMap':
            for task_name in value:
                value[task_name] = self._validate_task(value[task_name])
        super_set(key, value)

    def _validate_task(self, task):
        return task if isinstance(task, TaskDescription) else TaskDescription(task)

    def add_task(self, task_name, task):
        if not task_name and not isinstance(task_name, STRING):
            raise TypeError('''Task name must be str and can't be empty ''')
        self._d['TaskDescMap'][task_name] = self._validate_task(task)

    def delete_task(self, task_name):
        if task_name in self._d['TaskDescMap']:
            del self._d['TaskDescMap'][task_name]
        else:
            pass

    def get_task(self, task_name):
        if task_name in self._d['TaskDescMap']:
            return self._d['TaskDescMap'][task_name]
        else:
            raise KeyError('\'%s\'' % task_name)

    def validate(self):
        pass
TaskDag = add_metaclass(TaskDag, CamelCasedClass)


class JobDescription(Jsonizable):
    '''
    Description class for BatchCompute job.

    Job in BatchCompute descripts the batch task.
    '''
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'JobName': STRING,
        'JobTag': STRING,
        'ZoneId': STRING,
        'Priority': int,
        'Description': STRING,
        'TaskDag': (dict, TaskDag)
    }

    def __init__(self, dct={}):
        super(JobDescription, self).__init__(dct)
        if 'JobTag' not in self._d:
            self.setproperty('JobTag', 'Batchcompute')

    def setproperty(self, key, value):
        super_set = super(JobDescription, self).setproperty
        if key == 'TaskDag' and isinstance(value, dict):
            new_value = TaskDag(value)
        else:
            new_value = value
        super_set(key, new_value)

    def validate():
        for key in self.descriptor_map:
            if not self._d.get(key, None):
                raise ValidationError(key)
JobDescription = add_metaclass(JobDescription, CamelCasedClass)
