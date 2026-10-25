# 追风 Zhuifeng

追风 iOS 越狱源 (RootHide)，基于 GitHub Pages 托管，免费、稳定、全球加速。

## 添加源

在支持 RootHide 的包管理器（Sileo / Zebra）中添加源：

```
https://temple002.github.io/zhuifeng/
```

添加后即可看到源内插件。若提示"未受信任"，确认来源后信任即可。

## 已收录插件

| 包名 | 名称 | 版本 | 架构 | 说明 |
| --- | --- | --- | --- | --- |
| com.mtac.ampere | Ampere魔改版 | 1.5 | iphoneos-arm64（rootless） | iOS 16 Style Battery Indicator |
| com.mtac.ampere | Ampere魔改版-RootHide | 1.5 | iphoneos-arm64e（RootHide） | iOS 16 Style Battery Indicator |

## 维护方法（新增插件）

1. 把新的 `.deb` 文件放进 `debs/` 目录
2. 提交并推送，**GitHub Actions 会自动重建索引并部署 Pages**：
   ```bash
   git add -A
   git commit -m "add: 新插件"
   git push
   ```

（可选）想在本地预览索引：`python3 build_repo.py`

## 目录结构

```
zhuifeng-repo/
├── build_repo.py        # 索引构建脚本（扫描 debs/ 生成 Packages/Release）
├── CydiaIcon.png        # 源图标（Sileo/Zebra 添加源时显示）
├── debs/                # 存放 .deb 插件包
├── Packages             # 包索引（Sileo/Zebra 读取）
├── Packages.gz          # 压缩索引
├── Packages.bz2
└── Release              # 源元信息（含索引校验值）
```

## 说明

- 支持架构：`iphoneos-arm64`（rootless 越狱，如 Dopamine）、`iphoneos-arm64e`（RootHide），Sileo 会根据设备自动分发对应架构
- 未启用 GPG 签名；如需要可后续补充
