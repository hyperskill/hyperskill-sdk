from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator

MillisecondsDatetime = Annotated[
    datetime,
    BeforeValidator(lambda v: datetime.fromtimestamp(v / 1000, tz=timezone.utc)),
    AfterValidator(lambda v: int(v.timestamp() * 1000)),
]
