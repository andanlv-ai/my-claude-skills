---
name: worktree
description: Создание и управление git worktrees для параллельной работы нескольких Claude в одном проекте. Используй когда пользователь хочет параллельную работу, изолированные изменения или эксперимент с откатом.
allowed-tools: Bash
argument-hint: "[create|list|merge|remove] [name]"
---

# Git Worktree Manager

Управление изолированными рабочими копиями проекта через git worktree. Позволяет нескольким Claude работать параллельно в одном проекте, не мешая друг другу.

## Разбор аргументов

Аргумент `$ARGUMENTS` содержит операцию и имя. Определи операцию:

- Если начинается с `create` или просто имя без команды — **создать** worktree
- `list` — **показать** все worktrees
- `merge` — **смержить** worktree
- `remove` или `delete` — **удалить** worktree

Имя worktree — второй аргумент или единственный (если без команды).

---

## Операции

### 1. Создать worktree

```bash
# Убедиться что .claude/worktrees/ в .gitignore
grep -q '.claude/worktrees/' .gitignore 2>/dev/null || echo '.claude/worktrees/' >> .gitignore

# Создать worktree с отдельной веткой
git worktree add .claude/worktrees/<name> -b worktree-<name>
```

После создания сообщи пользователю:
```
Worktree "<name>" создан.
- Папка: .claude/worktrees/<name>/
- Ветка: worktree-<name>
- Все действия теперь будут в этой папке.

Когда закончу — скажи "/worktree merge <name>" чтобы перенести изменения в основной проект.
```

**После создания — ПЕРЕКЛЮЧИСЬ на работу в worktree:**
- ВСЕ операции с файлами делай через путь `.claude/worktrees/<name>/`
- Читай файлы: `.claude/worktrees/<name>/path/to/file`
- Пиши файлы: `.claude/worktrees/<name>/path/to/file`
- Запускай скрипты: `cd .claude/worktrees/<name> && ...`
- НЕ трогай файлы в корне проекта

### 2. Показать все worktrees

```bash
git worktree list
```

### 3. Смержить worktree

```bash
# 1. Закоммитить незакоммиченные изменения в worktree
cd .claude/worktrees/<name> && git add -A && git status
```

Если есть что коммитить:
```bash
cd .claude/worktrees/<name> && git commit -m "worktree <name>: описание изменений"
```

```bash
# 2. Вернуться в корень и смержить
cd <корень_проекта> && git merge worktree-<name> --no-edit
```

Если мерж-конфликт — сообщи пользователю и помоги разрешить.

После успешного мержа спроси: "Удалить worktree <name>? Изменения уже в основной ветке."

### 4. Удалить worktree

```bash
git worktree remove .claude/worktrees/<name>
git branch -d worktree-<name>
```

## Правила работы в worktree

1. **Все пути** — через `.claude/worktrees/<name>/`, НИКОГДА через корень
2. **Скрипты** — `cd .claude/worktrees/<name> && ...`
3. **Коммить часто** — маленькие коммиты = чистый мерж
4. **Не трогай корень** — только свой worktree

## Обработка ошибок

| Ошибка | Решение |
|--------|---------|
| `fatal: is not a git repository` | Проект не git-репо. Выполни `git init` |
| `fatal: '<name>' is already checked out` | Worktree уже существует. Покажи `git worktree list` |
| `error: branch 'worktree-X' not found` | Ветка удалена. `rm -rf .claude/worktrees/X` |
| Мерж-конфликт | Покажи конфликтующие файлы, помоги разрешить |
