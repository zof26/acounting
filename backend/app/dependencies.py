from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
# from app.core.security import get_current_user, get_current_active_user, get_superuser
# from app.models.user import User 

# Database session dependency
DBSession = Annotated[Session, Depends(get_session)]

# Auth-related placeholders
# CurrentUser = Annotated[User, Depends(get_current_user)]
# ActiveUser = Annotated[User, Depends(get_current_active_user)]
# SuperUser = Annotated[User, Depends(get_superuser)]

# Example permission checker (stubbed)
def verify_access():
    # Raise if unauthorized
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )
