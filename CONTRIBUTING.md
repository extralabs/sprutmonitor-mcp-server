# Участие

Пакет `sprutmonitor-mcp` — MCP-сервер только на чтение для [СпрутМонитор](https://sprutmonitor.ru/).

## Сборка

Нужен Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

Запуск: `sprutmonitor-mcp` или `python -m sprutmonitor_mcp`.

## Проверки

```bash
ruff check src tests
ruff format --check src tests
# Windows PowerShell:
$env:SPRUT_SKIP_LIVE = "1"
pytest tests/ -q
```

CI гоняет те же юнит-тесты на Python 3.10 и 3.12 с `SPRUT_SKIP_LIVE=1` и отдельно живой smoke демо. Новые тесты по возможности оставляйте без сети.

## Документация

Тексты для людей — на русском (`README.md`, `docs/`). Описания tools в `server.py`, по которым модель выбирает инструмент, — на английском.

Если меняются аргументы, переменные или маршрутизация:

1. Обновите [docs/TOOLS.md](docs/TOOLS.md) и таблицы в README.
2. Синхронизируйте [docs/hosts.md](docs/hosts.md) и `.env.example`.
3. Сверьте текст «какой tool когда» с ресурсом `sprutmonitor://tool-routing` и инструкциями в `src/sprutmonitor_mcp/server.py`.

Не копируйте в репозиторий большие куски сайта и каталога `/api/`. Ссылайтесь на них и пишите только то, что нужно MCP.

- https://sprutmonitor.ru/
- https://sprutmonitor.ru/docs2/
- https://app.sprutmonitor.ru/
- https://app.sprutmonitor.ru/api/

Пути `/api/...`, фильтры TreeviewUsers, режим только на чтение и отказ скачивать видео не меняйте без отдельного решения: это общий API кабинета.

## Публикация

Своего GitHub и PyPI пока нет. Не ставьте тег `v*` и не запускайте [`.github/workflows/publish.yml`](.github/workflows/publish.yml). См. [docs/distribution.md](docs/distribution.md).

## Лицензия

Вклад идёт под MIT. Текст лицензии и уведомление о правах в [LICENSE](LICENSE) не удаляйте.
