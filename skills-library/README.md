# Skills Library

Локальный индекс скиллов из репозитория [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills).

**1204 скилла** | Обновлено: 2026-03-29

---

## Поиск скиллов

```bash
cd /Users/andrej/Skill_Creator/skills-library

# Поиск по ключевым словам
python3 search.py "legal contract"

# Только безопасные скиллы
python3 search.py "code review" --risk safe

# По категории
python3 search.py --category security

# Ограничить количество результатов
python3 search.py "api" --limit 5
```

## Просмотр полного содержимого скилла

Когда нашёл нужный скилл — смотрим его SKILL.md прямо из репозитория:

```bash
gh api "repos/sickn33/antigravity-awesome-skills/contents/plugins/antigravity-awesome-skills-claude/skills/ИМЯ-СКИЛЛА/SKILL.md" \
  --jq '.content' | base64 -d
```

---

## Категории

| Категория | Скиллов |
|---|---|
| security | 4 |
| game-development | 10 |
| workflow-bundle | 10 |
| granular-workflow-bundle | 16 |
| development | 4 |
| uncategorized | 1139 |

---

## Проверка безопасности скилла

Перед установкой любого скилла (чужого или своего):

```bash
grep -iE "curl|wget|eval\s*\(|exec\s*\(|base64\s*-d|/etc/passwd" путь/к/SKILL.md
```

Если вывод пустой — скилл чист. Если что-то нашло — читать контекст вручную.

---

## Обновление индекса

```bash
gh api "repos/sickn33/antigravity-awesome-skills/contents/data/skills_index.json" \
  --jq '.content' | base64 -d > /Users/andrej/Skill_Creator/skills-library/skills_index.json
```

---

## Файлы

- `skills_index.json` — индекс всех скиллов (id, name, description, category, risk)
- `search.py` — скрипт поиска
