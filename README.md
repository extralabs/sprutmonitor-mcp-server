# MCP-сервер СпрутМонитор

<!-- mcp-name: io.github.extralabs/sprutmonitor-mcp -->

🗂️ СпрутМонитор собирает о работе компании очень много данных: время прихода и ухода, активность в программах и на сайтах, переписку в почте и мессенджерах, работу с файлами, печать, подключение флешек, срабатывания правил DLP. Всё это доступно в отчётах. Но чтобы ответить на конкретный вопрос, руководителю или специалисту по безопасности обычно приходится открыть нужный раздел, выставить фильтры, выгрузить таблицу и сопоставить цифры вручную. Если вопрос нестандартный, например «кто из отдела продаж последние две недели уходит раньше и при этом копировал клиентскую базу на внешний носитель», на это уходит много времени.

💬 Эту задачу решает MCP (Model Context Protocol). Это открытый протокол, через который языковая модель обращается к внешним системам напрямую, а не через скриншоты или пересказ пользователя. MCP-сервер описывает набор доступных инструментов, а ИИ-ассистент сам выбирает, какие из них вызвать, чтобы ответить на запрос. MCP-сервер СпрутМонитор переводит обычную речь в запросы к системе. Вы задаёте вопрос так, как задали бы его коллеге, а модель получает нужные данные, сопоставляет их и выдаёт готовый вывод с отсылкой к конкретным событиям.

🔒 Важно понимать, с какими данными идёт работа. СпрутМонитор хранит сведения, которые относятся к персональным данным и коммерческой тайне, поэтому MCP-сервер не открывает к ним обходного доступа. Он работает через API системы с правами пользователя (основного или дополнительного), и видит только то, что ему разрешено. В локальной версии данные остаются на вашем сервере, а модель получает только ту выборку, которая нужна для конкретного ответа. Какой ИИ-клиент подключать и где он будет работать, решаете вы.

- Сайт: [sprutmonitor.ru](https://sprutmonitor.ru/)
- Документация продукта: [sprutmonitor.ru/docs2/](https://sprutmonitor.ru/docs2/)
- Кабинет: [app.sprutmonitor.ru](https://app.sprutmonitor.ru/)
- Каталог API в кабинете: [app.sprutmonitor.ru/api/](https://app.sprutmonitor.ru/api/)
- Код: [extralabs/sprutmonitor-mcp-server](https://github.com/extralabs/sprutmonitor-mcp-server)

Пакет: [`sprutmonitor-mcp`](https://pypi.org/project/sprutmonitor-mcp/) (`uvx sprutmonitor-mcp` или `pip install sprutmonitor-mcp`). Сервер ходит в облако сам, отдельного удалённого MCP нет. Код основан на пакете octowatch-mcp 0.5.1 (лицензия MIT, см. [LICENSE](LICENSE)).

## Требования

- Python 3.10+
- Хост с MCP (Cursor, Claude Desktop, VS Code)
- Путь к web-api серверу СпрутМонитор. Например: `https://cloud.sprutmonitor.ru/v3` или `http://192.168.1.8:82/MonitorServer/`

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

## Свой вход и локальная установка

| Режим | Что задать |
|-------|------------|
| Демо | `demo@sprutmonitor.ru` / `demo` |
| Свой кабинет | Ваш логин и пароль от аккаунта СпрутМонитор [app.sprutmonitor.ru](https://app.sprutmonitor.ru/) или логин и пароль дополнительного пользователя (вкладка Настройки — Доступ) |
| Локальный сервер | `SPRUT_API_BASE` = адрес web-api сервера СпрутМонитор, со схемой и префиксом (например `https://host:port/MonitorServer`) |

| Переменная | Смысл |
|------------|--------|
| `SPRUT_EMAIL` | Логин аккаунта |
| `SPRUT_PASSWORD` | Пароль |
| `SPRUT_API_BASE` | Адрес Web-api сервера СпрутМонитор, в т.ч. облако |

Те же данные можно положить в `.env` рядом с рабочим каталогом процесса. Образец: [.env.example](.env.example). Проверка: инструмент `sprutmonitor_whoami`. Сверьте ответ с [кабинетом](https://app.sprutmonitor.ru/).

## Примеры вопросов

- Какие риски за последний день?
- Кто дольше всех простаивал вчера?
- Продуктивность отдела за 7 дней
- Найти слово в мониторинге за неделю
- Список пользователей и групп

Простой — это `get_idle_summary`, а не `list_anomalies`. Формальные отклонения (опоздания, переработки) — `list_anomalies`. Поиск по ключевому слову — `search_monitoring`, а не цикл по `list_monitoring`.

## Безопасность

Ответы tools могут содержать данные сотрудников: не выкладывайте их в открытые каналы. Подробнее: [SECURITY.md](SECURITY.md).

## Ограничения

- Только чтение.
- Нет скачивания бинарных скриншотов и видео, только метаданные потока.

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
| `SPRUT_DEFAULT_DAYS` | `1` | Глубина, если нет дат и `period` |
| `SPRUT_TOOLSETS` | `all` | `all`, `core` или `console` (console включает core) |

```bash
sprutmonitor-mcp
sprutmonitor-mcp --transport streamable-http
```

Второй вариант слушает `http://127.0.0.1:8000/mcp`.

Период: `today`, `yesterday`, `last_7_days`, `last_30_days` либо `date_from` / `date_to`. Дата без времени — целый день, `date_to` заканчивается в `23:59:59`. В POST фильтр группы — `NodeType=14`, человека — `NodeType=1`.

## Документация

| Файл | Содержание |
|------|------------|
| [docs/README.md](docs/README.md) | Оглавление |
| [docs/hosts.md](docs/hosts.md) | Установка в хост и свой вход |
| [docs/TOOLS.md](docs/TOOLS.md) | Аргументы tools |
| [docs/MCP.md](docs/MCP.md) | Протокол, ресурсы, промпты |
| [docs/API.md](docs/API.md) | Что из API кабинета покрыто |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Типовые сбои |

## Участие

См. [CONTRIBUTING.md](CONTRIBUTING.md) и [CHANGELOG.md](CHANGELOG.md).

## Лицензия

MIT — см. [LICENSE](LICENSE).
