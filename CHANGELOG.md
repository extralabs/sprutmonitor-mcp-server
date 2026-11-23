# История изменений

Формат близзок к [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/).

## [0.5.1]

Снимок поведения клиента 0.5.1, собранный как пакет СпрутМонитор.

### Изменено

- Команда `sprutmonitor-mcp`, модуль `sprutmonitor_mcp`.
- База по умолчанию `https://cloud.sprutmonitor.ru/v3`, демо `demo@sprutmonitor.ru` / `demo`.
- Переменные `SPRUT_API_BASE`, `SPRUT_EMAIL`, `SPRUT_PASSWORD`, `SPRUT_DEFAULT_DAYS`, `SPRUT_TOOLSETS`.
- Инструмент `sprutmonitor_whoami`, ресурсы `sprutmonitor://`.
- Тексты для людей на русском. Описания tools для модели остаются на английском.

Поведение, которое уже было в этом снимке: ошибки tools через `ToolError` (`is_error`), подсказка `read_only_hint`, логи в stderr, промпты `daily_risks_brief`, `idle_review`, `user_activity_drilldown`, `monitoring_keyword_hunt`, наборы `SPRUT_TOOLSETS=all|core|console`.
