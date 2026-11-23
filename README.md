# MCP-сервер СпрутМонитор

Локальный MCP-сервер только на чтение для облака [СпрутМонитор](https://sprutmonitor.ru/). Cursor, Claude и VS Code могут спрашивать про риски, простой, продуктивность и мониторинг. Код основан на пакете octowatch-mcp 0.5.1 (лицензия MIT, см. [LICENSE](LICENSE)).

- Сайт: [sprutmonitor.ru](https://sprutmonitor.ru/)
- Документация продукта: [sprutmonitor.ru/docs/](https://sprutmonitor.ru/docs/)
- Кабинет: [app.sprutmonitor.ru](https://app.sprutmonitor.ru/)
- Каталог API в кабинете: [app.sprutmonitor.ru/api/](https://app.sprutmonitor.ru/api/)
- Код: [extralabs/sprutmonitor-mcp-server](https://github.com/extralabs/sprutmonitor-mcp-server)

Пакет на PyPI не опубликован. Ставится из этого каталога. Сервер ходит в облако сам, отдельного удалённого MCP нет.

## Требования

- Python 3.10+
- Хост с MCP (Cursor, Claude Desktop, VS Code)
- Сеть до базы API. По умолчанию `https://cloud.sprutmonitor.ru/v3`

Клиент дописывает пути `/api/...` к этой базе. Префикс `/v3` должен остаться в базе, иначе логин уйдёт не туда.

## Быстрый старт

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
sprutmonitor-mcp
```

Пример для Cursor (демо-вход):

```json
{
  "mcpServers": {
    "sprutmonitor": {
      "command": "sprutmonitor-mcp",
      "env": {
        "SPRUT_API_BASE": "https://cloud.sprutmonitor.ru/v3",
        "SPRUT_EMAIL": "demo@sprutmonitor.ru",
        "SPRUT_PASSWORD": "demo"
      }
    }
  }
}
```

Готовые файлы: [examples/cursor-mcp-pypi.json](examples/cursor-mcp-pypi.json), [examples/claude-desktop-pypi.json](examples/claude-desktop-pypi.json). Запуск из исходников без установки команды в PATH: [examples/cursor-mcp.json](examples/cursor-mcp.json) (`python -m sprutmonitor_mcp` и свой `cwd`). Шаги по хостам: [docs/hosts.md](docs/hosts.md).

После перезапуска хоста: «Кто я в СпрутМонитор?» или «Риски за последнюю неделю».

Демо-кабинет общий. Не гоняйте по нему длинные циклы.

## Свой вход и локальная установка

Облаку нужна учётка оператора кабинета. Пароли в репозиторий не кладутся: их передаёт хост через `env`.

| Режим | Что задать |
|-------|------------|
| Демо | `demo@sprutmonitor.ru` / `demo` |
| Свой кабинет | Почта и пароль оператора с урезанными правами |
| Локальный сервер | `SPRUT_API_BASE` = значение `serverBase` из `spm-config.json`, со схемой и префиксом (например `https://host/MonitorServer`). Этот пакет файл `spm-config.json` не читает |

| Переменная | Смысл |
|------------|--------|
| `SPRUT_EMAIL` | Почта оператора |
| `SPRUT_PASSWORD` | Пароль |
| `SPRUT_API_BASE` | База API, если не публичное облако |

Те же данные можно положить в `.env` рядом с рабочим каталогом процесса. Образец: [.env.example](.env.example). Проверка: инструмент `sprutmonitor_whoami`. Сверьте ответ с [кабинетом](https://app.sprutmonitor.ru/).

## Примеры вопросов

- Какие риски за последний день?
- Кто дольше всех простаивал вчера?
- Продуктивность отдела за 7 дней
- Найти слово в мониторинге за неделю
- Список пользователей и групп

Простой — это `get_idle_summary`, а не `list_anomalies`. Формальные отклонения (опоздания, переработки) — `list_anomalies`. Поиск по ключевому слову — `search_monitoring`, а не цикл по `list_monitoring`.

## Безопасность

Демо-вход публичный. Боевые пароли не пишите в конфиг MCP и не коммитьте. Сервер ничего не изменяет в кабинете и не скачивает бинарные скриншоты и видео. Ответы tools могут содержать данные сотрудников: не выкладывайте их в открытые каналы. Подробнее: [SECURITY.md](SECURITY.md).

## Ограничения

- Только чтение. Это не замена [кабинета](https://app.sprutmonitor.ru/).
- Нет скачивания бинарных скриншотов и видео, только метаданные потока.
- Это не копия документации продукта и не полный каталог REST.
- Биллинг, SMS и reCAPTCHA сюда не входят.

## Основные tools

Имена на латинице. Описание, по которому модель выбирает tool, в коде на английском.

| Tool | Область | Заметка |
|------|---------|---------|
| `sprutmonitor_whoami` | Сессия | Хост и учётка, без пароля |
| `list_users_groups` | Дерево | Плоский список `Items`. Type 0 корень, 1 группа, 2 человек. Id человека — поле `ID` |
| `list_risks` | Риски | По умолчанию `mode=summary` |
| `list_anomalies` | Алерты | Формальные отклонения, не простой |
| `get_idle_summary` | Продуктивность | Ранг по `InactiveTime` |
| `get_activity_summary` | Активность | Топ программ и сайтов |
| `get_timesheet` | Табель | Факт против графика |
| `get_productivity_summary` | Продуктивность | Сводка по людям |
| `list_reports` | Отчёты | Расписание и очередь |

## Tools кабинета

| Tool | Область | Заметка |
|------|---------|---------|
| `get_analytics` | Аналитика | `view=overall\|disciplina\|activity\|productivity` |
| `get_dashboard` | Дашборд | Виджеты, крупные поля срезаются |
| `get_chrono` | Хронометраж | Лента |
| `get_day_structure` | Структура дня | `list` или `detail` |
| `list_monitoring` | Мониторинг | Один вид таблицы |
| `search_monitoring` | Поиск | `filter_key` по нескольким видам |
| `get_activity_detail` | Окно активности | Детализация |
| `list_online` | Онлайн | Только присутствие |
| `list_stream_meta` | Поток | Только метаданные |
| `list_directory` | Справочники | Пользователи, группы, компьютеры |
| `get_user_info` | Карточка | `user_id` — `ID` человека из дерева |
| `get_account_readonly` | Настройки Get* | Без записи и без PIN |
| `list_api_coverage` | Матрица | Что покрыто и что сознательно не входит |

Аргументы и маршрутизация: [docs/TOOLS.md](docs/TOOLS.md). Протокол: [docs/MCP.md](docs/MCP.md).

## Конфигурация

| Переменная | По умолчанию | Смысл |
|------------|--------------|--------|
| `SPRUT_API_BASE` | `https://cloud.sprutmonitor.ru/v3` | База API (`serverBase`) |
| `SPRUT_EMAIL` | `demo@sprutmonitor.ru` | Оператор |
| `SPRUT_PASSWORD` | `demo` | Только демо |
| `SPRUT_DEFAULT_DAYS` | `1` | Глубина, если нет дат и `period` |
| `SPRUT_TOOLSETS` | `all` | `all`, `core` или `console` (console включает core) |

```bash
sprutmonitor-mcp
sprutmonitor-mcp --transport streamable-http
```

Второй вариант слушает `http://127.0.0.1:8000/mcp`.

Период: `today`, `yesterday`, `last_7_days`, `last_30_days` либо `date_from` / `date_to`. Дата без времени — целый день, `date_to` заканчивается в `23:59:59`. В POST фильтр группы — `NodeType=14`, человека — `NodeType=1`. Число для человека берётся из поля `ID` узла с `Type=2` в `list_users_groups`. Поля `AliasID` в этом дереве нет: так называется тот же id уже в отчётах. `Type` дерева — не `NodeType`.

## Документация

| Файл | Содержание |
|------|------------|
| [docs/README.md](docs/README.md) | Оглавление |
| [docs/hosts.md](docs/hosts.md) | Установка в хост и свой вход |
| [docs/TOOLS.md](docs/TOOLS.md) | Аргументы tools |
| [docs/MCP.md](docs/MCP.md) | Протокол, ресурсы, промпты |
| [docs/API.md](docs/API.md) | Что из API кабинета покрыто |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Типовые сбои |
| [docs/distribution.md](docs/distribution.md) | Публикация ждёт своего репозитория |
| [docs/registry.md](docs/registry.md) | Реестр MCP пока не используется |

## Участие

См. [CONTRIBUTING.md](CONTRIBUTING.md) и [CHANGELOG.md](CHANGELOG.md).

## Лицензия

MIT — см. [LICENSE](LICENSE).
