# 银行智能客服 MVP 前端

基于 React 18+ 的极简聊天界面，用于银行智能客服系统。

## 技术栈

- **React 18+** - 前端框架
- **Axios** - HTTP 请求库
- **Tailwind CSS** - 样式框架
- **React Scripts** - 构建工具

## 项目结构

```
frontend/
├── src/
│   ├── App.js          # 主组件（聊天逻辑）
│   ├── index.js        # 入口文件
│   ├── index.css       # 全局样式（Tailwind + 自定义样式）
│   └── api/
│       └── axios.js    # Axios配置（基础URL、请求拦截）
├── public/
│   └── index.html      # HTML模板
├── .env                # 环境变量配置
├── package.json        # 依赖清单
├── tailwind.config.js  # Tailwind配置
├── postcss.config.js   # PostCSS配置
└── README.md           # 说明文档
```

## 环境配置

### 环境变量

在 `.env` 文件中配置后端API地址：

```env
REACT_APP_API_BASE_URL=http://localhost:3000
```

- **开发环境**：通常为 `http://localhost:3000`
- **生产环境**：根据实际部署的后端地址修改

### 安装依赖

```bash
cd frontend
npm install
```

## 启动和构建

### 开发模式启动

```bash
npm start
```

启动后，应用将在 `http://localhost:3000` 运行（如果端口被占用，会自动使用其他端口）。

### 生产构建

```bash
npm run build
```

构建完成后，静态文件将生成在 `build/` 目录中，可以部署到任何静态文件服务器。

### 其他命令

- `npm test` - 运行测试（如果有）
- `npm run eject` - 弹出配置（不可逆操作）

## 功能特性

### 核心功能

1. **极简聊天界面**
   - 清晰的对话列表展示
   - 用户消息和客服消息区分显示
   - 实时时间戳

2. **消息发送**
   - 输入框支持多行输入
   - 回车键发送（Shift+Enter换行）
   - 发送按钮状态管理

3. **加载状态**
   - 发送请求时显示"正在思考..."
   - 防止重复提交

4. **错误处理**
   - 网络错误提示
   - 友好的错误消息展示

5. **响应式设计**
   - 适配移动端和PC端
   - 优化的触摸交互

6. **其他功能**
   - 清空对话按钮
   - 自动滚动到底部
   - 消息淡入动画

## API 接口说明

### 聊天接口

**请求地址**: `POST /api/chat`

**请求体**:
```json
{
  "message": "用户输入的问题"
}
```

**响应格式**:
```json
{
  "reply": "客服回复内容"
}
```

或

```json
{
  "message": "客服回复内容"
}
```

前端代码会自动适配这两种响应格式。

## 部署说明

### 开发环境部署

1. 配置 `.env` 文件中的 `REACT_APP_API_BASE_URL`
2. 运行 `npm start` 启动开发服务器

### 生产环境部署

1. 修改 `.env` 文件中的后端API地址
2. 运行 `npm run build` 构建生产版本
3. 将 `build/` 目录部署到静态文件服务器（Nginx、Apache等）
4. 配置反向代理或CORS以连接后端API

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理（可选）
    location /api {
        proxy_pass http://backend-server:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 注意事项

1. **环境变量**：所有以 `REACT_APP_` 开头的环境变量会在构建时注入到应用中
2. **API地址**：确保后端API支持CORS，或使用反向代理
3. **浏览器兼容性**：支持现代浏览器（Chrome、Firefox、Safari、Edge等）
4. **移动端适配**：已优化触摸交互和响应式布局

## 开发建议

- 修改样式：编辑 `src/index.css`
- 修改API配置：编辑 `src/api/axios.js`
- 添加功能：在 `src/App.js` 中扩展

## 许可证

MIT

