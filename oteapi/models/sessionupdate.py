"""Pydantic SessionUpdate Data Model.

Note that the Session Object should be updated according to the
SessionUpdate. If the Session already has defined a session_type
and session_id, the code should throw an exception.
"""

from typing import Optional

from pydantic import Field, ValidationError, root_validator, validator

from oteapi.models import AttrDict


class OTESession(AttrDict):
    """Session Update Data Model for returning data from strategies."""

    session_type: Optional[str] = Field(
        None, description="Describe the current session type."
    )
    session_id: Optional[str] = Field(
        None, description="Optional ID for referring to session data."
    )

    @root_validator(pre=True)
    def check_session_assignment(cls, values):
        """Check that session_type is defined if session_id is given."""
        session_id = values.get("session_id")
        session_type = values.get("session_type")
        if session_id is not None and session_type is None:
            raise ValueError(
                "session_id cannot be defined without specifying session_type"
            )
        return values

    @validator("session_id", pre=True)
    def check_session_type_exist(cls, v, values):
        """Check that session_type is defined if session_id set."""
        if v is not None and "session_type" in values:
            raise ValueError(
                "`session_id` cannot be defined without specifying session_type"
            )
        return v

    class Config:
        """enable assignment validation"""

        validate_assignment = True
