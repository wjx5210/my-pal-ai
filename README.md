# My Pal AI

一个面向《幻兽帕鲁》的命令行 AI 攻略助手。项目以本地结构化帕鲁数据为知识源，结合实体匹配、向量检索和大语言模型，构建了一条可调试、可评估的混合 RAG 问答链路。

> 当前项目处于混合 RAG 原型阶段，重点验证知识构建、检索召回、上下文组装、回答生成和质量评估的完整流程。

## 项目状态

| 项目 | 当前实现 |
| --- | --- |
| 交互方式 | 命令行连续问答 |
| 知识库 | 18 个结构化帕鲁对象 |
| 检索方式 | 实体精确匹配 + 向量相似度检索 |
| 回答模型 | DeepSeek `deepseek-v4-flash` |
| Embedding | 阿里云百炼 `text-embedding-v3` |
| 向量存储 | 本地 JSON 文件 |
| 默认检索参数 | Top 3，最低相似度 0.7 |
| 可观测性 | 检索调试输出、Prompt/回答日志 |
| 测试规模 | 26 项，包含单元、集成和在线 AI 评估测试 |

## 核心能力

- 按完整名称或部分名称查询帕鲁
- 从自然语言问题中识别一个或多个帕鲁实体
- 使用向量检索召回语义相关的知识片段
- 合并实体资料与 RAG 召回结果，生成统一上下文
- 支持地点、战斗、工作、掉落、多帕鲁比较等问题
- 对知识不足的问题给出受限回答，降低无依据生成
- 为向量文档保存帕鲁名称、属性和推荐阶段元数据
- 支持检索结果、相似度和完整上下文的调试查看
- 可选记录问题、Prompt 和回答，便于排查回答质量
- 提供检索评估集与回答质量评估集
- 加载结构化知识时检查必需字段

## 系统流程

```text
data/pals.json
      │
      ├─ 数据校验
      │
      └─ 知识文本构建 → 百炼 Embedding → data/vector_store.json
                                                │
用户问题                                        │
   │                                            │
   ├─ 帕鲁实体匹配 ───────────────┐             │
   │                              │             │
   └─ 问题 Embedding → 向量检索 ──┴─→ 混合上下文
                                           │
                                           ↓
                                    DeepSeek 生成回答
                                           │
                              调试输出 / 问答日志 / 质量评估
```

当输入只匹配到一个帕鲁名称时，程序直接展示本地资料并生成单帕鲁攻略；其他自然语言问题统一进入混合 RAG 问答流程。

## 环境要求

- Python 3.10 或更高版本
- DeepSeek API Key，用于生成回答
- 阿里云百炼 API Key，用于生成文本向量
- 能够访问对应的模型 API

## 快速开始

### 1. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

在项目根目录创建 `.env`：

```dotenv
DEEPSEEK_API_KEY=你的_DeepSeek_API_Key
BAILIAN_API_KEY=你的_百炼_API_Key
```

`.env` 已被 Git 忽略。请勿把真实密钥写入 README、源码或提交记录。

### 4. 构建本地向量库

首次运行或修改 `data/pals.json` 后执行：

```bash
python scripts/build_vector_store.py
```

脚本会把每个帕鲁转换成知识文本，调用 Embedding API 生成向量，并保存到：

```text
data/vector_store.json
```

该文件由本地数据和 Embedding 模型生成，已加入 `.gitignore`，不提交到版本库。

### 5. 启动问答助手

请在项目根目录执行：

```bash
python -m app.main
```

输入 `exit` 退出程序。

## 使用示例

直接查询帕鲁：

```text
请输入帕鲁名称或提问：棉悠悠
```

询问工作能力：

```text
请输入帕鲁名称或提问：前期哪些帕鲁适合在基地伐木？
```

进行多帕鲁比较：

```text
请输入帕鲁名称或提问：棉悠悠和企丸丸哪个更值得前期培养？
```

查询资源来源：

```text
请输入帕鲁名称或提问：哪些帕鲁可以获得帕鲁的体液？
```

## 检索策略

混合检索由两部分组成：

1. **实体检索**：在问题中直接匹配知识库已有的帕鲁名称，保留完整结构化资料。
2. **向量检索**：将问题转换为向量，在本地向量库中计算余弦相似度，默认返回相似度不低于 `0.7` 的前 3 条结果。

两类结果会被统一整理为：

```python
{
    "entities": [],
    "knowledge": []
}
```

实体检索保证明确名称查询的准确性，向量检索则负责召回没有直接出现名称、但语义相关的帕鲁资料。

## 调试与日志

相关开关位于 `app/config.py`：

```python
DEBUG_RETRIEVAL = True
ENABLE_PROMPT_LOG = True
```

- `DEBUG_RETRIEVAL=True`：命令行显示召回文本及相似度分数。
- `ENABLE_PROMPT_LOG=True`：把问题、完整 Prompt 和模型回答追加到 `logs/qa.log`。

日志可能包含用户输入和模型上下文。在共享、上传或提交日志前，请先检查其中是否包含敏感信息。

## 项目结构

