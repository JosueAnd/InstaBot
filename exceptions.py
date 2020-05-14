class InstaBotException(Exception):
    """
        Base InstaBot exception.
    """

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = 'Message: %s\n' % self.msg
        if self.screen is not None:
            exception_msg += 'Screenshot: available via screen\n'
        if self.stacktrace is not None:
            stacktrace = '\n'.join(self.stacktrace)
            exception_msg += 'Stacktrace:\n%s' % stacktrace
        return exception_msg


class LoginError(InstaBotException):
    """
        Thrown when the user searched for is not found.
    """

    def __init__(self, msg=None, screen=None, stacktrace=None):
        super(LoginError, self).__init__(
            'Login failed, please double check your username and password.', screen, stacktrace)

    def __str__(self):
        return super(LoginError, self).__str__()
