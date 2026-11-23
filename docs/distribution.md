# Публикация

Код: [extralabs/sprutmonitor-mcp-server](https://github.com/extralabs/sprutmonitor-mcp-server).

Пакет `sprutmonitor-mcp` ставится из исходников этого репозитория. На PyPI и в MCP Registry он пока не опубликован.

Процесс MCP всегда запускается на машине пользователя (`stdio`). Он ходит в уже существующее облако СпрутМонитор с логином и паролем аккаунта. Отдельного удалённого MCP-хоста нет.

[scripts/sync-github-about.ps1](../scripts/sync-github-about.ps1) и [scripts/open-directory-submits.ps1](../scripts/open-directory-submits.ps1) ничего не отправляют. Не запускайте их, пока публикация в каталоги не настроена заново.

Идентификатор в [server.json](../server.json): `io.github.extralabs/sprutmonitor-mcp`.
