# Spork Bucket

这个仓库是 Spork 的下载 bucket，用来维护 Linux 第三方软件包的 manifest。

Spork 默认读取 `generated/*.json` 里的已生成元数据。人工维护的源配置放在 `apps/*.json`，`scripts/update.py` 会解析最新版本和下载地址。

## 使用

```bash
spork bucket add main https://github.com/Enkialon/spork-bucket.git
spork update
spork search code
spork download code
```

## 目录

```text
apps/                 # 手写 manifest
generated/            # Spork 直接消费的生成结果
scripts/update.py     # 自动更新版本和下载地址
bucket.json           # bucket 元数据
```

## 本地更新

```bash
python3 scripts/update.py
```

更新脚本支持这些来源类型：

- `github-release`
- `fixed-url`
- `html-regex`

GitHub Actions 会定时运行同一个脚本，并在生成结果变化时自动提交。
