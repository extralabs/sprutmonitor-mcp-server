# Заметки по API

Снимок покрытия MCP для пакета `sprutmonitor-mcp` 0.5.x. Это аудит кабинета только на чтение, не полная копия REST.

Канонические источники:

- Сайт: https://sprutmonitor.ru/
- Документация: https://sprutmonitor.ru/docs/
- Кабинет: https://app.sprutmonitor.ru/
- Каталог API в кабинете: https://app.sprutmonitor.ru/api/

## Хосты

| URL | Роль |
|-----|------|
| `https://sprutmonitor.ru/` | Сайт |
| `https://sprutmonitor.ru/docs/` | Документация продукта |
| `https://app.sprutmonitor.ru/` | Кабинет (SPA) |
| `https://app.sprutmonitor.ru/api/` | Каталог API внутри кабинета |
| `https://cloud.sprutmonitor.ru/v3` | База REST для облака. Клиент дописывает `/api/...` |
| `serverBase` из `spm-config.json` | База локальной установки, со схемой и префиксом вроде `/MonitorServer` |

Пакет `spm-config.json` не читает. Локальную базу задают через `SPRUT_API_BASE`.

## Вход

```http
GET /api/Access/login-jwt?email=demo%40sprutmonitor.ru&password=demo
```

Полный URL облака: `https://cloud.sprutmonitor.ru/v3/api/Access/login-jwt?...`.

Ответ содержит `Token`, `RefreshToken`, `ExpiresIn`, `PublicID`.

```http
GET /api/Access/refresh-token?refresh_Token=…&PublicID=…
Authorization: Bearer <Token>
```

Заголовок Bearer нужен на вызовах данных.

## Тело фильтра пользователей (`TreeviewUsers`)

Периодные POST шлют JSON-массив. Сервер смотрит только на `NodeType` и `UserID`.

```json
[{ "NodeType": -666666, "UserID": -666666 }]
```

| NodeType | Смысл | UserID |
|----------|--------|--------|
| `-666666` | Все | `-666666` |
| `14` | Группа | id группы |
| `1` | Пользователь | `ID` узла `Type=2` (в отчётах это `AliasID`) |

Это не поля `Type` у `GET /api/Edit/GetUsersGroups2`:

| Type в GetUsersGroups2 | Смысл |
|------------------------|--------|
| `0` | Корень |
| `1` | Группа |
| `2` | Пользователь |

MCP кладёт `group_id` в NodeType 14, `user_id` в NodeType 1. Оба можно передать вместе: клиент рассчитан на то, что сервер объединяет их по ИЛИ.

`GetUsersGroups2` возвращает плоский `Items`. У узла нет `AliasID`. У человека (`Type=2`) идентификатор — `ID`, имя — `NameInner`. На демо этот `ID` совпал с `AliasID` в `Productivity/Overall3`. У группы (`Type=1`) поля `ID` и `GroupID` — разные числа. Какое из них подставлять в NodeType 14, по этому прогону не видно: сверьте с кабинетом, прежде чем фильтровать отчёты по группе.

Отчёты Overall2 приходят в PascalCase: `List`, `AliasID`, `InactiveTime`, `TotalRecords`, плюс страница (`StartFrom`, `NumRecords`).

## Заголовки периодных POST

```
Authorization: Bearer <Token>
Accept: application/json
Content-Type: application/json
DateFrom: 2026-08-20 00:00:00
DateTo: 2026-08-27 23:59:59
Offset: 0
NumRows: 100
HideHidden: False
```

Необязательно: `FilterKey`, `FilterObjects` (URL-encoded). У экранов ещё `Videos`, `Screens`, `ScreenType`.

Правило MCP: `date_to` вида `YYYY-MM-DD` уходит как конец дня `23:59:59`.

## Матрица покрытия

| Статус | Смысл |
|--------|--------|
| `covered` | Есть tool, ответ полный или уже структурирован |
| `covered_compact` | Есть tool, по умолчанию ответ урезан |
| `out_of_scope_write` | Запись кабинета, в MCP только чтение её нет |
| `out_of_scope_binary` | Скачивание файла или живые кадры |
| `out_of_scope_not_in_console` | Есть на бэкенде, текущий кабинет этим не пользуется |
| `intentional_skip` | Чтение есть, но агенту отдавать опасно (например PIN) |

