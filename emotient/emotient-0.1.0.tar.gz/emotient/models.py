class Media(object):
    list_url = 'media'

    @staticmethod
    def aggregated_analytics_url(obj_id):
        return 'analytics/{}/aggregate'.format(obj_id)

    @staticmethod
    def analytics_url(obj_id):
        return 'analytics/{}'.format(obj_id)

    @staticmethod
    def instance_url(obj_id):
        return 'media/{}'.format(obj_id)


class Group(object):
    list_url = 'groups'

    @staticmethod
    def aggregated_analytics_url(obj_id):
        return 'analytics/groups/{}/aggregate'.format(obj_id)

    @staticmethod
    def instance_url(obj_id):
        return 'groups/{}'.format(obj_id)


class GroupMedia(Media):
    list_url = 'groups/{}/media'
