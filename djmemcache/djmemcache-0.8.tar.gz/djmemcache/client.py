from pymemcache.client.hash import HashClient


class Client(HashClient):
    # this just fixes some API holes between python-memcached and pymemcache
    set_multi = HashClient.set_many
    get_multi = HashClient.get_many
    # delete_multi = HashClient.delete_many

    def disconnect_all(self):
        if not self.use_pooling:
            self.quit()
