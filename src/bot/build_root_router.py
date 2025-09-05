from .admin_panel import include_admin_router
from .common import RootRouter
from .headman_panel import include_group_panel_router
from .help import include_help_command_router
from .poll_attendance import include_poll_attendance_router
from .profile import include_profile_router
from .registration import include_registration_router
from .show_attendance import include_show_attendance_router
from .show_schedule import include_show_schedule_router

__all__ = [
    "build_root_router",
]


def build_root_router() -> RootRouter:
    root_router = RootRouter(throttling=True)

    include_registration_router(root_router)
    include_group_panel_router(root_router)
    include_admin_router(root_router)
    include_help_command_router(root_router)
    include_poll_attendance_router(root_router)
    include_profile_router(root_router)
    include_show_schedule_router(root_router)
    include_show_attendance_router(root_router)

    return root_router
