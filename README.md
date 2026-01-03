# 银行智能客服 - 本地运行和联调指南

本文档提供详细的本地运行步骤，帮助您快速启动和测试银行智能客服系统。

---

## 📋 目录

1. [环境要求](#环境要求)
2. [后端启动步骤](#后端启动步骤)
3. [前端启动步骤](#前端启动步骤)
4. [联调验证要点](#联调验证要点)
5. [常见问题排查](#常见问题排查)

---

## 🔧 环境要求

### 后端环境
- Python 3.8 或更高版本
- pip（Python包管理器）

### 前端环境
- Node.js 16.x 或更高版本
- npm 或 yarn

### 第三方服务
- 百度千帆API（需要AK和SK密钥）

---

## 🚀 后端启动步骤

### 步骤1：进入后端目录

```bash
cd backend
```

### 步骤2：创建Python虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 步骤3：安装Python依赖

```bash
pip install -r requirements.txt
```

**依赖包列表：**
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic==2.5.3
- python-dotenv==1.0.0
- qianfan==0.3.2

### 步骤4：配置环境变量

在 `backend` 目录下创建 `.env` 文件（如果不存在）：

```bash
# Windows PowerShell
New-Item .env -ItemType File

# Linux/Mac
touch .env
```

编辑 `.env` 文件，添加以下内容：

```env
# 百度千帆API密钥（请替换为您的实际密钥）
QIANFAN_AK=your_ak_here
QIANFAN_SK=your_sk_here
```

**⚠️ 重要提示：**
- 请将 `your_ak_here` 替换为您的百度千帆AK（Access Key）
- 请将 `your_sk_here` 替换为您的百度千帆SK（Secret Key）
- 如果没有千帆API密钥，后端仍可启动，但大模型功能将不可用，只会使用固定FAQ回答

### 步骤5：启动后端服务

```bash
# 方式1：使用uvicorn直接启动（推荐用于开发）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式2：使用Python直接运行
python main.py
```

**启动成功标志：**
- 看到类似以下输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 步骤6：验证后端服务

打开浏览器访问：http://localhost:8000/health

如果返回 `{"status":"ok"}`，说明后端服务启动成功。

**API文档地址：** http://localhost:8000/docs（Swagger UI界面）

---

## 🎨 前端启动步骤

### 步骤1：进入前端目录

```bash
cd frontend
```

### 步骤2：安装Node.js依赖

```bash
npm install
```

**如果使用yarn：**
```bash
yarn install
```

**主要依赖包：**
- react ^18.2.0
- react-dom ^18.2.0
- axios ^1.6.0
- react-scripts 5.0.1
- tailwindcss ^3.3.0

### 步骤3：配置API地址（可选）

如果需要修改后端API地址，可以创建 `.env` 文件：

```bash
# Windows PowerShell
New-Item .env -ItemType File

# Linux/Mac
touch .env
```

编辑 `.env` 文件：

```env
# 后端API地址（默认：http://localhost:8000）
REACT_APP_API_BASE_URL=http://localhost:8000
```

**⚠️ 注意：**
- 如果后端运行在其他地址或端口，请修改此配置
- 如果后端和前端在同一台机器上，使用默认值即可

### 步骤4：启动前端开发服务器

```bash
npm start
```

**启动成功标志：**
- 浏览器自动打开 http://localhost:3000
- 控制台显示：
```
Compiled successfully!
You can now view bank-ics-frontend in the browser.
  Local:            http://localhost:3000
```

---

## ✅ 联调验证要点

### 核心测试问题

请在浏览器中打开前端页面（http://localhost:3000），测试以下3个核心问题：

#### 1. 储蓄卡怎么办理？

**预期结果：**
- 应该返回办卡相关答案，包含办理方式（网点、手机银行APP、客服热线等）

**测试步骤：**
1. 在前端输入框输入："储蓄卡怎么办理？"
2. 点击"发送"按钮
3. 查看返回的答案

#### 2. 定期存款利率？

**预期结果：**
- 应该返回当前定期存款利率信息（一年期、三年期、五年期等）

**测试步骤：**
1. 在前端输入框输入："定期存款利率？"
2. 点击"发送"按钮
3. 查看返回的利率信息

#### 3. 怎么转人工客服？

**预期结果：**
- 应该返回人工客服联系方式（客服热线、转接方式、工作时间等）

**测试步骤：**
1. 在前端输入框输入："怎么转人工客服？"
2. 点击"发送"按钮
3. 查看返回的客服联系方式

### 其他验证项

#### 健康检查接口
```bash
curl http://localhost:8000/health
```
应返回：`{"status":"ok"}`

#### 聊天接口直接测试
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"储蓄卡怎么办理？\"}"
```
应返回包含 `answer` 字段的JSON响应

---

## 🔍 常见问题排查

### 问题1：跨域错误（CORS Error）

**错误信息：**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/chat' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**解决方法：**
1. 确认后端 `main.py` 中已配置CORS中间件（代码中已包含）
2. 确认后端服务已正常启动
3. 检查前端 `axios.js` 中的 `API_BASE_URL` 配置是否正确
4. 如果问题仍存在，检查后端CORS配置：

```python
# backend/main.py 中应该包含：
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境可以使用 "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 问题2：密钥错误（千帆API配置问题）

**错误信息：**
- 后端启动时显示："警告：未找到千帆AK/SK配置，大模型功能将不可用"
- 前端返回："抱歉，智能客服服务暂时不可用"

**解决方法：**
1. 检查 `backend/.env` 文件是否存在
2. 确认 `.env` 文件格式正确（无多余空格、引号等）：
   ```env
   QIANFAN_AK=your_actual_ak
   QIANFAN_SK=your_actual_sk
   ```
3. 确认AK和SK值正确（可在百度智能云控制台获取）
4. 重启后端服务（修改.env后需要重启）
5. 验证密钥是否有效（检查百度智能云控制台的API调用记录）

**注意：** 如果没有配置密钥，系统仍可使用固定FAQ回答常见问题，但无法使用大模型回答复杂问题。

### 问题3：接口调用失败（404/500错误）

**错误信息：**
- `404 Not Found` - 接口路径不存在
- `500 Internal Server Error` - 服务器内部错误

**解决方法：**

**404错误：**
1. 检查前端 `axios.js` 中的 `baseURL` 是否正确
2. 确认后端API路径为 `/api/chat`（不是 `/chat`）
3. 检查后端是否正常运行在8000端口

**500错误：**
1. 查看后端控制台的错误日志
2. 检查千帆API调用是否正常（如果使用大模型）
3. 验证请求体格式是否正确：
   ```json
   {"question": "您的问题"}
   ```
4. 检查Python依赖是否完整安装

### 问题4：前端无法连接到后端

**错误信息：**
```
网络错误: 无法连接到服务器
```

**解决方法：**
1. 确认后端服务已启动（访问 http://localhost:8000/health 测试）
2. 检查防火墙是否阻止了8000端口
3. 确认前端 `.env` 中的 `REACT_APP_API_BASE_URL` 配置正确
4. 如果后端运行在其他机器，确保IP地址和端口正确
5. 重启前端服务（修改.env后需要重启）

### 问题5：前端启动失败（依赖安装问题）

**错误信息：**
```
npm ERR! code ELIFECYCLE
npm ERR! errno 1
```

**解决方法：**
1. 清除缓存并重新安装：
   ```bash
   rm -rf node_modules package-lock.json  # Linux/Mac
   rmdir /s node_modules & del package-lock.json  # Windows
   npm install
   ```
2. 检查Node.js版本（需要16.x或更高）：
   ```bash
   node --version
   ```
3. 使用yarn替代npm：
   ```bash
   yarn install
   yarn start
   ```

### 问题6：后端Python依赖安装失败

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方法：**
1. 升级pip：
   ```bash
   python -m pip install --upgrade pip
   ```
2. 使用国内镜像源（如果网络问题）：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
3. 检查Python版本：
   ```bash
   python --version  # 需要3.8或更高
   ```

---

## 📝 快速启动检查清单

启动前请确认：

- [ ] Python 3.8+ 已安装
- [ ] Node.js 16+ 已安装
- [ ] 后端 `.env` 文件已创建并配置千帆AK/SK（可选）
- [ ] 后端依赖已安装（`pip install -r requirements.txt`）
- [ ] 前端依赖已安装（`npm install`）
- [ ] 后端服务已启动（运行在8000端口）
- [ ] 前端服务已启动（运行在3000端口）
- [ ] 浏览器可访问 http://localhost:3000
- [ ] 后端健康检查通过（http://localhost:8000/health）

---

## 🔗 相关链接

- **后端API文档：** http://localhost:8000/docs
- **前端地址：** http://localhost:3000
- **后端健康检查：** http://localhost:8000/health

---

## 📞 技术支持

如遇到其他问题，请检查：
1. 后端控制台日志
2. 前端浏览器控制台（F12）
3. 网络请求详情（浏览器开发者工具 - Network标签）

---

**最后更新：** 2026年

