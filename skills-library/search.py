#!/usr/bin/env python3
"""
Поиск скиллов в библиотеке antigravity-awesome-skills.

Уровни поиска:
  Уровень 1 (быстрый)   — поиск по локальному индексу (name + description)
  Уровень 2 (глубокий)  — скачивает SKILL.md топ-5 и сравнивает полный текст
  Уровень 3 (референс)  — для создания нового скилла, показывает структуру аналогов

Использование:
  python3 search.py "legal contract"                   # уровень 1
  python3 search.py "legal contract" --deep            # уровень 2
  python3 search.py "проверка договоров" --new         # уровень 3
  python3 search.py --update                           # обновить индекс с GitHub
"""

import json, sys, argparse, re, os, subprocess, urllib.request, urllib.error
from datetime import datetime, timezone

INDEX_FILE   = os.path.join(os.path.dirname(__file__), "skills_index.json")
REPO         = "sickn33/antigravity-awesome-skills"
INDEX_URL    = f"https://api.github.com/repos/{REPO}/contents/data/skills_index.json"
SKILL_BASE   = f"https://api.github.com/repos/{REPO}/contents/plugins/antigravity-awesome-skills-claude/skills"
MAX_AGE_DAYS = 7  # обновлять индекс если старше 7 дней


# ─── Утилиты ──────────────────────────────────────────────────────────────────

def fetch_github(url):
    """Скачать файл с GitHub API, вернуть текст."""
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    # Если есть GITHUB_TOKEN — используем
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  GitHub API ошибка {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"  Ошибка сети: {e}")
        return None


def load_index():
    """Загрузить локальный индекс, при необходимости обновить."""
    if not os.path.exists(INDEX_FILE):
        print("Индекс не найден. Скачиваю с GitHub...")
        update_index()
    else:
        age = (datetime.now(timezone.utc).timestamp() - os.path.getmtime(INDEX_FILE)) / 86400
        if age > MAX_AGE_DAYS:
            print(f"Индекс устарел ({int(age)} дней). Обновляю...")
            update_index()
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def update_index():
    """Скачать свежий индекс с GitHub."""
    print(f"Загрузка индекса из {REPO}...")
    data = fetch_github(INDEX_URL)
    if not data or "content" not in data:
        print("Не удалось скачать индекс. Используется локальная копия.")
        return
    import base64
    content = base64.b64decode(data["content"]).decode("utf-8")
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    skills = json.loads(content)
    print(f"Индекс обновлён: {len(skills)} скиллов.")


def fetch_skill_md(skill_name):
    """Скачать полный SKILL.md для скилла по имени."""
    url = f"{SKILL_BASE}/{skill_name}/SKILL.md"
    data = fetch_github(url)
    if not data or "content" not in data:
        return None
    import base64
    return base64.b64decode(data["content"]).decode("utf-8")


# ─── Уровень 1: быстрый поиск по индексу ─────────────────────────────────────

def search_index(query, skills, category=None, risk=None, limit=20):
    keywords = query.lower().split() if query else []
    results = []

    for skill in skills:
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        cat  = skill.get("category", "").lower()

        if category and category.lower() not in cat:
            continue
        if risk and skill.get("risk", "") != risk:
            continue

        score = 0
        for kw in keywords:
            if kw in name: score += 3
            if kw in desc: score += 1
            if kw in cat:  score += 2

        if not keywords or score > 0:
            results.append((score, skill))

    results.sort(key=lambda x: -x[0])
    return results[:limit]


def print_results(results, show_score=False):
    if not results:
        print("Ничего не найдено.")
        return
    print(f"\nНайдено: {len(results)} скиллов\n")
    header = f"{'Скилл':<45} {'Категория':<20} {'Риск':<10} Описание"
    print(header)
    print("-" * 120)
    for score, s in results:
        name = s.get("name", "")[:44]
        cat  = s.get("category", "")[:19]
        risk = s.get("risk", "")[:9]
        desc = s.get("description", "")[:55]
        score_str = f"[{score:2d}] " if show_score else ""
        print(f"{score_str}{name:<45} {cat:<20} {risk:<10} {desc}")


# ─── Уровень 2: глубокий поиск (читает SKILL.md с GitHub) ────────────────────

