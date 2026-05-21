# Spork Bucket

这个仓库是 Spork 的下载 bucket，用来维护 Linux 第三方软件包的 manifest。

Spork 直接读取 `bucket/*.json` 里的软件元数据。`scripts/update.py` 只是仓库自动化使用的辅助脚本，Spork 客户端不会执行它。

## 使用

```bash
spork bucket add main https://github.com/Enkialon/spork-bucket.git
spork update
spork search code
spork download code
```

## 目录

```text
bucket/               # Spork 直接消费的 app manifest
scripts/update.py     # 基于 checkver 字段更新 manifest 的仓库自动化脚本
bucket.json           # bucket 元数据
```

## 本地更新

```bash
python3 scripts/update.py
```

更新脚本会根据每个 `bucket/*.json` 里的 `checkver` 字段刷新版本和下载地址。它支持这些来源类型：

- `github-release`
- `fixed-url`
- `html-regex`

GitHub Actions 会定时运行这个脚本，并在 manifest 变化时自动提交。本地 `spork update` 只拉取仓库并读取 JSON。
