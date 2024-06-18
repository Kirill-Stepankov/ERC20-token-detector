class ApplicationException(Exception):
    pass


class ContractDoesNotExistException(ApplicationException):
    pass


class InvalidContractAddressException(ApplicationException):
    pass


class ContractIsAlreadyUploadedException(ApplicationException):
    pass


class InvalidSourceCodeException(ApplicationException):
    pass


class CompilationProcessException(ApplicationException):
    pass


class AlreadyProcessedException(ApplicationException):
    pass