| Область | Endpoint | Tool | Статус |
|---------|----------|------|--------|
| Вход | `GET /api/Access/login-jwt` | `sprutmonitor_whoami` | covered |
| Вход | `GET /api/Access/refresh-token` | клиент | covered |
| Справочник | `GET /api/Edit/GetUsersGroups2` | `list_users_groups` / `list_directory` | covered |
| Справочник | `GetUsers` / `GetGroups` / `GetListGroups` / `GetComputers2` | `list_directory` | covered |
| Справочник | `GetAdditionalUsers` / `GetAdditionalUsersRights` | `list_directory` | covered |
| Справочник | создание, переименование, перенос, удаление, слияние | — | out_of_scope_write |
| Риски | `POST /api/Risks/Overall2` | `list_risks` | covered_compact |
| Алерты | `POST /api/Alerts/Overall2` | `list_anomalies` | covered_compact |
| Риски и алерты | ShowHide / SetMarker2 / RemoveRecord2 / AddAIBlackList | — | out_of_scope_write |
| Активность | `POST /api/Activity/Overall2` | `get_activity_summary` | covered_compact |
| Активность | `ActivityWindow` / `CategoryWindow` | `get_activity_detail` | covered_compact |
| Хронометраж | `POST /api/Chrono/Overall2` | `get_chrono` | covered_compact |
| Табель | `POST /api/TimeSheet/Overall2` | `get_timesheet` | covered_compact |
| Табель | SetComment / RemoveComment | — | out_of_scope_write |
| Продуктивность | `Overall3` / `GetStats` | `get_productivity_summary` / `get_idle_summary` | covered_compact |
| Продуктивность | `DayStructureList` / `GetDayStructure` | `get_day_structure` | covered |
| Продуктивность | `GetDashboardMetric1` | `get_dashboard`, виджет `metric1` | covered |
| Аналитика | `Overall` / `GetDisciplina` / `GetActivity` / `GetProductivity` | `get_analytics` | covered |
| Дашборд | виджеты `Dashboard/Get*` | `get_dashboard` | covered_compact |
| Мониторинг | `POST /api/Monitoring/{Sites,Apps,…}` | `list_monitoring` | covered_compact |
| Мониторинг | поиск Tools Search (`FilterKey` и `FilterObjects` по видам) | `search_monitoring` | covered_compact |
| Медиа мониторинга | бинарные скриншоты, буфер, файлы, печать, камера | — | out_of_scope_binary |
| Онлайн | `POST /api/Live/Overall2` | `list_online` | covered |
| Онлайн | живая камера, LiveStream, VNC, удалённое управление | — | out_of_scope_binary |
| Поток | `WhichContentExists` / `GetVideos` / `GetDownloads` | `list_stream_meta` | covered |
| Поток | `GetVideoWithSeek` / `DownloadVideo` / `ExportVideo` | — | out_of_scope_binary |
| Пользователи | `GetUserData2` / tooltip / `GetGroup` / `GetComputer` / `GetUsersFromComputer` | `get_user_info` | covered |
| Учётка | профили, график, правила, настройки, категории, Get50*, цена, число пользователей | `get_account_readonly` | covered |
| Учётка | `getlicenseinfo-jwt` / `getlicenseinfo-expired-jwt` / `getlicenseinfo-support-jwt` | — | out_of_scope_not_in_console |
| Учётка | `GetUninstallPin1` | — | intentional_skip |
| Учётка | Set* / RecalcProductivity / PostCategories | — | out_of_scope_write |
| Отчёты | `GetReports` и `GetProcessingTasks` | `list_reports` / `get_account_readonly` | covered |
| Отчёты | `QueueReportEmail` / `SetReports` | — | out_of_scope_write |
| Прочее | CustomReports / Geo / Archive / старый XML Overall | — | out_of_scope_not_in_console |
| Биллинг | `Pay/*` | — | out_of_scope_write |
| Мета | эта матрица | `list_api_coverage` | covered |

Биллинг, SMS и reCAPTCHA в сервер не входят.

### Сводка рисков

- `by_user` из `Analytics/Overall`: итоги без перелистывания всех строк.
- `by_rule`, `by_day`, `sample` с одной страницы `Risks/Overall2`, пока `fetch_all` не включён (потолок 2000).

### Простой и алерты

- Длительность простоя — `InactiveTime` продуктивности, tool `get_idle_summary`.
- Формальные отклонения — `Alerts/Overall2`, tool `list_anomalies`. Пустые алерты на круглосуточном графике ожидаемы.

### Объём ответа

По умолчанию `limit` не больше 100 (жёсткий потолок 500). `compact=true` срезает поля-блобы и длинный текст (клавиши, тела писем, OCR).

## Заголовки, которые кабинет шлёт не как периодный POST

| Endpoint | Метод | Заголовки |
|----------|--------|-----------|
| `Edit/GetUserData2` | GET | `DateFrom`, `DateTo`, `AliasID` |
| `Edit/GetUserDetailsForToolTip` | GET | `AliasID` |
| `Edit/GetGroup` | GET | `AliasID` (путь группы этого пользователя) |
| `Edit/GetComputer` / `GetUsersFromComputer` | GET | `ComputerGuid` |
| `Productivity/GetDayStructure` | GET | `UserID`, `DateFrom`, `DateTo`, `ProductivityFilter`, `ActivityTypeFilter` |
| `Account/GetProfiles2` | GET | `ProfilesType`, `AliasID`, `AliasType` (по умолчанию `-1`) |
| `Account/GetProfileTimeTable` | GET | `ProfileTimeTableID` |
| `Account/GetProfileRules2` | GET | `ProfileRulesID` |
| `Account/GetProfileSettings` | GET | `ProfileSettingsID` |
| `Account/GetProfileComputerSettings` | GET | `ProfileComputerSettingsID` |
| `Account/GetComputerProfiles` | GET | необязательный `Guid` |
| `Stream/WhichContentExists` | GET | `AliasID`, `DateTime` (тело — голое число) |
| `Stream/GetVideos` | GET | `DateFrom`, `DateTo`, `UserID` |
| `Stream/GetDownloads` | GET | только Bearer |

### Поиск (`search_monitoring`)

Тот же веер, что у кабинета: параллельные POST мониторинга с `FilterKey` и `FilterObjects` по умолчанию.

| Вид | FilterObjects |
|-----|----------------|
| Sites | `url,wt` |
| Apps | `app,wt` |
| Keystrokes | `app,keystrokestext` |
| Clipboard1 | `app,clipboardtext` |
| Screens | `ocr,url,wt` (Videos=0) |
| Messengers | `chatstext` |
| Mail | `chatstext,sender,recipient,subject` |
| WebcamAudio | `ar,wt` |
| Files | `files_file` |
| Prints | `prints_file` |
| Installs | нет |
| NetworkInterfaces | нет |
| WebForms | `url` |

Как и кабинет, поиск не включает SearchQueries, Risks, Crawler, USBExplorer и Traffic*.

Состав демо-дерева смотрите через `list_users_groups`: имена в публичном демо могут меняться.
