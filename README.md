# Skill Creator

Рабочая директория для разработки собственных скиллов под Claude Code.

---

## Структура

```
Skill_Creator/
├── skills-library/          # Индекс 1204 референсных скиллов + поиск
├── ai-engineering-process/  # Скилл: инженерный процесс с ИИ
└── README.md
```

---

## Библиотека референсов

→ [skills-library/README.md](skills-library/README.md) — поиск, просмотр, проверка безопасности, обновление индекса

---

## Создание нового скилла

### 1. Найти референс
```bash
python3 skills-library/search.py "моя тема"
```

### 2. Минимальная структура скилла

```
my-skill/
└── SKILL.md
```

```markdown
---
name: my-skill
description: Что делает и когда использовать (до 250 символов)
category: uncategorized
risk: safe
---

## Когда использовать
## Когда НЕ использовать
## Инструкции
```

### 3. Установить
```bash
cp -r my-skill/ ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/
```

---

## Готовые скиллы

| Скилл | Описание |
|---|---|
| [ai-engineering-process](ai-engineering-process/) | Research → Design → Plan → Implement с ИИ |

---

## Заметки

- Юрисдикция: **EU / Latvian law**
- `description` не более 250 символов
- Для ручного вызова: `disable-model-invocation: true` в frontmatter
