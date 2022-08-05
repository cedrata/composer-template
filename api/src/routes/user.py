from datetime import datetime
from typing import Any, Dict, Final

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from src.core.auth import OAUTH2_SCHEME, hash_password
from src.db.collections.user import User as UserCollection
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage, HttpExceptionMessage
from src.models.user import Role, UserAdminRegistration, UserRegistration
from src.routes.dependencies import require_admin
from src.routes.enums.commons import Endpoint
from src.services.logger.interfaces.i_logger import ILogger

# Router instantiation.
router = APIRouter()

_REGISTER_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: BaseMessage,
    Endpoint.RESPONSES: {
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "User registration for basic user, this will set the default user role to 'user', to let the use chose the roles use the /register-admin endpoint",
}


@router.post(
    "/register",
    response_model=_REGISTER_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_REGISTER_POST_PARAMS[Endpoint.RESPONSES],
    description=_REGISTER_POST_PARAMS[Endpoint.DESCRIPTION],
)
async def register(user_registration: UserRegistration):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username} as username.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=user_registration.password,
        roles=[Role.USER.value],
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.save()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg)
    except Exception as e:
        logger.error("routes", str(e))
        msg = f"An unknown exception occured, maybe bad db connection"
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username} has been succesully added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_REGISTER_ADMIN_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: BaseMessage,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": f"Forbidden access, {Role.ADMIN} role required",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "User registration for basic user, this will set the default user role to 'user', to let the use chose the roles use the /register-admin endpoint",
    Endpoint.DEPENDENCIES: [Depends(require_admin)],
    Endpoint.TAGS: [
        Role.ADMIN.value.capitalize()
    ]
}


@router.post(
    "/register-admin",
    response_model=_REGISTER_ADMIN_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_REGISTER_ADMIN_POST_PARAMS[Endpoint.RESPONSES],
    description=_REGISTER_ADMIN_POST_PARAMS[Endpoint.DESCRIPTION],
    dependencies=_REGISTER_ADMIN_POST_PARAMS[Endpoint.DEPENDENCIES],
    tags=_REGISTER_ADMIN_POST_PARAMS[Endpoint.TAGS]
)
async def register_admin(
    user_registration: UserAdminRegistration, _: str = Depends(OAUTH2_SCHEME)
):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username} as username and roles {user_registration.roles}.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=hash_password(user_registration.password),
        roles=user_registration.roles,
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.save()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg)
    except Exception as e:
        logger.error("routes", str(e))
        msg = f"An unknown exception occured, maybe bad db connection"
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username} and roles {user_registration.roles} has been succesully added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
