from typing import Tuple

from langchain.agents import tool

from assistants.hr_assistant.schemas import (
    Date,
    TimeOffRequest,
    TimeOffResponse,
)


@tool(response_format="content_and_artifact")
def request_time_off(request: TimeOffRequest) -> Tuple[str, TimeOffResponse]:
    """
    Apply for time-off in the provided date range.
    Args:
        employee_email (str): The employee's work email.
        start_date (Date): The starting date for requesting time-off.
        end_date (Date): The ending date for requesting time-off.
    """

    employee_email: str = request.employee_email
    if employee_email != "nimo@ibm.com":
        raise ValueError(
            f"No employee with email: {employee_email} exists, please provide a valid employee email."
        )

    start_date: Date = request.start_date
    end_date: Date = request.end_date

    response_message = (
        f"The time off request for the employee with email: {employee_email} "
        f"has been successfully made for the dates:\n"
        f"{str(start_date)} to {str(end_date)}.\n"
        "Please approach your in-office manager for approval."
    )

    response = TimeOffResponse(
        status=200,
    )

    return (
        response_message,
        response,
    )
