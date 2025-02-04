from fastapi import Header, HTTPException, status
from typing import Annotated

def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "secret-pass" : # Remember that even declaring x_token, on header (by default) will be x-token
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden url - Invalid token")