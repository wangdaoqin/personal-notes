# 静态笔记管理网站 - 完整使用指南

## 目录
1. [项目简介](#项目简介)
2. [快速开始](#快速开始)
3. [本地使用](#本地使用)
4. [部署到GitHub Pages](#部署到github-pages)
5. [使用方法](#使用方法)
6. [常见问题](#常见问题)

---

## 项目简介

这是一个**静态笔记管理网站**，可以帮助你轻松管理和展示多种格式的笔记文件（Markdown、HTML、PDF）。

### 核心特性

- ✅ **自动同步** - 在notes文件夹中添加/编辑文件，网站自动更新
- ✅ **多格式支持** - 支持.md、.html、.pdf文件
- ✅ **分类管理** - 通过文件夹自动分类
- ✅ **响应式设计** - 支持手机、平板、电脑访问
- ✅ **暗色模式** - 支持切换明暗主题
- ✅ **全文搜索** - 快速查找笔记内容
- ✅ **免费托管** - 部署到GitHub Pages无需服务器费用

---

## 快速开始

### 第一步：安装Python

1. 访问 https://www.python.org/downloads/
2. 下载最新版本的Python（建议Python 3.8或更高版本）
3. 运行安装程序，**重要**：勾选"Add Python to PATH"
4. 点击"Install Now"

### 第二步：安装依赖

打开命令提示符（Win+R，输入cmd，回车），依次执行：

```bash
cd E:\personal-notes
pip install -r requirements.txt
```

### 第三步：构建网站

```bash
python scripts/build.py
```

### 第四步：本地预览

双击打开 `E:\personal-notes\docs\index.html` 即可在浏览器中预览网站。

---

## 本地使用

### 方式一：手动构建（推荐）

每次添加或修改笔记后，运行：

```bash
python scripts/build.py
```

### 方式二：自动监听模式

启动后，当你在notes文件夹中添加/修改/删除文件时，网站会自动重新构建：

```bash
python scripts/sync.py
```

> 注意：此模式会持续运行，适合开发调试时使用。

---

## 部署到GitHub Pages

### 第一步：创建GitHub账号

1. 访问 https://github.com/
2. 点击"Sign up"注册账号
3. 完成邮箱验证

### 第二步：创建新仓库

1. 登录GitHub后，点击右上角"+" → "New repository"
2. Repository name填：`personal-notes`（或其他你喜欢的名字）
3. 选择"Public"（公开仓库才能使用GitHub Pages免费版）
4. 点击"Create repository"

### 第三步：上传代码

在命令提示符中执行：

```bash
cd E:\personal-notes

# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/personal-notes.git

# 推送代码
git branch -M main
git push -u origin main
```

### 第四步：启用GitHub Pages

1. 在GitHub仓库页面，点击"Settings"（设置）
2. 左侧菜单找到"Pages"
3. Source部分选择：
   - Branch: `main`
   - Folder: `/ (root)`
   - 点击"Save"
4. 等待1-2分钟，页面会显示你的网站地址

### 第五步：访问你的网站

在GitHub Pages设置页面，你会看到类似这样的链接：
```
https://YOUR_USERNAME.github.io/personal-notes/
```

这就是你的网站地址，可以分享给任何人访问！

---

## 使用方法

### 添加新笔记

1. 在`notes`文件夹中创建或选择分类文件夹
2. 添加.md、.html或.pdf文件
3. 重新构建网站

**示例：添加R语言笔记**
```
notes/R语言/数据可视化.md
```

**示例：添加子分类**
```
notes/R语言/基础教程/入门指南.md
```

### 笔记文件格式

#### Markdown文件（推荐）

```markdown
---
title: 我的笔记标题
tags:
  - 标签1
  - 标签2
summary: 简短描述
---

# 笔记正文

这里是笔记内容...
```

#### HTML文件

直接写入完整的HTML代码即可。

#### PDF文件

将PDF文件直接放入分类文件夹即可。

### 配置网站

编辑`config.json`文件：

```json
{
    "site_name": "我的笔记",
    "theme": "light",
    "sort_by": "mtime",
    "show_sidebar": true,
    "enable_search": true,
    "enable_theme_switch": true
}
```

---

## 常见问题

### Q: 构建失败怎么办？

确保：
1. Python已正确安装（运行`python --version`检查）
2. 依赖已安装（运行`pip install -r requirements.txt`）
3. notes文件夹存在且有文件

### Q: 网站显示空白怎么办？

检查浏览器控制台（F12）是否有错误，并确保docs文件夹中有index.html文件。

### Q: 如何更新网站内容？

1. 本地：修改notes文件夹中的文件，然后运行`python scripts/build.py`
2. GitHub：推送代码后，GitHub Actions会自动构建和部署

### Q: 可以自定义域名吗？

可以！在GitHub Pages设置中添加你的自定义域名即可。

---

## 项目结构说明

```
E:\personal-notes\
├── notes/              # 放置你的笔记文件
│   ├── R语言/          # 分类文件夹
│   └── 生活/
├── scripts/           # 构建脚本（一般不需要修改）
├── templates/         # 网站模板（一般不需要修改）
├── static/            # 静态资源（CSS、JS）
├── docs/              # 构建输出的网站文件
├── config.json        # 网站配置
└── requirements.txt   # Python依赖
```

---

## 示例笔记

项目已包含两个示例笔记：

1. **R语言教程.html** - 位于 `notes/R语言/` 文件夹
   - 包含R语言基础语法介绍和示例代码

2. **vibe coding心得.md** - 位于 `notes/生活/` 文件夹
   - 关于编程氛围和效率的个人感悟

---

祝使用愉快！🚀