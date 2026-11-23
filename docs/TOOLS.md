# Справочник tools

Аргументы и какой tool когда звать. Тот же маршрут отдаёт ресурс `sprutmonitor://tool-routing`. Если меняете инструкции в `server.py`, обновите и этот файл.

Интерфейс и REST: [sprutmonitor.ru/docs/](https://sprutmonitor.ru/docs/) и [app.sprutmonitor.ru/api/](https://app.sprutmonitor.ru/api/). Ниже только MCP. Описания tools в коде на английском.

## Общие аргументы

| Аргумент | Смысл |
|----------|--------|
| `period` | `today`, `yesterday`, `last_7_days`, `last_30_days`. Если задан, перекрывает даты |
| `date_from` / `date_to` | `YYYY-MM-DD` или `YYYY-MM-DD HH:MM:SS`. Дата без времени у `date_to` становится `23:59:59` |
| `group_id` | Id группы для POST NodeType=14. В дереве у группы есть и `ID`, и `GroupID` — это разные числа |
| `user_id` | Поле `ID` узла с `Type=2`. В отчётах то же число называется `AliasID`. В POST это NodeType=1 |
| `limit` | Строк, по умолчанию 100, потолок 500 |
| `offset` | Сдвиг страницы |
| `compact` | По умолчанию `true`: срезает большие поля и длинный текст |

Не путайте `Type` дерева (0/1/2 из `GetUsersGroups2`) с POST `NodeType` (14 группа / 1 пользователь).

## Какой tool когда

| Нужно | Tool | Не этот |
|-------|------|---------|
| Простой | `get_idle_summary` | `list_anomalies` |
| Опоздания, переработки, алерты графика | `list_anomalies` | `get_idle_summary` |
| DLP, ключевые слова, USB, правила | `list_risks` (`mode=summary`) | `list_anomalies` |
| Топ программ и сайтов по времени | `get_activity_summary` | — |
| Одна программа или сайт | `get_activity_detail` | — |
| Процент продуктивности | `get_productivity_summary` | — |
| Явка против графика | `get_timesheet` | — |
| Хронометраж | `get_chrono` | — |
| Отрезки дня | `get_day_structure` | — |
| Ключевое слово по мониторингу | `search_monitoring(filter_key=…)` | Цикл `list_monitoring` |
| Одна таблица мониторинга | `list_monitoring(kind=…)` | — |
| Плитка дашборда | `get_dashboard(widget=…)` | — |
| График аналитики | `get_analytics(view=…)` | — |
| Кто онлайн | `list_online` | Кадры видео |
| Метаданные видео | `list_stream_meta` | Скачивание файла |
| Дерево пользователей | `list_users_groups` / `list_directory` | — |
| Карточка человека | `get_user_info` | — |
| Профили и настройки, только Get | `get_account_readonly` | Set*, PIN и лицензия |
| Очередь отчётов | `list_reports` | — |
| Пробелы покрытия | `list_api_coverage` | — |
| Учётка и хост | `sprutmonitor_whoami` | — |

Пустые формальные алерты на круглосуточном графике — норма. Где можно, берите `period`, а не сырые даты.

## Короткие сценарии

| Цель | Цепочка | Как спросить |
|------|---------|--------------|
| Сводка рисков | `list_risks(period=today, mode=summary)`, имена через `list_users_groups` | Риски за сегодня по людям и правилам |
| Простой | `get_idle_summary(period=yesterday)`, можно `min_idle_hours` | Кто дольше всех простаивал вчера |
| Продуктивность группы | `get_productivity_summary` и `group_id` | Продуктивность отдела за 7 дней |
| Поиск слова | `search_monitoring(filter_key=…, period=…)` | Найти слово в мониторинге за неделю |
| Один человек | `get_user_info`, затем `get_activity_summary`, при нужде `get_activity_detail` | Что делал человек с таким `ID` из дерева сегодня |

Промпты хоста (`daily_risks_brief`, `idle_review` и другие) задают те же цепочки. См. [MCP.md](MCP.md).

## Основные tools

### `sprutmonitor_whoami`

Без аргументов. Хост API и учётка. Пароль не возвращается.

### `list_users_groups`

| Аргумент | По умолчанию | Заметка |
|----------|--------------|---------|
| `refresh` | `false` | Сбросить кэш сессии (около 5 минут) |

`Type` дерева: 0 корень, 1 группа, 2 человек. Ответ — плоский `Items`, не вложенные дети. Поля узла: `ID`, `GroupID`, `GroupUsersCount`, `IconIndex`, `NameInner`, `Type`. Имя — `NameInner`. Поля `AliasID` нет. У человека (`Type=2`) `user_id` — это `ID`; в отчётах то же число приходит как `AliasID`.

### `list_risks`

| Аргумент | По умолчанию | Заметка |
|----------|--------------|---------|
| `mode` | `summary` | `summary` или `raw` |
| `fetch_all` | `false` | Потолок 2000 строк детализации |

Плюс период, даты, `group_id`, `user_id`, `offset`, `limit`, `compact`.

В сводке `by_user` берётся из аналитики. `by_rule`, `by_day` и `sample` — со страницы рисков, пока не включён `fetch_all`.

### `list_anomalies`

Только формальные алерты. Период, `offset`, `limit`, `filter_key`, `compact`.

### `get_idle_summary`

Ранг по `InactiveTime`. Необязательный `min_idle_hours`.

### `get_activity_summary`

| Аргумент | По умолчанию |
|----------|--------------|
| `top_n` | `15` |
| `raw` | `false` |

### `get_timesheet`

Фильтры периода и необязательный `raw`.

### `get_productivity_summary`

Фильтры периода и необязательный `raw` (детализация, статистика, аналитика).

### `list_reports`

Без аргументов. Настройки отчётов и задачи обработки.

## Tools кабинета

### `get_analytics`

| Аргумент | По умолчанию | Значения |
|----------|--------------|----------|
| `view` | `overall` | `overall`, `disciplina`, `activity`, `productivity` |

### `get_dashboard`

| Аргумент | По умолчанию | Значения |
|----------|--------------|----------|
| `widget` | `users` | `users`, `screens`, `risks`, `alerts`, `top10_risks_alerts`, `productivity_by_day`, `applications`, `websites`, `top10_users`, `top10_groups`, `metric1` |
| `num_screens` | `6` | Сколько плиток экранов |

При `compact=true` крупные поля срезаются.

### `get_chrono`

Лента хронометража. Период, `offset`, `limit`, `filter_key`, `compact`.

### `get_day_structure`

| Аргумент | По умолчанию | Заметка |
|----------|--------------|---------|
| `mode` | `list` | `list` или `detail` (`detail` требует `user_id`) |
| `productivity_filter` | `0` | 0–4 |
| `activity_type_filter` | `0` | 0–2 |

### `list_monitoring`

| Аргумент | Заметка |
|----------|---------|
| `kind` | Обязателен: `Sites`, `Apps`, `Installs`, `Screens`, `Keystrokes`, `Clipboard1`, `SearchQueries`, `WebForms`, `Messengers`, `Mail`, `WebcamAudio`, `Files`, `Crawler`, `USBExplorer`, `Prints`, `NetworkInterfaces`, `WiFis`, `Traffic`, `TrafficSum` |
| `filter_objects` | Необязательная строка фильтра |

Чувствительные виды при compact обрезают текст. Бинарных файлов нет.

### `search_monitoring`

| Аргумент | По умолчанию | Заметка |
|----------|--------------|---------|
| `filter_key` | обязателен | Ключевое слово |
| `per_source_limit` | `20` | На каждый вид |
| `max_rows` | `50` | Общий потолок |
| `kinds` | все источники поиска | Подмножество через запятую, например `Sites,Apps,Mail` |

### `get_activity_detail`

| Аргумент | Заметка |
|----------|---------|
| `mode` | `activity_window` (нужен `activity_name`) или `category_window` (нужен `category_guid`) |
| `is_website` | Для окна активности |

### `list_online`

Только присутствие (`Live/Overall2`). Кадров камеры нет.

### `list_stream_meta`

| Аргумент | Заметка |
|----------|---------|
| `source` | `which_content`, `videos`, `downloads` |
| `user_id` | Нужен для `which_content` и `videos` |

`DownloadVideo` нет.

### `list_directory`

| Аргумент | По умолчанию | Значения |
|----------|--------------|----------|
| `source` | `users_groups` | `users_groups`, `users`, `groups`, `list_groups`, `computers`, `additional_users`, `additional_rights` |
| `refresh` | `false` | Сброс кэша для `users_groups` |

### `get_user_info`

| Аргумент | Заметка |
|----------|---------|
| `source` | `user_data`, `tooltip`, `group`, `computer`, `users_from_computer` |
| `user_id` | Нужен для user_data, tooltip, group |
| `computer_guid` | Нужен для источников компьютера |

### `get_account_readonly`

Только Get, без Set* и PIN. `source`: `profiles`, `computer_profiles`, `timetable`, `rules`, `profile_settings`, `computer_settings`, `account_settings`, `categories`, `top_websites`, `top_apps`, `price_settings`, `num_users`, `reports`, `processing_tasks`. Маршрутов лицензии нет: на этом облаке они отвечают 404, tool их не вызывает. Части источников нужны `profile_id`, `profiles_type`, `user_id` или `computer_guid`. Точные аргументы смотрите в описании tool у хоста.

### `list_api_coverage`

Статическая матрица, те же данные, что ресурс `sprutmonitor://coverage`. Текст аудита: [API.md](API.md).

## Наборы

`SPRUT_TOOLSETS` (по умолчанию `all`):

- `all` — все tools
- `core` — whoami, дерево, риски, алерты, простой, активность, табель, продуктивность, отчёты
- `console` — аналитика, дашборд, хронометраж, мониторинг и остальное (core добавляется сам)

## Ошибки

Сбой поднимает `ToolError`, хост видит `is_error=true`. Не ищите ключ `"error"` в успешном JSON: его убрали в 0.5.0.
