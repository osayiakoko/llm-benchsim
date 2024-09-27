import redis
import json


class RedisCache:
    def __init__(self, host, port):
        """
        Initializes a RedisCache instance with the given host and port.

        Args:
            host (str): The hostname or IP address of the Redis server.
            port (int): The port number of the Redis server.

        Returns:
            None
        """
        self.redis = redis.Redis(host=host, port=port)

    def get(self, key):
        """
        Retrieves a value from the Redis cache by the given key.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            The value associated with the key if it exists, otherwise None.
        """
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key, value, expiration=3600):
        """
        Sets a value in the Redis cache with the given key and expiration time.

        Args:
            key (str): The key to store the value under.
            value (any): The value to store.
            expiration (int, optional): The expiration time in seconds. Defaults to 3600.

        Returns:
            None
        """
        self.redis.setex(key, expiration, json.dumps(value))
