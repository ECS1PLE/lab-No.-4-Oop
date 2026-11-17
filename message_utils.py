def split_message(text: str, limit: int = 4000) -> list[str]:
    if limit < 2:
        raise ValueError("Лимит сообщения должен быть не меньше 2.")

    parts = []
    for i in range(0, len(text), limit):
        parts.append(text[i:i + limit])
    return parts
