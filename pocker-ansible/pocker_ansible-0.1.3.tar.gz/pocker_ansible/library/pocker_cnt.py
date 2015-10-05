#!/usr/bin/python
# encoding: utf-8
import json
import shlex

from pocker import Docker
from pocker.utils import qdict
from pocker.exceptions import PExitNonZero

class _PockerFail(Exception):pass

class GroupManager(object):
    def __init__(self, beacon, count, attach, docker, opts, img, cmd):
        self.beacon = beacon
        self.count = count
        self.docker = docker
        self.opts = opts
        self.img = img
        self.cmd = cmd
        self.attach = attach

        if img:
            img_inspect = self.docker.inspect(self.img).result
            if not img_inspect: #no image on host
                self.docker.pull(self.img)
                img_inspect = self.docker.inspect(self.img).result
            self.img_info = img_info = img_inspect[0]
        else:
            self.img_info = {'Id': None}

        container_conf = beacon, attach, docker, opts, img, cmd, self.img_info['Id']
        #TODO: if name set and count == 1, check if container exists
        containers_list = docker.ps(all=True, filter="label={0}".format(Container.label('_beacon', beacon))).result
        if self.count is None:
            self.count = len(containers_list)
        self.containers = self._get_containers(containers_list, container_conf)

    def _get_containers(self, containers_list, container_conf):
        inspections = []
        if containers_list:
            inspections = self.docker.inspect(*(item['Id'] for item in containers_list)).result
        [inspect.update({'pocker._state': Container.get_state(inspect)}) for inspect in inspections]
        containers = [Container(*container_conf, inspect_data=inspect)
                      for inspect in inspections]
        if len(containers) < self.count:
            containers += [Container(*container_conf, inspect_data={'pocker._state': 'deleted'})
                           for _ in range(0, self.count - len(containers))]
        return containers

    def present(self):
        count = self.count
        to_present, to_absent = self.containers[:count], self.containers[count:]
        for container in to_present:
            if container.state == 'deleted':
                container.created()

        for container in to_absent:
            container.deleted()

    def started(self):
        count = self.count
        to_start, to_stop = self.containers[:count], self.containers[count:]
        for container in to_start:
            container.running()

        for container in to_stop:
            if not (container.state == 'deleted'):
                container.stopped()

    def reloaded(self):
        #TODO: check that beacon was set
        if self.img_info['Id'] is None:
            raise _PockerFail("Container image must be set for state=reloaded")

        count = self.count
        to_reload, to_stop = self.containers[:count], self.containers[count:]
        for container in to_reload:
            if container.need_reload():
                container.deleted()
            container.running()

        for container in to_stop:
            if not (container.state == 'deleted'):
                container.stopped()

    def restarted(self):
        count = self.count
        to_restart, to_stop = self.containers[:count], self.containers[count:]
        for container in to_restart:
            if container.state == 'deleted':
                container.running()
            else:
                container.stopped()
                container.running()

        for container in to_stop:
            if not (container.state == 'deleted'):
                container.stopped()

    def stopped(self):
        count = self.count
        to_stop, _ = self.containers[:count], self.containers[count:]
        #TODO:   ^ - что делать с этими контейнерами?
        for container in to_stop:
            if not (container.state == 'deleted'):
                container.stopped()

    def killed(self):
        count = self.count
        to_kill, _ = self.containers[:count], self.containers[count:]
        #TODO:   ^ - что делать с этими контейнерами?
        for container in to_kill:
            if not (container.state == 'deleted'):
                container.killed()

    def absent(self):
        count = self.count
        to_delete, _ = self.containers[:count], self.containers[count:]
        #TODO:     ^ - что делать с этими контейнерами?
        for container in to_delete:
            container.deleted()

    def paused(self):
        count = self.count
        to_pause, _ = self.containers[:count], self.containers[count:]
        #TODO:    ^ - что делать с этими контейнерами?
        for container in to_pause:
            container.paused()


