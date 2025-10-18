from __future__ import annotations

import datetime

from pydantic import BaseModel, model_validator


class Date(BaseModel):
    """
    Represents a date value.
    """

    day: int
    month: int
    year: int

    def __str__(self) -> str:
        return f"{self.day}/{self.month}/{self.year}"

    @model_validator(mode="after")
    def validate_date_time(self) -> "Date":

        try:
            datetime.date(self.year, self.month, self.day)

        except Exception as e:
            raise ValueError(
                f"Invalid date: '{self.day}/{self.month}/{self.year}'\n"
                f"Error: {e}"
            )

        return self


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
