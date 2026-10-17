# quiz-library

Бібліотека квізів для застосунку `quiz_app`. Застосунок підтягує список із `index.json` і завантажує обрані квізи без перезбирання.

## Структура

```
index.json          генерується скриптом, руками не редагувати
uk/*.json           квізи українською
en/*.json           квізи англійською
scripts/build_index.py
```

## Формат квізу

Файл — JSON-масив питань:

```json
[
  {
    "id": "1",
    "question": "Текст питання?",
    "options": ["A", "B", "C", "D"],
    "correct_index": 0
  }
]
```

- `id` — рядок або число, унікальний у межах файлу
- `question` — непорожній рядок
- `options` — рівно 4 непорожні рядки
- `correct_index` — ціле від 0 до 3

Назва квізу в застосунку береться з імені файлу (`flutter-junior.json` → «Flutter Junior»).

## Додати квіз

1. Поклади файл у папку мови (`uk/`, `en/`). Нова мова: додай її в `LANG_TITLES` у `scripts/build_index.py`.
2. Запусти `python3 scripts/build_index.py`: скрипт перевіряє файли й оновлює `index.json`.
3. Закоміть разом з `index.json`. GitHub Action падає, якщо файл невалідний або індекс застарів.

## Підключення в застосунку

Налаштування, URL репозиторію: `https://raw.githubusercontent.com/MIt9/quiz-library/main`
