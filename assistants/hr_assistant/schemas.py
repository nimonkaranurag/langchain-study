from typing import Optional

from pydantic import BaseModel


class Date(BaseModel):
    """
    Represents a date value.
    """

    day: int
    month: int
    year: int

    def __str__(self) -> str:
        return f"{self.day}/{self.month}/{self.year}"


class TimeOffRequest(BaseModel):
    """
    Represents a request for time-off.
    """

    employee_email: str
    start_date: Date
    end_date: Date


class TimeOffResponse(BaseModel):
    """
    Represents the response received when a time-off request is made.
    """

    status: int
