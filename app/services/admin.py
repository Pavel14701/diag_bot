from app.config import get_settings


def is_admin(user_id: int) -> bool:
    settings = get_settings()
    return user_id in settings.admin_id_list