# Установка в хосты

Как запустить `sprutmonitor-mcp` в Cursor, Claude Desktop и VS Code и как подставить свой вход.

Сайт: [sprutmonitor.ru](https://sprutmonitor.ru/) · [документация](https://sprutmonitor.ru/docs2/) · [кабинет](https://app.sprutmonitor.ru/) · [каталог API](https://app.sprutmonitor.ru/api/).

## Что нужно

- Python 3.10+ в том PATH, который видит хост
- Пакет из исходников: `pip install -e .` в этом каталоге (на PyPI его нет)
- Путь к web-api серверу СпрутМонитор. Например: `https://cloud.sprutmonitor.ru/v3` или `http://192.168.1.8:82/MonitorServer/`

## Cursor

Демо, если команда `sprutmonitor-mcp` уже в PATH после `pip install -e .`:

Файл [../examples/cursor-mcp-pypi.json](../examples/cursor-mcp-pypi.json). Имя файла старое: пакета на PyPI нет, команда берётся из локальной установки.

Корневой [../mcp.json](../mcp.json) вызывает `uvx sprutmonitor-mcp`. Так сервер запустится только после публикации на PyPI. До этого используйте примеры выше или запуск из каталога.

Свой кабинет: [../examples/cursor-mcp-pypi-with-env.json](../examples/cursor-mcp-pypi-with-env.json). Подставьте логин и пароль, перезапустите MCP и спросите, кто вошёл.

### Из исходников

[../examples/cursor-mcp.json](../examples/cursor-mcp.json): `command` = `python`, аргумент `-m sprutmonitor_mcp`, `cwd` — абсолютный путь к каталогу.

- macOS/Linux: `/absolute/path/to/sprutmonitor-mcp-server`
- Windows в JSON: `D:\\path\\to\\sprutmonitor-mcp-server`

Если хост не видит PATH оболочки, укажите `python` из `.venv`.

## Claude Desktop

1. `pip install -e .` в каталоге пакета.
2. В `claude_desktop_config.json` вставьте блок из [../examples/claude-desktop-pypi.json](../examples/claude-desktop-pypi.json) или [../examples/claude-desktop-pypi-with-env.json](../examples/claude-desktop-pypi-with-env.json).
3. Перезапустите Claude Desktop.
4. Сервер в списке называется `sprutmonitor`.

Из исходников: [../examples/claude-desktop.json](../examples/claude-desktop.json), `cwd` как у Cursor.

## VS Code

Тот же блок `command` + `env`, что у Cursor. Точный пункт меню зависит от версии поддержки MCP: «MCP: Open User Configuration» или `.vscode/mcp.json` в рабочей области.

## Свой вход

По умолчанию демо `demo@sprutmonitor.ru` / `demo`. Для своего кабинета:

1. Возьмите ваш логин и пароль от аккаунта СпрутМонитор [app.sprutmonitor.ru](https://app.sprutmonitor.ru/) или логин и пароль дополнительного пользователя (вкладка Настройки — Доступ).
2. Задайте переменные:

| Переменная | Пример |
|------------|--------|
| `SPRUT_EMAIL` | логин аккаунта |
| `SPRUT_PASSWORD` | пароль |
| `SPRUT_API_BASE` | `https://cloud.sprutmonitor.ru/v3` или `http://192.168.1.8:82/MonitorServer/` |

3. Лучше положить их в `env` JSON хоста, а не в репозиторий.
4. Для запуска из исходников можно скопировать [../.env.example](../.env.example) в `.env` в рабочем каталоге процесса. `.env` не коммитить.

Затем вызовите `sprutmonitor_whoami` и сверьте учётку с кабинетом.

### Адрес web-api

`SPRUT_API_BASE` — адрес web-api сервера СпрутМонитор, со схемой и префиксом (например `https://host:port/MonitorServer`). Облако: `https://cloud.sprutmonitor.ru/v3`. Своя установка: `http://192.168.1.8:82/MonitorServer/`.

## Первые вопросы

1. Кто я в СпрутМонитор?
2. Риски за последнюю неделю.
3. Список пользователей и групп.

Если ответ пустой, сверьте тот же период в [кабинете](https://app.sprutmonitor.ru/).

## Streamable HTTP

```bash
sprutmonitor-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

По умолчанию только localhost. Другой адрес выставляет сессию в сеть. См. [SECURITY.md](../SECURITY.md).

## ChatGPT и прочие хосты

Отдельного JSON под ChatGPT нет: многие облачные агенты ждут удалённый URL, а не локальную команду.

1. Для рабочего стола используйте Cursor, Claude Desktop или VS Code.
2. Если хост умеет свой MCP по HTTP, поднимите Streamable HTTP на localhost и зарегистрируйте `http://127.0.0.1:8000/mcp` так, как написано у этого хоста.

## Дальше

- Аргументы: [TOOLS.md](TOOLS.md)
- Протокол: [MCP.md](MCP.md)
- Сбои: [troubleshooting.md](troubleshooting.md)
