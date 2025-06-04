from fastapi import status, HTTPException


class AppBaseException(HTTPException):
    pass




InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Wrong or expired token'
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User with this username already exists'
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found'
)


IncorrectPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Wrong password'
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Do not have permission to perform this action'
)

LinkNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Link not found or expired'
)






