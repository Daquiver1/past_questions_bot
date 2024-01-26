# """Dependency for authentication."""


# # Standard library imports
# import logging
# from typing import Union

# # Third party imports
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer

# from src.core.config import CLIENT_ID, SECRET_KEY

# # from src.db.repositories.users import UsersRepository
# from src.services.auth import AuthService

# auth_service = AuthService()
# logger = logging.getLogger(__name__)

# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="api/authenticate-client/", scheme_name="JWT"
# )


# async def get_client_from_token(
#     # *,
#     token: str = Depends(reuseable_oauth),
# ) -> Union[str, None]:
#     """Get user token."""
#     try:
#         client_id = auth_service.get_data_from_token(
#             token=token, secret_key=str(SECRET_KEY)
#         )
#     except Exception:
#         raise
#     return client_id


# def get_current_active_client(
#     current_user_id: str = Depends(get_client_from_token),
# ) -> str:
#     """Get current active user from token."""
#     if current_user_id != CLIENT_ID:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="No authenticated user.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return current_user_id
