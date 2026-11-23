# Протокол MCP

Сервер только на чтение для облака [СпрутМонитор](https://sprutmonitor.ru/). Руководства продукта и каталог REST: [sprutmonitor.ru/docs/](https://sprutmonitor.ru/docs/) и [app.sprutmonitor.ru/api/](https://app.sprutmonitor.ru/api/). Здесь только поверхность самого MCP.

Транспорт: stdio по умолчанию или Streamable HTTP.

## Tools

- У всех tools `annotations.read_only_hint=True` и `open_world_hint=True`.
- Сбой — это `ToolError`, у хоста `is_error=True`. Успешный JSON с ключом `"error"` больше не используется (с 0.5.0).
- Все tools возвращают JSON-объект в `structured_content`. Не-объект API заворачивается в `{"data": ...}`.
- Аргументы и выбор tool: [TOOLS.md](TOOLS.md). Описания в коде на английском, чтобы модель не промахивалась.

## Ресурсы

| URI | Заметка |
|-----|---------|
| `sprutmonitor://coverage` | Матрица пробелов, те же данные, что `list_api_coverage` |
| `sprutmonitor://tool-routing` | Какой tool когда. Держите в ладу с [TOOLS.md](TOOLS.md) |
| `sprutmonitor://whoami` | Живая сессия. Может упасть с `ResourceError` |

Как открыть ресурс, зависит от хоста. Если неясно, вызовите тот же tool.

## Промпты

| Промпт | Зачем |
|--------|--------|
| `daily_risks_brief` | Сводка рисков (`period`) |
| `idle_review` | Рейтинг простоя через `get_idle_summary` |
| `user_activity_drilldown` | Активность одного человека (`user_id`, `period`) |
| `monitoring_keyword_hunt` | Поиск через `search_monitoring` (`filter_key`, `period`) |

Тексты промптов на английском: их читает модель.

## Наборы tools

`SPRUT_TOOLSETS` (по умолчанию `all`):

- `all` — все
- `core` — whoami, дерево, риски, алерты, простой, активность, табель, продуктивность, отчёты
- `console` — аналитика, дашборд, хронометраж, мониторинг и остальное кабинета, плюс core
- `core,console` — то же, что `all`

## Транспорт

```bash
sprutmonitor-mcp
sprutmonitor-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

HTTP по умолчанию на `127.0.0.1`. Другой адрес выставляет учётные данные в сеть. См. [SECURITY.md](../SECURITY.md).

## Логи

Логи идут в stderr. stdout занят кадром stdio.

## Inspector

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) можно направить на `sprutmonitor-mcp` (stdio), чтобы посмотреть tools, ресурсы и промпты.

## Рядом

- Установка: [hosts.md](hosts.md)
- Покрытие API: [API.md](API.md)
- Кабинет: [app.sprutmonitor.ru](https://app.sprutmonitor.ru/)
