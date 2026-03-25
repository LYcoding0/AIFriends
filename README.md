# AIFriends

一个基于 `Vue 3 + Django + LangChain/LangGraph` 的 AI 角色社交项目。

项目的核心思路不是传统“用户与用户聊天”，而是“用户创建 AI 角色、进入角色空间、与角色持续对话”，并在对话过程中叠加：

- 文本聊天
- 语音识别（ASR）
- 语音合成（TTS）
- 角色音色选择
- 对话长期记忆
- 简单知识库检索

当前仓库同时包含：

- 前端源码：`frontend/`
- Django 后端源码：`backend/`
- Django 静态打包产物目录：`backend/static/frontend/`

## 1. 项目特性

### 1.1 用户系统

- 用户注册 / 登录
- JWT 鉴权
- Access Token 自动刷新
- 用户资料编辑
- 用户头像上传
- 个人空间查看

### 1.2 角色系统

- 创建角色
- 编辑角色
- 删除角色
- 角色头像上传
- 角色聊天背景上传
- 角色音色选择
- 角色列表展示

### 1.3 对话系统

- 与 AI 角色建立会话
- 流式返回聊天结果（SSE）
- 显示历史消息
- 记录 token 消耗
- 长期记忆更新

### 1.4 语音能力

- 麦克风录音
- VAD 语音活动检测
- PCM 音频上传
- ASR 语音转文字
- TTS 文字转语音
- 按角色音色播放语音

### 1.5 知识库能力

- 读取本地文档
- 文本切分
- 向量化写入 LanceDB
- 对话时按相似度检索知识片段

## 2. 技术栈

### 2.1 前端

- `Vue 3`
- `Vite`
- `Vue Router 4`
- `Pinia`
- `Axios`
- `Tailwind CSS 4`
- `DaisyUI`
- `@microsoft/fetch-event-source`
- `@ricky0123/vad-web`
- `Croppie`

### 2.2 后端

- `Python`
- `Django 6`
- `Django REST Framework`
- `SimpleJWT`
- `django-cors-headers`
- `Pillow`
- `python-dotenv`

### 2.3 AI / 检索

- `LangChain`
- `LangGraph`
- `langchain-openai`
- `OpenAI Compatible API`
- `LanceDB`

## 3. 整体架构

### 3.1 前后端关系

开发阶段有两种常见使用方式：

1. 前后端分离开发
   - 前端跑在 `Vite`
   - 后端跑在 `Django`
   - 前端通过 HTTP 调 Django API

2. Django 集成静态部署
   - 前端打包到 `backend/static/frontend/`
   - Django 直接返回模板页和静态资源

### 3.2 鉴权方式

当前项目采用：

- `Access Token`：前端内存保存，放在 `Authorization: Bearer ...`
- `Refresh Token`：通过 `HttpOnly Cookie` 保存
- 前端在 `401` 时自动请求 `/api/user/account/refresh_token/` 刷新 token

对应前端逻辑位于：

- `frontend/src/js/http/api.js`

### 3.3 AI 对话链路

一次聊天的大致流程如下：

1. 前端发送消息到 `/api/friend/message/chat/`
2. 后端构造系统提示词 + 历史消息 + 用户输入
3. LangGraph 调用大模型生成回复
4. 回复文本通过 SSE 流式返回前端
5. 同时把文本增量送入 TTS WebSocket，返回音频分片
6. 前端边显示文本边播放音频
7. 消息落库
8. 长期记忆更新

## 4. 目录结构

