#!/usr/bin/env python3
"""Простой классификатор обращений без внешних зависимостей."""

from __future__ import annotations

import argparse
from pathlib import Path


COMPLAINT_MARKERS = (
    "жалоб",
    "очеред",
    "холодн",
    "пропал",
    "не работает",
    "сломал",
    "проблем",
)

INFO_MARKERS = (
    "как получить",
    "где",
    "когда",
    "какие документы",
    "сколько",
)


def classify(message: str) -> str:
    """Вернуть одну из категорий: справка, жалоба или другое."""
    normalized = normalize(message)

    if any(marker in normalized for marker in COMPLAINT_MARKERS):
        return "жалоба"
    if any(marker in normalized for marker in INFO_MARKERS):
        return "справка"
    return "другое"


def draft_reply(message: str, category: str) -> str:
    """Сформировать короткий черновик ответа с учётом темы обращения."""
    normalized = normalize(message)

    if "справк" in normalized and "учеб" in normalized:
        return (
            "Справку о месте учёбы можно заказать в учебном офисе. "
            "Уточните, пожалуйста, нужна электронная или бумажная версия."
        )
    if "столов" in normalized:
        return (
            "Спасибо за сообщение. Передадим информацию об очереди и холодной "
            "еде администрации столовой для проверки."
        )
    if "консультац" in normalized:
        return (
            "Поможем записаться на консультацию. Уточните, пожалуйста, тему "
            "и удобное время завтра."
        )
    if "wi-fi" in normalized or "wifi" in normalized:
        return (
            "Спасибо за сигнал. Передадим заявку технической службе по Wi-Fi "
            "в корпусе B; уточните, пожалуйста, этаж или аудиторию."
        )
    if "парков" in normalized:
        return (
            "Гостевая парковка находится у главного въезда. Для точных указаний "
            "уточните, пожалуйста, к какому корпусу вы направляетесь."
        )

    if category == "жалоба":
        return "Спасибо за сообщение. Уточним детали и передадим обращение ответственному подразделению."
    if category == "справка":
        return "Поможем с информацией. Уточните, пожалуйста, интересующие вас детали."
    return "Спасибо за обращение. Уточните, пожалуйста, детали запроса."


def normalize(message: str) -> str:
    """Нормализовать регистр, букву ё и распространённые варианты дефиса."""
    return (
        message.casefold()
        .replace("ё", "е")
        .replace("‑", "-")
        .replace("–", "-")
        .replace("—", "-")
    )


def read_messages(path: Path) -> list[str]:
    """Прочитать непустые строки файла как отдельные обращения."""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Классификатор обращений")
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("messages.txt"),
        help="путь к файлу с обращениями (по умолчанию messages.txt рядом со скриптом)",
    )
    args = parser.parse_args()

    for number, message in enumerate(read_messages(args.file), start=1):
        category = classify(message)
        reply = draft_reply(message, category)
        print(f"{number}. {message}")
        print(f"   Категория: {category}")
        print(f"   Черновик ответа: {reply}\n")


if __name__ == "__main__":
    main()
