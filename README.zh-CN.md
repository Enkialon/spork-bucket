# Spork Bucket

这个仓库是 Spork 默认下载 bucket，用来维护 Linux 第三方 DEB 软件包的 manifest。

它为 Spork 这个受 Scoop Windows 包管理器工作流启发的 Linux 包管理工具提供 bucket manifest。Spork 直接读取 `bucket/*.json` 里的软件元数据。`scripts/update.py` 只是仓库自动化使用的辅助脚本，Spork 客户端不会执行它。

关键词：Spork bucket、DEB package manifests、Linux package manager bucket、apt package downloads、dpkg package metadata、Scoop-style bucket。

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

## 多架构 Manifest

如果软件按 CPU 架构发布不同 DEB 文件，使用 `architectures`：

```json
{
  "id": "example",
  "version": "1.0.0",
  "architectures": {
    "amd64": {
      "url": "https://example.com/example_1.0.0_amd64.deb",
      "sha256": null
    },
    "arm64": {
      "url": "https://example.com/example_1.0.0_arm64.deb",
      "sha256": null
    }
  },
  "checkver": {
    "type": "github-release",
    "repo": "owner/example",
    "versionRegex": "^v?(.*)$",
    "architectures": {
      "amd64": {
        "assetPattern": "example_[0-9.]+_amd64\\.deb$"
      },
      "arm64": {
        "assetPattern": "example_[0-9.]+_arm64\\.deb$"
      }
    }
  }
}
```

Spork 客户端会在 `spork update` 时按配置架构选择对应构建。仓库自动化会逐架构更新这些 URL。

GitHub Actions 会定时运行这个脚本，并在 manifest 变化时自动提交。本地 `spork update` 只拉取仓库并读取 JSON。