```text
AIFriends/
├─ backend/
│  ├─ backend/                     # Django 项目配置
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ ...
│  ├─ web/                         # 主业务 app
│  │  ├─ admin.py
│  │  ├─ models/
│  │  │  ├─ user.py
│  │  │  ├─ character.py
│  │  │  └─ friend.py
│  │  ├─ views/
│  │  │  ├─ user/                  # 用户、登录、资料
│  │  │  ├─ create/character/      # 角色创建、更新、音色
│  │  │  ├─ friend/                # 好友/会话
│  │  │  └─ homepage/              # 首页列表
│  │  ├─ documents/                # 知识库原始文本 + 向量库
│  │  └─ templates/
│  ├─ media/                       # 上传文件
│  ├─ static/                      # Django 静态目录
│  ├─ manage.py
│  └─ .env                         # 后端环境变量（本地）
├─ frontend/
│  ├─ public/
│  │  └─ vad/                      # VAD 运行所需资源
│  ├─ src/
│  │  ├─ components/
│  │  ├─ views/
│  │  ├─ router/
│  │  ├─ stores/
│  │  └─ js/
│  ├─ package.json
│  └─ vite.config.js
├─ requirements.txt                # 完整 Python 依赖
├─ README.md
└─ main.py                         # PyCharm 默认示例文件，非项目入口
```

## 5. 核心数据模型

### 5.1 用户

- `User`：Django 内置用户表
- `UserProfile`
  - 头像
  - 简介
  - 创建时间 / 更新时间

### 5.2 角色

- `Voice`
  - 音色名称
  - 第三方音色 ID

- `Character`
  - 作者
  - 角色名
  - 角色头像
  - 音色
  - 角色设定 / 简介
  - 聊天背景图

### 5.3 会话

- `Friend`
  - 当前用户与角色之间的“会话关系”
  - 包含长期记忆字段

- `Message`
  - 用户输入
  - 模型输出
  - 原始 prompt 片段
  - token 使用量

- `SystemPrompt`
  - 后台可维护的系统提示词模板
  - 支持按顺序拼接

## 6. 运行环境要求

推荐版本：

- `Python 3.11+`
- `Node.js 20.19+` 或 `22.12+`
- `npm 9+`

如果只是运行一个“普通 Django + Vue”项目，`backend/requirements.txt` 勉强够用；
但如果要完整启用当前仓库里的 AI 对话、知识库、LangGraph、语音能力，应该安装根目录的：

```bash
pip install -r requirements.txt
```

## 7. 环境变量

后端使用 `python-dotenv`，默认会从 `backend/.env` 读取配置。

建议在 `backend/.env` 中至少提供以下变量：

```env
API_KEY="your_api_key"
API_BASE="https://your-openai-compatible-endpoint/v1"
MODEL_NAME="your-model-name"
WSS_URL="wss://your-realtime-or-audio-endpoint"
VOICE_URL="https://your-voice-customization-endpoint"
```

### 7.1 变量说明

- `API_KEY`
  - 大模型、ASR、TTS、向量 embedding 所使用的统一密钥

- `API_BASE`
  - OpenAI Compatible 接口地址
  - 聊天模型和 embedding 会走这个地址

- `MODEL_NAME`
  - 对话与记忆总结使用的大模型名称

- `WSS_URL`
  - ASR / TTS 使用的 WebSocket 推理地址

- `VOICE_URL`
  - 自定义音色管理接口地址

### 7.2 安全建议

- 不要把真实 `API_KEY` 提交到仓库
- `SECRET_KEY` 不建议继续写死在 `settings.py`
- 生产环境应使用单独的环境变量注入方式

## 8. 本地启动

## 8.1 克隆项目

```bash
git clone <your-repository-url>
cd AIFriends
```

## 8.2 创建虚拟环境并安装 Python 依赖

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 8.3 配置后端环境变量

在 `backend/` 目录下创建 `.env`：

```env
API_KEY="your_api_key"
API_BASE="https://your-openai-compatible-endpoint/v1"
MODEL_NAME="your-model-name"
WSS_URL="wss://your-realtime-or-audio-endpoint"
VOICE_URL="https://your-voice-customization-endpoint"
```

## 8.4 初始化数据库

```bash
cd backend
..\.venv\Scripts\python.exe manage.py migrate
```

