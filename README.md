# AIFriends - 智能社交平台

一个基于Vue 3 + Django的现代化社交网络应用，专注于AI驱动的朋友圈互动体验。

## 🚀 技术栈

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 现代化构建工具
- **Pinia** - Vue状态管理库
- **Vue Router 4** - 官方路由管理器
- **Tailwind CSS** - 实用优先的CSS框架
- **DaisyUI** - Tailwind CSS组件库
- **Axios** - HTTP客户端

### 后端
- **Django 6.0** - Python Web框架
- **Django REST Framework** - RESTful API框架
- **SimpleJWT** - JWT认证方案
- **SQLite** - 默认数据库

## 📁 项目结构

```
AIFriends/
├── backend/                 # Django后端
│   ├── backend/            # Django项目配置
│   ├── web/                # 主要应用
│   │   ├── models/         # 数据模型
│   │   ├── views/          # 视图逻辑
│   │   ├── migrations/     # 数据库迁移
│   │   └── urls.py         # 路由配置
│   └── manage.py           # Django管理脚本
├── frontend/               # Vue前端
│   ├── src/                # 源代码
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia状态管理
│   │   ├── router/         # 路由配置
│   │   └── js/             # JavaScript工具
│   ├── public/             # 静态资源
│   └── package.json        # npm配置
├── README.md               # 项目说明文档
└── main.py                 # 启动脚本
```

## 🔧 环境要求

- **Python**: 3.8+
- **Node.js**: 20.19.0 或 >=22.12.0
- **npm**: 9.0+

## 🛠️ 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/LYcoding0/AIFriends
cd AIFriends
```

### 2. 后端设置
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver
```

### 3. 前端设置
```bash
# 在新终端中进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用
- 前端: http://localhost:5173
- 后端API: http://127.0.0.1:8000
- Django管理后台: http://127.0.0.1:8000/admin

## 🎯 核心功能

### 用户系统
- ✅ 用户注册/登录
- ✅ JWT Token认证
- ✅ 自动Token刷新
- ✅ 用户资料管理
- ✅ 头像上传

### 社交功能
- 🔜 朋友圈动态发布
- 🔜 好友关系管理
- 🔜 消息系统
- 🔜 个人空间展示

## 🔒 安全特性

- **双Token机制**: Access Token + Refresh Token
- **HttpOnly Cookie**: 防止XSS攻击
- **JWT认证**: 无状态认证方案
- **CORS配置**: 跨域资源共享控制
- **CSRF保护**: Django内置安全机制

## 📱 响应式设计

- 移动端适配
- 桌面端优化
- 组件化UI设计
- 暗色模式支持

## 🚀 部署指南

### 生产环境部署

#### 后端部署
```bash
# 收集静态文件
python manage.py collectstatic

# 设置生产环境变量
export DEBUG=False
export SECRET_KEY="your-secret-key"

# 使用Gunicorn部署
pip install gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

#### 前端部署
```bash
# 构建生产版本
npm run build

# 部署到Nginx/Apache
# 配置静态文件服务
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

<p align="center">Made with ❤️ for the developer community</p>
