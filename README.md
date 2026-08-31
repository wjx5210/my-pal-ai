# My Pal AI

一个面向《幻兽帕鲁》的全栈 AI 图鉴助手。项目以本地结构化帕鲁数据为知识源，结合图鉴筛选、实体匹配、向量检索、会话记忆和大语言模型，提供可浏览、可追问、可解释的混合 RAG 攻略体验。

> 当前项目处于混合 RAG 原型阶段，重点验证知识构建、检索召回、上下文组装、回答生成和质量评估的完整流程。

在线体验：[https://mypalai.space](https://mypalai.space)

## 项目状态

| 项目 | 当前实现 |
| --- | --- |
| 交互方式 | React 图鉴网站 + 命令行问答 |
| 知识库 | 100 个结构化帕鲁对象 |
| 检索方式 | 实体精确匹配 + 向量相似度检索 |
| 回答模型 | DeepSeek `deepseek-v4-flash` |
| Embedding | 阿里云百炼 `text-embedding-v3` |
| 向量存储 | 本地 JSON 文件 |
| 默认检索参数 | Top 3，最低相似度 0.7 |
| 可观测性 | 检索调试输出、Prompt/回答日志 |
| 会话能力 | 最近 12 条消息记忆、追问检索、本地历史恢复 |
| 测试规模 | 34 项，包含单元、API、集成和在线 AI 评估测试 |

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
- 以图鉴卡片浏览帕鲁，并按名称、属性和工作适应性筛选
- 点击帕鲁进入完整详情页，并按需生成 AI 培养总结
- 保存当前浏览器中的对话记录，支持清空会话与连续追问

## 工程亮点

- **完整 AI 应用链路**：独立打通数据采集与清洗、知识构建、混合检索、大模型回答、Web 交互、测试评估和服务器部署。
- **混合 RAG 检索**：将实体名称匹配与向量相似度检索结合，兼顾明确对象查询的准确性和自然语言问题的语义召回能力。
- **受限回答与异常降级**：通过上下文组装、Prompt 约束、相似度阈值和空结果处理，减少知识不足时的无依据生成。
- **多轮会话体验**：后端按会话 ID 保留最近 12 条消息，结合历史问题补全短追问；前端支持会话恢复与清空。
- **可测试、可观测**：34 项测试覆盖数据、检索、AI 问答、API 和会话流程，并提供检索相似度、Prompt 与回答日志用于问题定位。
- **全栈部署实践**：使用 FastAPI、React、TypeScript、Docker Compose 和 Nginx 完成前后端开发及 Linux 云服务器部署。

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

### 5. 启动 FastAPI 后端

```bash
uvicorn app.api.server:app --reload
```

后端默认运行在 `http://127.0.0.1:8000`，接口文档位于 `http://127.0.0.1:8000/docs`。

### 6. 启动 React 前端

打开另一个终端：

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。如果后端地址不同，可在前端环境变量中设置：

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 7. 启动命令行助手（可选）

请在项目根目录执行：

```bash
python -m app.main
```

输入 `exit` 退出程序。

## Web 功能

- 首页展示 100 个帕鲁的响应式图鉴卡片。
- 支持按名称或简介搜索，并按属性、基地工作筛选。
- 首页内置 RAG 聊天面板，可连续追问和查看参考帕鲁。
- 浏览器保存当前对话；后端通过会话 ID 保留最近 12 条消息。
- 短追问会结合最近用户问题重新检索，例如“那它适合基地吗？”。
- 详情页展示属性、工作能力、战斗定位、优缺点、地点、掉落和培养建议。
- 详情页可根据当前图鉴资料生成 AI 总结。

## API 接口

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `GET` | `/health` | 服务健康检查 |
| `GET` | `/pals` | 获取完整图鉴列表 |
| `GET` | `/pal/{name}` | 获取单个帕鲁详情 |
| `POST` | `/pal/{name}/summary` | 生成单个帕鲁 AI 总结 |
| `POST` | `/ask` | 带会话 ID 的混合 RAG 问答 |
| `GET` | `/sessions/{session_id}` | 获取会话历史 |
| `DELETE` | `/sessions/{session_id}` | 清空会话上下文 |

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
│  ├─ config.py              # 调试和日志开关
│  ├─ conversation_service.py # 有界会话历史与上下文记忆
│  └─ api/
│     └─ server.py           # FastAPI 图鉴、问答和会话接口
├─ data/
│  ├─ pals.json              # 结构化知识源
│  └─ vector_store.json      # 本地生成的向量库，Git 忽略
├─ evaluation/
│  ├─ questions.json         # 回答质量评估问题
│  └─ retrieval_questions.json # 检索召回评估问题
├─ scripts/
│  └─ build_vector_store.py  # 向量库构建脚本
├─ tests/                    # 单元、集成及在线评估测试
├─ frontend/                 # React + TypeScript + Vite 图鉴网站
│  └─ src/
│     ├─ pages/              # 图鉴首页与帕鲁详情页
│     └─ components/         # RAG 聊天、图鉴卡片与来源链接
├─ logs/
│  └─ qa.log                 # 可选的问答日志
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

## 知识库结构

`data/pals.json` 当前包含从 PalDB 图鉴顺序采集的前 100 个帕鲁。每条数据采用以下结构：

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

## PalDB 数据采集

项目提供低频、可缓存、可续跑的采集脚本，用于生成图鉴顺序前 100 个帕鲁的结构化数据：

```bash
python scripts/crawl_paldb.py --limit 100 --delay 2
```

默认输出：

- `data/imported/paldb_first_100.json`：清洗后的兼容知识库。
- `data/raw/paldb/`：原始 HTML 缓存，不提交 Git。
- `data/manifests/paldb_first_100.json`：URL、采集时间、状态和内容哈希。

采集器使用单线程、请求间隔、超时重试、可识别 User-Agent 和本地缓存。详情事实保存在 `wiki` 字段中，包括图鉴编号、伙伴技能、基础属性、移动能力、主动技能和来源 URL；`combat`、推荐阶段等攻略字段由本地规则派生。

重新采集前请确认来源网站的服务条款和自动访问许可，不要绕过验证码、登录或访问限制。修改结构化数据后仍需重新构建向量库。

## 测试与评估

收集完整测试集：

```bash
python -m pytest --collect-only -q
```

运行全部测试：

```bash
python -m pytest -q
```

当前共收集 34 项测试，覆盖：

- 本地名称匹配与数据校验
- 意图分类和上下文构建
- Embedding 调用
- 余弦相似度、Top K、阈值与向量库持久化
- RAG 空结果和回答生成
- 实体检索与向量检索的混合流程
- 统一 QA 服务及调试信息
- LLM 异常降级、Prompt 约束和回答质量
- 检索召回与端到端 RAG 评估
- FastAPI 健康检查、图鉴列表、详情、404、会话问答和 AI 总结

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
7. **全栈图鉴与会话助手（2026-08-11）**：加入 FastAPI 接口、React 图鉴、详情页、多轮会话记忆、追问检索和详情 AI 总结。

## 当前限制

- 当前只采集了 PalDB 图鉴顺序中的前 100 个帕鲁，尚未覆盖完整游戏内容。
- 名称实体识别仍基于字符串匹配，不支持别名、错别字和语义实体抽取。
- 向量库需要在数据更新后手动重建，暂不支持增量更新。
- 本地 JSON 向量库适合原型验证，不适合大规模数据或高并发检索。

## 国内云服务器部署

项目已经提供 Docker Compose 生产配置，适用于 Ubuntu 服务器。部署结构为 Nginx 静态托管 React，并通过同域 `/api` 反向代理 FastAPI，因此使用公网 IP 测试时不需要单独配置跨域。

### 服务器准备

建议使用 Ubuntu 24.04、2 核 4 GB 或更高配置，并安装 Docker Engine 与 Docker Compose Plugin。云防火墙仅需开放 `22`、`80`；备案和证书完成后再开放 `443`。

### 上传与配置

将项目上传或拉取到服务器，确认以下文件存在：

```text
data/pals.json
data/vector_store.json
```

向量库属于部署所需的只读产物。知识数据变化后，应先在可信环境重新执行 `python scripts/build_vector_store.py`，再将生成结果部署到服务器，避免每次构建容器都重复调用 Embedding API。

创建生产环境变量：

```bash
cp .env.production.example .env.production
```

编辑 `.env.production`，填写：

```dotenv
DEEPSEEK_API_KEY=你的DeepSeek密钥
BAILIAN_API_KEY=你的百炼密钥
ALLOWED_ORIGINS=
ENABLE_PROMPT_LOG=false
DEBUG_RETRIEVAL=false
```

`.env.production` 已被 Git 忽略。前后端默认同域访问，`ALLOWED_ORIGINS` 可以留空；如果后续拆分前后端域名，再填写允许的完整来源地址，多个地址使用英文逗号分隔。

### 启动与检查

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

也可以直接运行：

```bash
docker compose up -d --build
```

检查服务：

```bash
docker compose ps
docker compose logs --tail=100
curl http://127.0.0.1/health
curl http://127.0.0.1/api/health
```

域名备案完成前，可通过 `http://服务器公网IP` 验证页面。备案完成并解析域名后，再为 Nginx 增加 SSL 证书和 `443` 配置。

AI 问答和详情总结接口已在 Nginx 层按公网 IP 限制为平均每分钟 5 次，并允许少量突发请求。正式公开前仍应在 DeepSeek 和百炼控制台配置余额预警及调用额度。
- 检索阈值、Top K、模型和服务地址目前主要写在代码中，尚未统一配置化。
- 会话历史当前保存在单个后端进程内，服务重启后会丢失，也不适合多实例部署。
- 图鉴卡片目前使用属性视觉标识，尚未接入帕鲁图片资源。
- 尚未实现用户账户、跨设备历史同步、重排序器和自动化离线评估报告。

## 后续计划

- 扩充并持续核验帕鲁知识数据
- 增强数据类型、非空内容和嵌套结构校验
- 支持别名、模糊匹配和更稳健的实体识别
- 将模型、阈值、Top K 和路径统一迁移到配置层
- 增加向量库增量更新、版本检测和自动重建
- 完善测试标记，明确区分纯单元测试与在线 API 测试
- 引入重排序、答案来源展示和自动评估报告
- 将会话历史迁移到持久化存储，并支持多个会话的管理与命名
- 接入有授权的帕鲁图片资源和图片回退策略
- 增加前端端到端测试、加载骨架和更完整的无障碍支持

## 免责声明

本项目用于学习和验证 AI Agent、RAG、提示词设计与本地知识增强流程，与游戏开发商及发行商无关。模型生成内容可能存在误差，具体游戏信息请以实际游戏版本为准。