如果你已经激活虚拟环境，也可以直接：

```bash
python manage.py migrate
```

创建管理员账号：

```bash
python manage.py createsuperuser
```

## 8.5 启动 Django

```bash
cd backend
python manage.py runserver
```

默认地址：

- 后端 API：`http://127.0.0.1:8000`
- Django Admin：`http://127.0.0.1:8000/admin`

## 8.6 启动前端

```bash
cd frontend
npm install
npm run dev
```

默认地址：

- 前端：`http://localhost:5173`

## 9. 前端环境切换

前端请求地址配置位于：

- `frontend/src/js/config/config.js`

当前支持三种模式：

- `vue`
  - 前端跑在 Vite
  - API 指向 `http://127.0.0.1:8000`
  - VAD 资源从 `http://localhost:5173/vad/` 读取

- `django`
  - 前端作为 Django 静态资源使用
  - API 指向 `http://127.0.0.1:8000`
  - VAD 资源从 Django 静态目录读取

- `cloud`
  - 线上域名模式

本地开发一般建议用：

```js
const platform = 'vue'
```

## 10. 初始化业务数据

项目能启动，不代表核心功能一定能直接用。
第一次运行通常还需要补几类业务数据。

## 10.1 添加音色

角色创建与更新依赖 `Voice` 表。

如果后台没有任何音色记录：

- 创建角色时音色下拉为空
- 更新角色时无法正常选择音色

可以通过 Django Admin 维护：

- `Voice`
  - `name`：显示名称
  - `voice_id`：第三方平台返回的音色 ID

## 10.2 添加系统提示词

聊天接口会从 `SystemPrompt` 表中读取系统提示词并按顺序拼接。

建议在 Django Admin 中至少创建一组用于“回复”的提示词，例如：

- 角色扮演边界
- 回复长度
- 说话风格
- 输出限制

如果这里没有内容，聊天仍可能运行，但效果会明显不稳定。

## 10.3 准备知识库数据

知识库原始文件位于：

- `backend/web/documents/data.txt`

向量库存储位于：

- `backend/web/documents/lancedb_storage/`

如果你更新了 `data.txt`，可以重新生成向量库。

在 `backend/` 目录执行：

```bash
python manage.py shell
```

然后运行：

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

## 11. 常用页面与路由

前端路由配置位于：

- `frontend/src/router/index.js`

主要页面：

- `/`
  - 首页，展示角色列表

- `/friend/`
  - 我的会话 / 好友列表

- `/create/`
  - 创建角色页

- `/create/character/update/:character_id/`
  - 编辑角色页

- `/user/account/login/`
  - 登录页

- `/user/account/register/`
  - 注册页

- `/user/space/:user_id/`
  - 用户个人空间

- `/user/profile`
  - 编辑个人资料

## 12. API 概览

后端路由位于：

- `backend/web/urls.py`

### 12.1 用户相关

- `POST /api/user/account/login/`
- `POST /api/user/account/logout/`
- `POST /api/user/account/register/`
- `POST /api/user/account/refresh_token/`
- `GET /api/user/account/get_user_info/`
- `POST /api/user/profile/update/`

### 12.2 角色相关

- `POST /api/create/character/create/`
- `POST /api/create/character/update/`
- `POST /api/create/character/remove/`
- `GET /api/create/character/get_single/`
- `GET /api/create/character/get_list/`
- `GET /api/create/character/voice/get_list/`
- `GET /api/homepage/index/`

### 12.3 会话相关

- `POST /api/friend/get_or_create/`
- `POST /api/friend/remove/`
- `GET /api/friend/get_list/`
- `POST /api/friend/message/chat/`
- `GET /api/friend/message/get_history/`
- `POST /api/friend/message/asr/asr/`

## 13. 前端打包与 Django 集成

Vite 配置位于：

- `frontend/vite.config.js`

打包输出目录是：

- `backend/static/frontend/`

执行：

```bash
cd frontend
npm run build
```

