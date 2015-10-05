def pocker_env(dict):
    envs = []
    for key, val in dict.iteritems():
      envs.append(unicode(key)) if val is None else envs.append(u"{0}={1}".format(key, val))
    return envs

class FilterModule(object):
     def filters(self):
         return {
             'pocker_env': pocker_env,
          }
