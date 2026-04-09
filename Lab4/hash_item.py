class HashItem:
    def __init__(self, key=None, data=None, value=None, hash_address=None):
        self.key = key
        self.data = data
        self.value = value
        self.hash_address = hash_address
        self.is_deleted = False

    def is_empty(self):
        return self.key is None

    def is_active(self):
        return self.key is not None and not self.is_deleted