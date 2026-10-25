# 追风 Zhuifeng

追风 iOS 越狱源 (RootHide)，基于 GitHub Pages 托管，免费、稳定、全球加速。

## 添加源

在支持 RootHide 的包管理器（Sileo / Zebra）中添加源：

```
https://temple002.github.io/zhuifeng/
```

添加后即可看到源内插件。若提示"未受信任"，确认来源后信任即可。

## 已收录插件

| 包名 | 名称 | 版本 | 说明 |
| --- | --- | --- | --- |
| com.mtac.ampere | Ampere | 1.5 | iOS 16 Style Battery Indicator |

## 维护方法（新增插件）

1. 把新的 `.deb` 文件放进 `debs/` 目录
2. 运行索引构建脚本：
   ```bash
   python3 build_repo.py
   ```
3. 提交并推送，Pages 自动更新：
   ```bash
   git add -A
   git commit -m "add: 新插件"
   git push
   ```

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

- 支持架构：`iphoneos-arm64e`（RootHide / rootless 系）
- 未启用 GPG 签名；如需要可后续补充
