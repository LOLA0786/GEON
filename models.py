from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    hashed_password: str
    account_type: str  # 'free', 'pro', or 'pro_plus'
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
