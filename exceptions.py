from sqlalchemy.exc import SQLAlchemyError


class SendToDeviceException(SQLAlchemyError):
    pass