def search_deep(query, skills, limit=5):
    print(f"\n[Уровень 1] Быстрый поиск по индексу...")
    top = search_index(query, skills, limit=10)
    if not top:
        print("Ничего не найдено в индексе.")
        return

    print_results(top[:5], show_score=True)

    print(f"\n[Уровень 2] Загружаю SKILL.md топ-{min(5, len(top))} для глубокого анализа...\n")
    keywords = query.lower().split()
    deep_results = []

    for score, skill in top[:5]:
        name = skill.get("name", "")
        print(f"  → {name}...", end=" ", flush=True)
        content = fetch_skill_md(name)
        if not content:
            print("не удалось скачать")
            continue

        # Глубокий скоринг по полному тексту
        text = content.lower()
        deep_score = score * 2  # базовый скор из индекса
        for kw in keywords:
            deep_score += text.count(kw) * 1
        # Бонус за теги в frontmatter
        tags_match = re.findall(r'tags:\s*\[([^\]]+)\]', content, re.IGNORECASE)
        if tags_match:
            tags = tags_match[0].lower()
            for kw in keywords:
                if kw in tags:
                    deep_score += 5

        print(f"скор {deep_score}")
        deep_results.append((deep_score, skill, content))

    deep_results.sort(key=lambda x: -x[0])

    print(f"\n{'─'*60}")
    print(f"Топ результаты после глубокого анализа:\n")
    for i, (score, skill, content) in enumerate(deep_results[:limit], 1):
        name = skill.get("name", "")
        desc = skill.get("description", "")
        print(f"{i}. {name}  [скор: {score}]")
        print(f"   {desc}")
        # Показать trigger/use section из SKILL.md
        use_match = re.search(r'## (Use|When|Когда)[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if use_match:
            snippet = use_match.group(2).strip()[:200]
            print(f"   Применение: {snippet}")
        print()


# ─── Уровень 3: референс для создания нового скилла ──────────────────────────

def search_for_new_skill(description, skills):
    print(f"\n[Уровень 3] Поиск референсов для создания скилла...")
    print(f"Описание: {description}\n")

    top = search_index(description, skills, limit=8)
    if not top:
        print("Похожих скиллов не найдено — твой скилл будет уникальным!")
        return

    print(f"[Уровень 1] Похожие скиллы в индексе:")
    print_results(top[:5], show_score=True)

    print(f"\n[Уровень 2] Загружаю структуру топ-3 как референс...\n")

    for score, skill in top[:3]:
        name = skill.get("name", "")
        print(f"{'═'*60}")
        print(f"РЕФЕРЕНС: {name}")
        print(f"{'═'*60}")
        content = fetch_skill_md(name)
        if not content:
            print("  (не удалось загрузить)\n")
            continue

        # Показываем frontmatter + структуру секций
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            print(f"Frontmatter:\n---\n{fm_match.group(1)}\n---")

        sections = re.findall(r'^(#{1,3} .+)', content, re.MULTILINE)
        print(f"\nСтруктура секций:")
        for s in sections:
            print(f"  {s}")

        # Инструкции (первые 300 символов)
        instr_match = re.search(r'## Instructions?\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if instr_match:
            print(f"\nИнструкции (фрагмент):\n{instr_match.group(1).strip()[:300]}")
        print()

    # Шаблон для нового скилла
    slug = re.sub(r'[^a-z0-9]+', '-', description.lower())[:40].strip('-')
    print(f"\n{'─'*60}")
    print(f"ШАБЛОН для нового скилла (скилл: {slug}):\n")
    print(f"""---
name: {slug}
description: {description[:120]}
category: uncategorized
risk: safe
source: personal
---

## Когда использовать

- TODO: опиши сценарии

## Когда НЕ использовать

- TODO: опиши исключения

## Инструкции

TODO: конкретные шаги для Claude
""")


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Поиск скиллов в библиотеке antigravity-awesome-skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 search.py "legal contract"              # быстрый поиск
  python3 search.py "code review" --risk safe     # только безопасные
  python3 search.py "security" --category security
  python3 search.py "legal" --deep                # глубокий поиск (GitHub)
  python3 search.py "проверка договоров" --new    # референс для нового скилла
  python3 search.py --update                      # обновить индекс
        """
    )
    parser.add_argument("query",      nargs="?", default="",    help="Поисковый запрос")
    parser.add_argument("--deep",     action="store_true",      help="Уровень 2: читать SKILL.md с GitHub")
    parser.add_argument("--new",      action="store_true",      help="Уровень 3: найти референсы + шаблон для нового скилла")
    parser.add_argument("--update",   action="store_true",      help="Обновить индекс с GitHub")
    parser.add_argument("--category", "-c",                     help="Фильтр по категории")
    parser.add_argument("--risk",     "-r", choices=["safe","unknown"], help="Фильтр по риску")
    parser.add_argument("--limit",    "-l", type=int, default=20, help="Макс. результатов (по умолчанию 20)")
    args = parser.parse_args()

    if args.update:
        update_index()
        sys.exit(0)

    skills = load_index()

    if args.new:
        if not args.query:
            print("Укажи описание скилла: python3 search.py 'описание' --new")
            sys.exit(1)
        search_for_new_skill(args.query, skills)

    elif args.deep:
        if not args.query:
            print("Укажи запрос: python3 search.py 'запрос' --deep")
            sys.exit(1)
        search_deep(args.query, skills, limit=args.limit)

    else:
        results = search_index(args.query, skills, args.category, args.risk, args.limit)
        print_results(results, show_score=True)
