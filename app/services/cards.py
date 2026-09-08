from app.database.models.cause import Cause


def format_cause_card(cause: Cause) -> str:
    if cause.card is None:
        return (
            f"🔴 <b>{cause.name}</b>\n\n"
            "Карточка пока не заполнена."
        )

    parts = [
        f"🔴 <b>{cause.name}</b>",
    ]

    if cause.card.description:
        parts.append(
            f"\n📋 <b>Описание</b>\n"
            f"{cause.card.description}"
        )

    if cause.card.inspection:
        parts.append(
            f"\n🔍 <b>Проверка</b>\n"
            f"{cause.card.inspection}"
        )

    if cause.card.recommendation:
        parts.append(
            f"\n🛠 <b>Рекомендации</b>\n"
            f"{cause.card.recommendation}"
        )

    return "\n".join(parts)