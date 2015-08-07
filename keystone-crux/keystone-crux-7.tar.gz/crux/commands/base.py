import logging

class BaseCommand (object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger('%s.%s' % (
            self.__module__, self.__class__.__name__))

    def find_tenant(self, tenant_name):
        client = self.app.client
        tenants = client.tenants.list()

        res = [x for x in tenants if x.name == args.tenant_name]

        if len(res) == 1:
            return res[0]

        raise KeyError(tenant_name)

    def find_or_create_tenant(self, args):
        client = self.app.client
        tenants = client.tenants.list()

        res = [x for x in tenants if x.name == args.tenant_name]

        if res:
            tenant = res[0]
            self.log.info('using existing tenant %s (%s)',
                     tenant.name, tenant.id)
        else:
            self.log.info('creating new tenant')
            tenant = client.tenants.create(
                args.tenant_name,
                args.tenant_description)
            self.log.info('created tenant %s (%s)',
                          tenant.name, tenant.id)

        return tenant

    def find_or_create_user(self, args, tenant):
        client = self.app.client
        users = client.users.list()

        res = [x for x in users if x.name == args.user_name]

        if res:
            user = res[0]
            self.log.info('using existing user %s (%s)',
                     user.name, user.id)

            if args.update:
                self.log.info('updating enabled=%s for user %s',
                              args.enabled, user.name)
                client.users.update(user, enabled=args.enabled)
                if args.user_email:
                    self.log.info('updating email for user %s',
                                  user.name)
                    client.users.update(user, email=args.user_email)
                if args.password:
                    self.log.info('updating password for user %s',
                                  user.name)
                    client.users.update_password(user, args.password)
        else:
            if not args.password:
                raise CruxException('cannot create a user with an empty '
                                    'password')

            self.log.info('creating new user %s',
                          args.user_name)
            user = client.users.create(
                args.user_name,
                args.password,
                args.user_email,
                tenant.id,
                args.enabled)
            self.log.info('created user %s (%s)',
                          user.name, user.id)

        return user

    def find_or_create_role(self, args):
        client = self.app.client
        roles = client.roles.list()

        res = [x for x in roles if x.name == args.role]

        if res:
            role = res[0]
            self.log.info('using existing role %s (%s)',
                     role.name, role.id)
        else:
            role = client.roles.create(args.role)
            self.log.info('created role %s (%s)',
                          role.name, role.id)

        return role