class Container(object):
    def __init__(self, beacon, attach, docker, opts, img, cmd, img_id, inspect_data):
        self._state = None
        self.changed = False
        #TODO: use name from opts for beacon if exsits?
        self.beacon, self.docker = beacon, docker
        self.attach = attach
        self.opts, self.img = opts, img
        self.cmd, self.inspect_data = cmd, inspect_data
        self.img_id = img_id
        self.state = inspect_data.pop('pocker._state')

        self.goal_signature = self.make_signature(self.opts, {'img_id': img_id,
                                                              'command': self.cmd})

    def _create(self):
        self.add_label('_signature', self.goal_signature)
        self.add_label('_beacon', self.beacon)
        cmd = self.cmd if self.cmd is not None else ''
        cnt_id = self.docker.create(self.img, *shlex.split(cmd), **self.opts).result['Id']
        self.inspect_data = self.docker.inspect(cnt_id).result[0]

    def _start(self):
        self.docker.start(self.id, attach=self.attach)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        states = 'deleted created_or_stopped running paused'.split()
        if not (state in states):
            raise _PockerFail('wrong state: {0} not in {1}'.format(state, states))

        if self._state != state:
            if self._state is not None:
                self.changed = True
            self._state = state


    @property
    def id(self):
        try:
            return self.inspect_data['Id']
        except KeyError:
            return None

    @property
    def present_signature(self):
        try:
            return json.loads(self.inspect_data['Config']['Labels']['pocker._signature'])
        except KeyError:
            return None


    # след. методы переводят контейнер непосредственно заданное состояние
    # т.е. если вызвать stopped для отсутствующего контейнера, то он создасться,
    # запуститься, а затем остановиться
    def created(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state == 'running':
            self.stopped()
            self.deleted()
        if self.state == 'deleted':
            self._create()
        self.state = 'created_or_stopped'

    def stopped(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state == 'running':
            self.docker.stop(self.id)
        if self.state == 'deleted':
            self._create()
            self._start()
            self.docker.stop(self.id)
        self.state = 'created_or_stopped'

    def killed(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state == 'running':
            self.docker.kill(self.id)
        if self.state == 'deleted':
            self._create()
            self._start()
            self.docker.kill(self.id)
        self.state = 'created_or_stopped'

    def running(self):
        if self.state == 'running':
            return
        if self.state == 'paused':
            self.docker.unpause(self.id)
        if self.state == 'created_or_stopped':
            self.docker.start(self.id)
        if self.state == 'deleted':
            self._create()
            self._start()
        self.state == 'running'

    def deleted(self):
        if self.state == 'deleted':
            return
        if self.state == 'paused':
            self.running()
        if self.state == 'running':
            self.stopped()
        if self.state == 'created_or_stopped':
            self.docker.rm(self.id)
        self.state = 'deleted'
        self.inspect_data = {}

    def paused(self):
        if self.state == 'paused':
            return
        if self.state == 'deleted':
            self.running()
        if self.state == 'created_or_stopped':
            self.running()
        if self.state == 'running':
            self.docker.pause(self.id)
        self.state = 'paused'

    def need_reload(self):
        #проверяем совпадают ли "подписи" существующего контейнера и "желаемого"
        return not (self.goal_signature == self.present_signature)

    def add_label(self, name, value):
        opts = self.opts
        label = self.label(name, value)
        if not opts.get('label'):
            opts['label'] = label
        else:
            if isinstance(label, list):
                opts['label'].append(label)
            else:
                opts['label'] = [opts['label'], label]

    @classmethod
    def get_state(cls, inspect_data):
        # deleted, created_or_stopped, paused, running
        if not inspect_data:
            return 'deleted'
        elif inspect_data['State']['Paused']:
            return 'paused'
        elif inspect_data['State']['Running']:
            return 'running'
        else:
            return 'created_or_stopped'

    @classmethod
    def label(cls, name, value):
        return "pocker.{0}={1}".format(name, json.dumps(value))

    @classmethod
    def make_signature(cls, *args):
        signature = {}
        for d in args:
            signature.update(d)
        return signature


def pocker_cnt(params):
    #TODO: use name as beacon if count == 1
    #TODO: check that count == 1 if name set
    p = params = qdict(params)
    docker = Docker(**p.docker_opts)

    manager = GroupManager(p.beacon, p.count, p.attach, docker,
                           p.cnt_opts, p.cnt_img, p.cnt_cmd)
    states = 'present started reloaded restarted stopped killed absent paused'.split()
    if not (p.state in states):
        raise _PockerFail("Unknown state. State must be one of: {0}".format(states))

    getattr(manager, p.state)()

    changed = any([cnt.changed for cnt in manager.containers])

    containers = [str(cnt.id) for cnt in manager.containers if cnt.id]
    if containers:
        facts = docker.inspect(*containers).result
    else:
        facts = []

    #TODO: возвращать что изменилось
    return qdict({'changed': changed, 'facts': facts})

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
            beacon=dict(type='str', required=True),
            count=dict(required=False, default=1),
                # не используем type='int', чтобы можно было передать None
                # если None - применяем операцию ко всем существующим контейнерам
            cnt_opts=dict(type='dict', required=False, default={}),
            cnt_img=dict(type='str', required=False, default=None),
            cnt_cmd=dict(type='str', required=False, default=None),
            attach=dict(type='bool', required=False, default=False),

            #common
            docker_opts=dict(type='dict', required=False, default={}),
        ),
    )

    try:
        result = pocker_cnt(module.params)
        module.exit_json(changed=result.changed, ansible_facts={'containers': result.facts})

    except _PockerFail as e:
        module.fail_json(msg=e.message)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


