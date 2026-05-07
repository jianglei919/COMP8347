# COMP8347 课程工作区

这是 COMP8347 课程资料仓库，用于集中整理 Python 示例、实验文件和讲义资源。

## 目录

- [概览](#概览)
- [内容](#内容)
- [使用方法](#使用方法)
- [项目结构](#项目结构)
- [说明](#说明)

## 概览

这个工作区更像是一个轻量级学习资料仓库，而不是一个可部署的应用程序。当前内容主要包括第 1 周的 Python 入门示例、lab 1 提交材料以及课程讲义文档。

## 内容

- `code/week1/` 包含一些 Python 小脚本，用来演示字符串、列表、字典、嵌套循环以及日期/时间等基础语法。
- `labs/lab1/` 包含 lab 1 的说明文件和提交要求。
- `lectures/` 包含课程讲义、幻灯片和相关补充文档。
- `assignments/` 预留给后续作业相关内容。

## 使用方法

这个仓库没有构建步骤，也没有包管理器配置。要运行 Python 示例，可以直接在仓库根目录使用 `python3`，例如：

```bash
python3 code/week1/strings.py
python3 code/week1/lists.py
python3 code/week1/dictionaries.py
python3 code/week1/daytime.py
python3 code/week1/nestedloop1.py
python3 code/week1/nestedloop2.py
```

每个脚本都是独立的，会输出对应主题的简短演示结果。

## 项目结构

```text
COMP8347/
├── assignments/
├── code/
│   └── week1/
│       ├── daytime.py
│       ├── dictionaries.py
│       ├── lists.py
│       ├── nestedloop1.py
│       ├── nestedloop2.py
│       └── strings.py
├── labs/
│   └── lab1/
│       ├── Lab 1 Submit Requirement.pdf
│       └── Lab1.docx
├── lectures/
│   ├── COMP8347 Syllabus Summer 2026.pdf
│   ├── Lecture - 01.pdf
│   ├── Lecture - 01 - python.pdf
│   └── python-django-installation-stepsAJ.docx
└── README.md
```

## 说明

- 目前仓库还没有单一的主程序入口。
- 讲义文档同时包含 PDF 和 Word 两种格式。
- 如果后续作业加入了可复用代码，可以在这里补充所需的环境配置说明。
