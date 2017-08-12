class MergeException(Exception):
    pass


class MergeTypeDisparity(MergeException):
    pass


class MergeIntoSelfException(MergeException):
    pass
