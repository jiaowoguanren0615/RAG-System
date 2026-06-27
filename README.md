# RAG-System · 医药企业知识库问答

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

面向医药企业的 **检索增强生成（RAG）** 系统，支持 SOP、产品说明书、法规等内部文档的智能问答。

> **核心能力**：混合检索 · 答案引用溯源 · 文档版本管理 · RBAC 权限 · 审计日志

> ⚠️ **免责声明**：本系统仅用于企业内部知识查阅辅助，不构成临床、注册或用药建议。请以最新批准文件及主管部门意见为准。

---

## 目录

- [功能特性](#功能特性)
- [架构概览](#架构概览)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [API 概览](#api-概览)
- [文档类型与分块策略](#文档类型与分块策略)
- [评测体系](#评测体系)
- [安全与合规](#安全与合规)
- [实施路线图](#实施路线图)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 功能特性

- **多格式文档接入**：PDF / Word / Excel，支持扫描件 OCR
- **混合检索**：向量语义 + 关键词（BM25）+ 元数据过滤（产品、部门、文档类型、生效版本）
- **可溯源回答**：每条回答附带文档名、版本、页码/章节引用
- **企业级治理**：角色权限、密级过滤、问答审计、人工反馈闭环
- **版本管理**：索引与生效日期绑定，归档文档可检索但标注「已失效」
- **评测体系**：Citation 准确率、拒答率、版本正确率等指标

---

## 架构概览

```mermaid
flowchart TB
    subgraph ingest [文档接入层]
        A1[文件上传 / API]
        A2[格式解析 PDF/Word/Excel]
        A3[OCR 扫描件]
        A4[元数据抽取]
    end

    subgraph process [索引流水线]
        B1[清洗与去噪]
        B2[分块 Chunking]
        B3[Embedding]
        B4[向量库 + 全文检索]
    end

    subgraph serve [问答服务层]
        C1[Query 理解 / 改写]
        C2[混合检索]
        C3[重排序 Rerank]
        C4[LLM 生成 + 引用]
        C5[置信度 / 拒答]
    end

    subgraph gov [治理与合规]
        D1[RBAC 权限]
        D2[审计日志]
        D3[版本管理]
        D4[人工反馈]
    end

    subgraph ui [应用层]
        E1[Web 问答]
        E2[管理后台]
        E3[API 对接 OA/DMS]
    end

    ingest --> process --> serve
    gov --> ingest
    gov --> serve
    serve --> ui
```

| 模块 | 职责 |
|------|------|
| **Ingestion** | 文档解析、元数据抽取、版本绑定 |
| **Retrieval** | 向量库 + 全文检索 + Rerank |
| **Generation** | 约束式 Prompt、拒答策略、引用格式化 |
| **Governance** | RBAC、审计、反馈闭环 |

---

## 技术栈

| 类别 | 选型 |
|------|------|
| 后端 | FastAPI |
| RAG 框架 | LlamaIndex / LangChain |
| 向量库 | Milvus / Qdrant / pgvector |
| 全文检索 | Elasticsearch / OpenSearch（可选） |
| Embedding | BGE-M3 |
| LLM | Qwen2.5 / DeepSeek（支持本地部署） |
| 任务队列 | Celery + Redis |
| 前端 | React + Ant Design |
| 对象存储 | MinIO |
| 关系数据库 | PostgreSQL（元数据 / 用户 / 审计） |
| 部署 | Docker Compose → Kubernetes |

---

## 项目结构

```
RAG-System/
├── apps/
│   ├── api/                 # FastAPI 问答 & 管理 API
│   ├── worker/              # Celery 异步索引任务
│   └── web/                 # 前端
├── packages/
│   ├── core/                # 领域模型、配置
│   ├── ingestion/           # 解析、OCR、元数据
│   ├── chunking/            # 分块策略（按 doc_type 插件化）
│   ├── retrieval/           # 混合检索 + Rerank
│   ├── generation/          # Prompt、引用、拒答
│   └── governance/          # RBAC、审计、版本
├── configs/
│   ├── chunking/            # 各文档类型分块规则
│   └── prompts/             # 系统 Prompt 模板
├── eval/                    # 评测集、RAGAS / 自定义指标
├── infra/
│   ├── docker/
│   └── k8s/
├── scripts/                 # 批量导入、重建索引
├── tests/
└── docs/
    ├── architecture.md
    └── compliance.md
```

---

## 快速开始

### 环境要求

- Python 3.11+
- Docker & Docker Compose
- （可选）NVIDIA GPU，用于本地 Embedding / LLM

### 1. 克隆仓库

```bash
git clone https://github.com/jiaowoguanren0615/RAG-System.git
cd RAG-System
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

至少配置以下变量：

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/pharma_rag
VECTOR_DB_URL=http://localhost:6333
EMBEDDING_MODEL=BAAI/bge-m3
LLM_MODEL=qwen2.5-72b-instruct
LLM_API_BASE=http://localhost:8001/v1
LLM_API_KEY=your-api-key
DEFAULT_DOC_STATUS_FILTER=active
```

### 3. 启动服务

```bash
docker compose up -d
```

本地开发模式：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn apps.api.main:app --reload
```

### 4. 导入文档并提问

```bash
# 上传文档
curl -X POST http://localhost:8000/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@docs/examples/sample-sop.pdf"

# 问答
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"question": "该 SOP 中取样频率要求是什么？"}'
```

- Web 界面：`http://localhost:3000`
- API 文档：`http://localhost:8000/docs`

---

## 配置说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `DATABASE_URL` | PostgreSQL 连接 | `postgresql://...` |
| `VECTOR_DB_URL` | 向量库连接 | `http://localhost:6333` |
| `EMBEDDING_MODEL` | Embedding 模型 | `BAAI/bge-m3` |
| `LLM_MODEL` | 对话模型 | `qwen2.5-72b-instruct` |
| `LLM_API_BASE` | LLM 服务地址 | `http://localhost:8001/v1` |
| `DEFAULT_DOC_STATUS_FILTER` | 默认只检索生效文档 | `active` |
| `REDIS_URL` | Celery 消息队列 | `redis://localhost:6379/0` |

---

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/v1/chat` | 流式问答（含 citations） |
| `POST` | `/v1/documents/upload` | 上传并触发索引 |
| `GET` | `/v1/documents` | 文档列表、版本、状态 |
| `POST` | `/v1/documents/{id}/reindex` | 版本更新后重建索引 |
| `GET` | `/v1/audit/logs` | 审计日志查询 |
| `POST` | `/v1/feedback` | 用户反馈（点赞 / 纠错） |

**问答响应示例：**

```json
{
  "answer": "根据现行 SOP，取样频率为每批次生产前、中、后各一次……",
  "citations": [
    {
      "doc_id": "uuid",
      "title": "生产取样 SOP",
      "version": "v2.1",
      "page": 12,
      "section": "4.2 取样频次",
      "snippet": "……"
    }
  ],
  "confidence": "high",
  "disclaimer": "以上内容仅供内部查阅，不构成注册或临床意见。"
}
```

---

## 文档类型与分块策略

| 文档类型 | 分块方式 | 关键元数据 |
|----------|----------|------------|
| SOP / 制度 | 按章节 / 条款 | 版本、生效日期、部门 |
| 说明书 / 标签 | 按固定段落（适应症、用法用量等） | 产品编码、批准日期 |
| 法规 | 按条 / 款 / 项 | 法规编号、发布机关 |
| 表格 | 整表或按行组，保留表头上下文 | 页码、所属章节 |

**文档元数据模型：**

```python
{
    "doc_id": "uuid",
    "title": "产品说明书-XX片",
    "doc_type": "label | sop | regulation | clinical | pv | spec",
    "department": "注册部",
    "product_code": "P001",
    "version": "v2.1",
    "effective_date": "2025-01-01",
    "status": "active | archived",
    "classification": "internal | confidential"
}
```

---

## 评测体系

建立 **100–500 条黄金问答集**，定期回归评测：

```bash
python -m eval.run --dataset eval/golden_qa.json
```

| 指标 | 说明 | 目标 |
|------|------|------|
| **Citation Accuracy** | 引用片段是否支撑答案 | ≥ 90% |
| **Answer Accuracy** | 与标准答案一致性 | ≥ 85% |
| **Refusal Rate** | 无依据时是否正确拒答 | ≥ 95% |
| **Version Accuracy** | 是否引用生效版本 | ≥ 98% |
| **Permission Leakage** | 无权限文档是否被检索 | 0 |

---

## 安全与合规

- **RBAC**：按部门 / 角色 / 文档密级过滤检索与展示
- **审计日志**：记录用户、时间、问题、引用文档，支持合规审查
- **版本优先**：检索前过滤 `status=active` 且 `effective_date <= today`
- **数据不出域**：建议私有化部署（Docker / K8s），敏感数据保留在企业内网
- **低幻觉策略**：仅依据参考片段回答；信息不足时明确拒答
- **界面提示**：区分「法规要求」与「企业内部 SOP」，避免被当作医学决策系统

---

## 实施路线图

| 阶段 | 周期 | 交付物 |
|------|------|--------|
| **P0 POC** | 2–3 周 | 单类文档（SOP）+ 混合检索 + 引用 + Docker 部署 |
| **P1 MVP** | 4–6 周 | 多格式解析、RBAC、审计、管理后台 |
| **P2 生产** | 6–8 周 | 版本管理、批量导入、评测体系、高可用 |
| **P3 增强** | 持续 | 同义词库、知识图谱、多轮对话、DMS 集成 |

- [ ] P0 POC
- [ ] P1 MVP
- [ ] P2 生产
- [ ] P3 增强

---

## 贡献指南

1. Fork 本仓库并创建功能分支
2. 提交前运行测试与 lint

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

3. 提交 Pull Request，描述变更内容与测试方式

---

## 许可证

[MIT](LICENSE) © Howard
