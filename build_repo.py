#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追风 (Zhuifeng) iOS 越狱源构建脚本
用法: python3 build_repo.py
功能: 扫描 debs/ 目录下的所有 .deb，生成 Packages / Packages.gz / Packages.bz2 / Release
      新增插件时，把 .deb 放进 debs/ 后重新运行本脚本即可。
"""
import os, subprocess, hashlib, gzip, bz2, tempfile, tarfile, email.utils, re

REPO = os.path.dirname(os.path.abspath(__file__))
DEBS_DIR = os.path.join(REPO, "debs")


def extract_control(deb_path):
    """从 deb 中提取 control 文件内容（无需 dpkg，用系统 ar+tar）"""
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ar", "-x", deb_path], cwd=td, check=True, capture_output=True)
        ctar = None
        for name in ("control.tar.xz", "control.tar.gz", "control.tar.bz2", "control.tar"):
            p = os.path.join(td, name)
            if os.path.exists(p):
                ctar = p
                break
        if not ctar:
            raise RuntimeError(f"{deb_path}: 未找到 control 压缩包")
        try:
            with tarfile.open(ctar) as t:
                t.extractall(td)
        except Exception:
            subprocess.run(["tar", "-xf", ctar, "-C", td], check=True)
        with open(os.path.join(td, "control"), "rb") as f:
            return f.read().decode("utf-8", "replace")


def file_hash(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    debs = sorted(f for f in os.listdir(DEBS_DIR) if f.endswith(".deb"))
    if not debs:
        print("错误: debs/ 目录下没有 .deb 文件")
        return 1

    entries = []
    archs = set()
    for fn in debs:
        path = os.path.join(DEBS_DIR, fn)
        control = extract_control(path).rstrip("\n")
        m = re.search(r"^Architecture:\s*(\S+)", control, re.M)
        if m:
            archs.add(m.group(1))
        size = os.path.getsize(path)
        entry = (
            f"{control}\n"
            f"Filename: debs/{fn}\n"
            f"Size: {size}\n"
            f"MD5sum: {file_hash(path, 'md5')}\n"
            f"SHA1: {file_hash(path, 'sha1')}\n"
            f"SHA256: {file_hash(path, 'sha256')}"
        )
        entries.append(entry)
        print(f"[+] {fn}  ({size} bytes)")

    packages_text = "\n\n".join(entries) + "\n"
    with open(os.path.join(REPO, "Packages"), "w", encoding="utf-8") as f:
        f.write(packages_text)
    with open(os.path.join(REPO, "Packages"), "rb") as f:
        raw = f.read()
    with gzip.open(os.path.join(REPO, "Packages.gz"), "wb") as f:
        f.write(raw)
    with bz2.open(os.path.join(REPO, "Packages.bz2"), "wb") as f:
        f.write(raw)

    date = email.utils.formatdate(localtime=True)

    def hashes(alg):
        lines = []
        for name in ("Packages", "Packages.gz", "Packages.bz2"):
            p = os.path.join(REPO, name)
            lines.append(f" {file_hash(p, alg)} {os.path.getsize(p)} {name}")
        return "\n".join(lines)

    release = (
        "Origin: 追风\n"
        "Label: 追风\n"
        "Suite: stable\n"
        "Version: 1.0\n"
        "Codename: zhuifeng\n"
        f"Architectures: {' '.join(sorted(archs))}\n"
        "Components: main\n"
        "Description: 追风 iOS 越狱源 (RootHide)\n"
        f"Date: {date}\n"
        f"MD5Sum:\n{hashes('md5')}\n"
        f"SHA1:\n{hashes('sha1')}\n"
        f"SHA256:\n{hashes('sha256')}\n"
    )
    with open(os.path.join(REPO, "Release"), "w", encoding="utf-8") as f:
        f.write(release)

    print("\n已生成: Packages, Packages.gz, Packages.bz2, Release")
    print(f"共 {len(debs)} 个插件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
