from demands import HTTPServiceClient

from yolapy.resources import campaign, partner, site, subscription, user


class Yola(
        HTTPServiceClient, campaign.CampaignResourceMixin,
        partner.PartnerResourceMixin, site.SiteResourceMixin,
        subscription.SubscriptionResourceMixin, user.UserResourceMixin):
    """Client for Yola's API.

    ```
    yola = Yola(
        url='https://wl.yola.net/',
        auth=('username', 'password'))

    yola.get_user('user_id')
    ```

    When appropriate, successful responses will return parsed json objects.

    Failures will raise instances of `demands.HTTPServiceError`.

    See [TODO] for available methods with documentation.
    """

    def __init__(self, **kwargs):
        """Initialize with url, auth, and optional headers.

        ```
        Yola(
            url='https://wl.yola.net/',
            auth=('username', 'password'),
            headers={'Header-Name': 'value'})
        ```
        """
        kwargs['send_as_json'] = True
        super(Yola, self).__init__(**kwargs)
