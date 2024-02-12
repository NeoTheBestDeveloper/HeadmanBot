from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.poll_attendance.callback_data import UpdateAllAttendancesCallbackData, UpdateAttendanceCallbackData
from src.modules.attendance.domain import Attendance, VisitStatus

__all__ = [
    "update_attendance_buttons",
]


def update_attendance_buttons(attendance_noted: bool, attendances: Iterable[Attendance], timezone: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    day_of_poll = datetime.now(tz=ZoneInfo("UTC")).date()
    for attendance in attendances:
        start_time = convert_time_from_utc(attendance.lesson.start_time, timezone)
        if attendance_noted:
            if attendance.status == VisitStatus.ABSENT:
                builder.button(
                    text=f"❌ Не посещу {start_time:%H:%M} {attendance.lesson.name}",
                    callback_data=UpdateAttendanceCallbackData(
                        attendance_id=attendance.id,
                        new_status=VisitStatus.PRESENT,
                        day_of_poll=day_of_poll,
                    ),
                )
            else:
                builder.button(
                    text=f"✅ Посещу {start_time:%H:%M} {attendance.lesson.name}",
                    callback_data=UpdateAttendanceCallbackData(
                        attendance_id=attendance.id,
                        new_status=VisitStatus.ABSENT,
                        day_of_poll=day_of_poll,
                    ),
                )
        else:
            builder.button(
                text=f"🤷 Неизвестно {start_time.strftime('%H:%M')} {attendance.lesson.name}",
                callback_data=UpdateAttendanceCallbackData(attendance_id=attendance.id, new_status=VisitStatus.PRESENT,
                                                           day_of_poll=day_of_poll,
),
            )

    builder.button(
        text="Буду на всех",
        callback_data=UpdateAllAttendancesCallbackData(new_status=VisitStatus.PRESENT,
                                                       day_of_poll=day_of_poll,
                                                       ),
    )
    builder.button(
        text="Меня сегодня не будет",
        callback_data=UpdateAllAttendancesCallbackData(new_status=VisitStatus.ABSENT,
                                                       day_of_poll=day_of_poll,
                                                       ),
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
