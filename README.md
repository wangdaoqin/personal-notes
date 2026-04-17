# 笔记管理系统

一个静态笔记管理网站，实现本地笔记的自动同步与可视化展示。通过文件系统的简单操作（增删改文件）自动更新网站内容，无需手动编辑网页代码。

## 核心功能

### 1. 动态分类管理系统
- **自动发现机制**：能够自动识别 `notes/` 目录下的所有子文件夹作为笔记分类
- **实时同步**：在任意分类下新增文件夹时，网站自动识别为新分类板块
- **无限层级支持**：支持分类→子分类的层级结构（如 `R语言/基础教程/`、`R语言/高级技巧/`）

### 2. 多格式文件支持
- **Markdown文件**：自动解析渲染，支持代码高亮、数学公式、图表
- **HTML文件**：无缝嵌入展示，保持原始格式
- **PDF文件**：内嵌查看器，可直接在线预览
- **扩展性**：预留接口，未来可添加Word、Excel、图片等格式支持

### 3. 智能构建与同步
- **监听模式**：监控 `notes/` 目录变化，文件变动时自动重新构建
- **增量更新**：仅更新变更文件，提高构建效率
- **配置化**：通过 `config.json` 自定义网站主题、布局、排序规则

### 4. 专业前端界面
- **响应式设计**：适配桌面、平板、手机
- **搜索功能**：全文搜索（标题+内容）
- **排序过滤**：按文件名、修改时间、文件类型排序
- **暗色/亮色主题**：支持切换
- **访问统计**：页面访问量记录

## 项目结构

```
E:/personal-notes/
├── .github/workflows/          # GitHub Actions 自动化部署
│   └── deploy.yml
├── notes/                      # 笔记源文件（.gitignore排除）
│   ├── R语言/
│   │   ├── 基础语法.md
│   │   ├── 数据分析实战.html
│   │   ├── 统计模型.pdf
│   │   └── advanced/          # 子分类示例
│   │       └── 高级可视化.md
│   ├── 公共卫生/
│   │   ├── 流行病学基础.md
│   │   └── 卫生政策分析.pdf
│   ├── 生活/
│   │   └── 旅行计划.md
│   └── CFETP/                 # 新增分类示例
│       └── 现场流行病学.md
├── scripts/                    # 构建脚本
│   ├── build.py               # 主构建脚本
│   ├── sync.py               # 文件变化监听
│   ├── generate_index.py     # 索引生成
│   └── utils/               # 工具函数
├── templates/                 # 网站模板
│   ├── base.html             # 基础模板
│   ├── category.html        # 分类页面模板
│   ├── note.html           # 笔记详情模板
│   └── search.html         # 搜索页面模板
├── static/                   # 静态资源
│   ├── css/                  # 样式文件
│   ├── js/                   # JavaScript文件
│   └── lib/                 # 第三方库
├── docs/                    # 构建输出目录（GitHub Pages根目录）
├── config.json             # 配置文件
├── requirements.txt        # Python依赖
├── .gitignore
└── README.md
```

## 安装与使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 添加笔记

在 `notes/` 目录下创建文件夹和文件，例如：
- 创建 `R语言/` 文件夹
- 在其中添加 `基础语法.md` 文件
- 可以创建子文件夹，如 `R语言/advanced/`

### 3. 构建网站

```bash
python scripts/build.py
```

构建完成后，网站文件会生成在 `docs/` 目录中。

### 4. 启动监听模式

```bash
python scripts/sync.py
```

这样，当你在 `notes/` 目录中添加、修改或删除文件时，网站会自动重新构建。

### 5. 部署到GitHub Pages

1. 将项目推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages，选择 `docs/` 目录作为发布源
3. 每次推送代码后，GitHub Actions会自动构建并部署网站

## 配置说明

在 `config.json` 文件中，你可以自定义以下配置：

- `site_name`：网站名称
- `theme`：默认主题（light/dark）
- `sort_by`：文件排序方式（mtime/name）
- `show_sidebar`：是否显示侧边栏
- `enable_search`：是否启用搜索功能
- `enable_theme_switch`：是否启用主题切换
- `footer_text`：页脚文本

## 支持的文件格式

- **.md**：Markdown文件，会自动渲染
- **.html**：HTML文件，会通过iframe嵌入
- **.pdf**：PDF文件，会通过PDF.js查看器嵌入

## 技术栈

- **后端**：Python (markdown2, watchdog, jinja2, python-frontmatter)
- **前端**：HTML, CSS, JavaScript
- **构建工具**：自定义Python脚本
- **部署**：GitHub Pages

## 许可证

MIT License