class SnmpReply:
    def __init__(self, has_error=False, value='', error=''):
        self.has_error = has_error
        self.value = value
        self.error = error
