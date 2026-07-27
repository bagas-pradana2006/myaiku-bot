"""
Time Utilities
--------------
Utility untuk konversi waktu UTC dan WIB.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")
WIB = ZoneInfo("Asia/Jakarta")


def now_utc() -> datetime:
    """Mengembalikan waktu UTC saat ini."""

    return datetime.now(UTC)


def now_wib() -> datetime:
    """Mengembalikan waktu WIB saat ini."""

    return datetime.now(WIB)


def wib_to_utc(dt: datetime) -> datetime:
    """Mengubah datetime WIB menjadi UTC."""

    return dt.replace(
        tzinfo=WIB,
    ).astimezone(
        UTC,
    )


def utc_to_wib(dt: datetime) -> datetime:
    """Mengubah datetime UTC menjadi WIB."""

    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=UTC,
        )

    return dt.astimezone(WIB)