会把产物写到 Django 静态目录。

### 13.1 当前代码里的一个实际约束

模板文件：

- `backend/web/templates/index.html`

当前是直接写死了构建产物的 hash 文件名，例如：

- `index-xxxx.js`
- `index-xxxx.css`

这意味着：

1. 每次前端重新打包后，hash 可能变化
2. `backend/web/templates/index.html` 里的引用可能需要同步更新

如果你后面想把部署流程做稳定，建议改成：

- 由 Django 读取打包后的 `backend/static/frontend/index.html`
- 或引入 manifest 自动注入资源

## 14. 部署建议

### 14.1 Django

部署前至少需要处理：

- `DEBUG=False`
- 更换 `SECRET_KEY`
- 正确设置 `ALLOWED_HOSTS`
- 配置静态资源与媒体资源目录
- 为 cookie、跨域、代理头做生产环境设置

### 14.2 静态资源

如果使用 Django 托管前端静态文件：

- 前端先 `npm run build`
- Django 提供 `/assets/` 与 `/media/` 访问

当前开发环境中，`backend/backend/urls.py` 会在 `DEBUG=True` 时额外挂载：

- `/assets/`
- `/media/`

生产环境应由 Nginx 或其他 Web Server 处理。

## 15. 常见问题

### 15.1 前端可以打开，但聊天没响应

优先检查：

- `backend/.env` 是否存在
- `API_KEY / API_BASE / MODEL_NAME / WSS_URL` 是否正确
- 后端是否安装了根目录 `requirements.txt`

### 15.2 创建角色时没有音色

检查 Django Admin 中 `Voice` 表是否有数据。

### 15.3 语音输入无法工作

检查以下几项：

- 浏览器是否授权麦克风
- `frontend/public/vad/` 是否完整
- 当前 `platform` 是否与运行方式匹配
- `WSS_URL` 是否可用

### 15.4 知识库检索没有效果

检查：

- `backend/web/documents/data.txt` 是否有内容
- `lancedb_storage` 是否已生成
- `API_BASE` / embedding 接口是否可用

### 15.5 重新打包前端后页面空白

优先检查：

- `backend/static/frontend/assets/` 中的新 hash 文件名
- `backend/web/templates/index.html` 中引用是否还是旧文件

### 15.6 本地执行 `vite build` 遇到 `spawn EPERM`

这通常是 Windows 本机环境权限、PowerShell 执行策略、杀软或 Node 子进程限制问题，不一定是前端代码错误。

建议优先排查：

- 是否通过 `cmd /c npm run build` 执行
- 是否有安全软件拦截
- 是否存在受限目录权限

## 16. 当前代码里值得注意的点

这部分不是 README 必需内容，但对二次开发有帮助。

### 16.1 根目录 `requirements.txt` 才是完整依赖

`backend/requirements.txt` 只包含 Django 基础依赖，不包含 LangChain / LangGraph / OpenAI / LanceDB 等完整能力。

### 16.2 根目录 `main.py` 不是项目入口

真正的后端入口是：

- `backend/manage.py`

真正的前端入口是：

- `frontend/src/main.js`

### 16.3 仓库中已包含部分构建产物

包括：

- `backend/static/frontend/`
- `frontend/public/vad/`

这对快速运行是方便的，但也意味着：

- 静态资源可能和当前源码版本不完全同步
- 打包后请重新核对引用关系

## 17. 开发建议

如果你准备继续迭代这个项目，建议优先做这几件事：

1. 把 `SECRET_KEY`、Cookie `secure`、域名配置改成环境变量控制。
2. 统一前端构建产物注入方式，去掉模板里写死的 hash 文件名。
3. 给 `Voice`、`SystemPrompt`、知识库初始化加脚本或 management command。
4. 把 README 里的环境变量模板同步成 `.env.example`。
5. 为关键接口补基础测试，尤其是登录、角色更新、聊天链路。
