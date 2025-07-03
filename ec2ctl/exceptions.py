class Ec2CtlError(Exception):
    """Base exception for ec2ctl."""
    pass

class ConfigError(Ec2CtlError):
    """Raised when there is a config error."""
    pass

class AwsError(Ec2CtlError):
    """Raised when there is an AWS error."""
    pass
