import re
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, validator


class Gender(str, Enum):
    """Enum class to enforce usage of pre-defined values for `gender` field."""
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NOT_SPECIFIED = 'NOT_SPECIFIED'


class Listing(str, Enum):
    """Enum class to enforce usage of pre-defined values for `type` field."""
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'


class UserSignup(BaseModel):
    """Class for validating user sign-up data."""
    username: str
    full_name: str | None = None
    email: EmailStr
    password: str
    date_of_birth: str = Field(default=None, example='4-7-2001', description='Date format is in mm-dd-YYYY')
    gender: Gender = Gender.NOT_SPECIFIED

    @validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        """Validator function for checking the date_of_birth constraints."""
        # validate the date format
        try:
            value = datetime.strptime(value, '%m-%d-%Y').replace(tzinfo=timezone.utc)
            # validate the year condition
            if value.year <= 1940:
                raise ValueError('Year must be after 1940')
        except ValueError:
            raise ValueError('Input date must be in mm-dd-YYYY format')
        return value

    
    @validator('password')
    def validate_password(cls, value):
        """Validator function for checking the password constraints."""
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[a-z]', value) or not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase and one lowercase character')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        return value


class UserLogin(BaseModel):
    """Class for validating user login data."""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Class for validating the insertion of a users's updated data."""
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None


class UserView(BaseModel):
    """Class for showing user info."""
    username: str
    full_name: str | None = None
    email: EmailStr
    date_of_birth: datetime | None = None
    gender: Gender
    created_at: datetime
    updated_at: datetime


class ListingAdd(BaseModel):
    """Class for validating the insertion of a listing's data."""
    type: Listing
    available_now: bool = True
    address: str


class ListingUpdate(BaseModel):
    """Class for validating the insertion of a listing's updated data."""
    available_now: bool = True


class ListingView(ListingAdd):
    """
    Class for showing a listing,
    inherits from `ListingAdd`.
    """
    id: str
    created_at: datetime
    updated_at: datetime
