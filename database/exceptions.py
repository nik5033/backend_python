class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserNotExistsException(Exception):
    pass


class DBUserExistsException(Exception):
    pass


class DBMsgNotExistsException(Exception):
    pass