```text
my-pal-ai/
├─ app/
│  ├─ main.py                # 命令行入口
│  ├─ qa_service.py          # 统一问答入口及调试结果
│  ├─ hybrid_service.py      # 实体检索与 RAG 结果合并
│  ├─ rag_service.py         # 查询向量化与相似度检索
│  ├─ context_builder.py     # 混合上下文组装
│  ├─ embedding_service.py   # 百炼 Embedding API
│  ├─ vector_store.py        # 本地向量存储与余弦搜索
│  ├─ knowledge_builder.py   # 结构化数据转知识文本
│  ├─ pal_service.py         # 帕鲁数据加载和名称匹配
│  ├─ data_validator.py      # 知识库必需字段校验
│  ├─ ai_service.py          # Prompt 与回答生成
│  ├─ llm_client.py          # DeepSeek 客户端
│  ├─ logger_service.py      # 问答日志
│  ├─ intent_service.py      # 意图分类与白名单校验
│  ├─ context_service.py     # 意图式上下文筛选
│  └─ config.py              # 调试和日志开关
├─ data/
│  ├─ pals.json              # 结构化知识源
│  └─ vector_store.json      # 本地生成的向量库，Git 忽略
├─ evaluation/
│  ├─ questions.json         # 回答质量评估问题
│  └─ retrieval_questions.json # 检索召回评估问题
├─ scripts/
│  └─ build_vector_store.py  # 向量库构建脚本
├─ tests/                    # 单元、集成及在线评估测试
├─ logs/
│  └─ qa.log                 # 可选的问答日志
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

## 知识库结构

`data/pals.json` 当前包含 18 个帕鲁。每条数据采用以下结构：

```json
{
  "name": "帕鲁名称",
  "element": ["属性"],
  "summary": "简介",
  "work_suitability": {
    "工作类型": 1
  },
  "combat": {
    "positioning": "战斗定位",
    "strengths": ["优势"],
    "weaknesses": ["弱点"]
  },
  "drops": ["掉落物"],
  "locations": ["出现地点"],
  "recommended_stage": "推荐阶段",
  "recommendation": "推荐理由",
  "tips": "攻略提示"
}
```

修改知识源后，需要重新运行向量库构建脚本，否则语义检索仍会使用旧数据。

## 测试与评估

收集完整测试集：

```bash
python -m pytest --collect-only -q
```

运行全部测试：

```bash
python -m pytest -q
```

当前共收集 26 项测试，覆盖：

- 本地名称匹配与数据校验
- 意图分类和上下文构建
- Embedding 调用
- 余弦相似度、Top K、阈值与向量库持久化
- RAG 空结果和回答生成
- 实体检索与向量检索的混合流程
- 统一 QA 服务及调试信息
- LLM 异常降级、Prompt 约束和回答质量
- 检索召回与端到端 RAG 评估

部分测试会调用真实的 DeepSeek 或百炼 API，并要求已经生成 `data/vector_store.json`。因此完整测试集不是纯离线测试；运行前需配置两个 API Key、构建向量库并保证网络可用。`pytest.ini` 中的 `ai` 标记用于标识部分在线 AI 测试。

评估数据位于 `evaluation/`：

- `questions.json`：3 个端到端回答质量问题。
- `retrieval_questions.json`：3 个实体及知识召回问题。

## Git 演进记录

根据现有提交记录，项目经历了以下阶段：

1. **本地查询（2026-07-31 ～ 2026-08-01）**：完成名称查询、多结果选择和连续交互。
2. **AI 问答（2026-08-02）**：加入自然语言路由、本地上下文问答和多帕鲁比较。
3. **Agent 管线（2026-08-04）**：引入意图分类，打通意图识别、上下文选择与回答生成。
4. **稳定性与测试（2026-08-05 ～ 2026-08-06）**：统一模型客户端、增加异常处理、数据校验和测试覆盖，并扩充知识库。
5. **基础 RAG（2026-08-07）**：实现向量搜索、知识 Embedding、向量持久化和主流程集成，并加入阈值及空上下文处理。
6. **混合 RAG 与可观测性（2026-08-10）**：增加检索元数据、实体与向量混合检索、统一 QA 服务、调试输出、日志和质量评估体系。

## 当前限制

- 知识库只有 18 个帕鲁，无法覆盖完整游戏内容。
- 名称实体识别仍基于字符串匹配，不支持别名、错别字和语义实体抽取。
- 向量库需要在数据更新后手动重建，暂不支持增量更新。
- 本地 JSON 向量库适合原型验证，不适合大规模数据或高并发检索。
- 检索阈值、Top K、模型和服务地址目前主要写在代码中，尚未统一配置化。
- 当前只有命令行界面，没有 Web 页面或 HTTP API。
- 尚未实现多轮会话记忆、重排序器和自动化离线评估报告。

## 后续计划

- 扩充并持续核验帕鲁知识数据
- 增强数据类型、非空内容和嵌套结构校验
- 支持别名、模糊匹配和更稳健的实体识别
- 将模型、阈值、Top K 和路径统一迁移到配置层
- 增加向量库增量更新、版本检测和自动重建
- 完善测试标记，明确区分纯单元测试与在线 API 测试
- 引入重排序、答案来源展示和自动评估报告
- 封装 HTTP API，并提供简单的 Web 界面

## 免责声明

本项目用于学习和验证 AI Agent、RAG、提示词设计与本地知识增强流程，与游戏开发商及发行商无关。模型生成内容可能存在误差，具体游戏信息请以实际游戏版本为准。
