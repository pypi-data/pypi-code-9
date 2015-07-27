


class Device(object):

    def __init__(self, client, device_id):
        self.client = client
        self.device_id = device_id


    def set_zone(self, zone_id, state):
        """
        set_zone(zone_id, state)

        Turn on or off a zone. When specifing a zone, keep in
        mind they are zero based, so to turn on zone 1 you'd want
        to specify 0 for the first parameter.

        > lc = LonoClient(client_id="...", ...) # etc...
        # ** connect to lono cloud **
        > lc.get_device("device id").set_zone(0, true)
        """
        return self.client.query_device(self.device_id, {
            "url": "zones/{0}/{1}".format(zone_id, state and "on" or "off"),
            "method": "post"
        })


    def set_led(self, mode="off", color=None, brightness=255, interval=None, times=None):
        """
        set_zone(zone_id, state)

        Turn on or off a zone. When specifing a zone, keep in
        mind they are zero based, so to turn on zone 1 you'd want
        to specify 0 for the first parameter.

        > lc = LonoClient(client_id="...", ...) # etc...
        # ** connect to lono cloud **
        > lc.get_device("device id").set_zone(0, true)
        """
        return self.client.query_device(self.device_id, {
            "url": "state",
            "method": "post",
            "body": {
                "color": color,
                "mode": mode,
                "brightness": brightness,
                "interval": interval,
                "times": times,
            }
        })
