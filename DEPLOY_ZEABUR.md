# 银行智能客服MVP - Zeabur部署指南

本文档提供详细的Zeabur部署步骤，帮助您将银行智能客服系统部署到Zeabur平台。

---

## 📋 目录

1. [部署前准备](#部署前准备)
2. [第一部分：FastAPI后端部署](#第一部分fastapi后端部署)
3. [第二部分：React前端部署](#第二部分react前端部署)
4. [部署后验证](#部署后验证)
5. [常见问题排查](#常见问题排查)

---

## 🔧 部署前准备

### 前提条件

- ✅ 项目已上传到GitHub仓库
- ✅ 拥有Zeabur账号（如未注册，请访问 https://zeabur.com 注册）
- ✅ 已获取百度千帆API的AK和SK密钥

### 项目结构确认

确保您的GitHub仓库结构如下：

```
bank-ics-service/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── package.json
    ├── public/
    └── src/
```

---

## 🚀 第一部分：FastAPI后端部署

### 步骤1：创建后端服务

1. **登录Zeabur控制台**
   - 访问 https://zeabur.com 并登录您的账号
   - 点击Zeabur左侧的「**Deploy**」按钮（或「**+ New Project**」）

2. **导入GitHub仓库**
   - 在「**Import from Git**」区域，点击「**GitHub**」图标
   - 授权Zeabur访问您的GitHub账号（如首次使用）
   - 在仓库列表中找到并选择 `bank-ics-service` 仓库
   - 点击「**Import**」按钮

3. **选择服务类型**
   - Zeabur会自动检测项目类型
   - 如果未自动识别，请手动选择「**Python**」或「**Other**」
   - 在「**Root Directory**」中设置：`backend`
   - 点击「**Deploy**」开始部署

### 步骤2：配置环境变量

1. **进入服务设置**
   - 部署开始后，点击服务卡片进入详情页
   - 点击左侧菜单的「**Environment Variables**」（环境变量）

2. **添加千帆API密钥**
   
   点击「**+ Add Variable**」按钮，依次添加以下环境变量：

   **变量1：QIANFAN_AK**
   - **Name（变量名）**：`QIANFAN_AK`
   - **Value（变量值）**：输入您的百度千帆Access Key
   - 点击「**Save**」保存

   **变量2：QIANFAN_SK**
   - **Name（变量名）**：`QIANFAN_SK`
   - **Value（变量值）**：输入您的百度千帆Secret Key
   - 点击「**Save**」保存

   **⚠️ 重要提示：**
   - 环境变量添加后，服务会自动重新部署
   - 请确保AK和SK值正确，不要包含多余的空格或引号
   - 如果密钥错误，后端仍可运行，但大模型功能将不可用

### 步骤3：配置启动命令

1. **进入服务设置**
   - 在服务详情页，点击左侧菜单的「**Settings**」（设置）

2. **设置启动命令**
   - 找到「**Start Command**」（启动命令）配置项
   - 输入以下命令：
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   - 点击「**Save**」保存

   **说明：**
   - `$PORT` 是Zeabur自动提供的端口环境变量，必须使用此变量
   - Zeabur会自动分配端口，无需手动指定

3. **确认Python版本（可选）**
   - 在「**Settings**」中找到「**Python Version**」
   - 建议选择 Python 3.10 或更高版本
   - 如果未显示此选项，Zeabur会自动检测 `requirements.txt` 并选择合适的版本

### 步骤4：配置端口（自动处理）

**重要说明：**
- Zeabur会自动处理端口配置，无需手动设置
- 后端代码中的 `--port $PORT` 会使用Zeabur分配的端口
- 确保 `main.py` 中的启动命令使用 `0.0.0.0` 作为host（代码中已配置）

### 步骤5：等待部署完成

1. **查看部署日志**
   - 在服务详情页，点击「**Logs**」（日志）标签
   - 观察部署进度，等待看到类似以下输出：
   ```
   INFO:     Uvicorn running on http://0.0.0.0:xxxx (Press CTRL+C to quit)
   INFO:     Application startup complete.
   ```

2. **获取服务域名**
   - 部署完成后，在服务详情页顶部会显示服务域名
   - 格式类似：`your-service-name-xxxxx.zeabur.app`
   - **请复制此域名，后续前端部署需要使用**

---

## 🎨 第二部分：React前端部署

### 步骤1：创建前端服务

1. **在同一个项目中添加新服务**
   - 在Zeabur项目页面，点击「**+ Add Service**」或「**+ New Service**」按钮
   - 选择「**Import from Git**」→「**GitHub**」
   - 选择同一个仓库：`bank-ics-service`

2. **配置服务类型**
   - Zeabur会自动检测为Node.js项目
   - 在「**Root Directory**」中设置：`frontend`
   - 点击「**Deploy**」开始部署

### 步骤2：配置构建命令

1. **进入服务设置**
   - 部署开始后，点击前端服务卡片进入详情页
   - 点击左侧菜单的「**Settings**」（设置）

2. **设置构建命令**
   - 找到「**Build Command**」（构建命令）配置项
   - 输入以下命令：
   ```bash
   npm install && npm run build
   ```
   - 点击「**Save**」保存

   **说明：**
   - `npm install`：安装Node.js依赖
   - `npm run build`：构建React生产版本（生成 `build` 目录）

3. **设置输出目录（重要）**
   - 找到「**Output Directory**」（输出目录）配置项
   - 输入：`build`
   - 点击「**Save**」保存

   **说明：**
   - React构建后的静态文件位于 `build` 目录
   - Zeabur需要知道静态文件的位置才能正确部署

### 步骤3：配置环境变量

1. **进入环境变量设置**
   - 在前端服务详情页，点击左侧菜单的「**Environment Variables**」

2. **添加后端API地址**
   
   点击「**+ Add Variable**」按钮，添加以下环境变量：

   **变量：REACT_APP_API_BASE_URL**
   - **Name（变量名）**：`REACT_APP_API_BASE_URL`
   - **Value（变量值）**：输入后端服务的完整URL
     - 格式：`https://your-backend-service-name-xxxxx.zeabur.app`
     - **注意：** 必须使用 `https://` 开头，不要包含末尾的斜杠
   - 点击「**Save**」保存

   **⚠️ 重要提示：**
   - 此环境变量必须在构建时可用（React使用 `REACT_APP_` 前缀的环境变量）
   - 环境变量添加后，服务会自动重新构建和部署
   - 如果后端地址配置错误，前端将无法调用API

### 步骤4：等待部署完成

1. **查看构建日志**
   - 在服务详情页，点击「**Logs**」（日志）标签
   - 观察构建进度，等待看到：
   ```
   Compiled successfully!
   ```

2. **获取前端域名**
   - 部署完成后，在服务详情页顶部会显示前端服务域名
   - 格式类似：`your-frontend-service-name-xxxxx.zeabur.app`
   - **此域名即为您的应用访问地址**

---

## ✅ 部署后验证

### 验证步骤1：检查后端服务

1. **访问健康检查接口**
   - 在浏览器中打开：`https://your-backend-service-name-xxxxx.zeabur.app/health`
   - 应该返回：`{"status":"ok"}`

2. **访问API文档**
   - 在浏览器中打开：`https://your-backend-service-name-xxxxx.zeabur.app/docs`
   - 应该看到Swagger UI界面，可以测试API接口

3. **测试聊天接口（可选）**
   - 在Swagger UI中，找到 `/api/chat` 接口
   - 点击「**Try it out**」
   - 输入测试问题：`{"question": "办卡"}`
   - 点击「**Execute**」
   - 应该返回包含 `answer` 字段的JSON响应

### 验证步骤2：检查前端服务

1. **访问前端页面**
   - 在浏览器中打开前端服务域名：`https://your-frontend-service-name-xxxxx.zeabur.app`
   - 应该看到银行智能客服的聊天界面

2. **测试核心功能**
   
   在前端页面测试以下问题：

   **测试1：办卡相关**
   - 输入："储蓄卡怎么办理？"
   - 应该返回办卡相关答案

   **测试2：利率查询**
   - 输入："定期存款利率？"
   - 应该返回利率信息

   **测试3：人工客服**
   - 输入："怎么转人工客服？"
   - 应该返回客服联系方式

3. **检查浏览器控制台（可选）**
   - 按 `F12` 打开开发者工具
   - 切换到「**Console**」标签
   - 发送消息后，检查是否有错误信息
   - 切换到「**Network**」标签，检查API请求是否成功（状态码应为200）

### 验证步骤3：检查跨域配置

如果前端调用后端API时出现跨域错误：

1. **确认后端CORS配置**
   - 后端代码中已配置允许所有来源（`allow_origins=["*"]`）
   - 如果仍有问题，可以检查后端日志

2. **检查环境变量**
   - 确认前端的 `REACT_APP_API_BASE_URL` 配置正确
   - 确认使用 `https://` 协议

---

## 🔍 常见问题排查

### 问题1：后端部署失败

**错误信息：**
- `ModuleNotFoundError` 或依赖安装失败

**解决方法：**
1. 检查 `backend/requirements.txt` 文件是否存在且格式正确
2. 查看部署日志，确认Python版本是否兼容
3. 在Zeabur设置中，确认「**Root Directory**」设置为 `backend`
4. 检查启动命令是否正确：`uvicorn main:app --host 0.0.0.0 --port $PORT`

### 问题2：后端无法连接千帆API

**错误信息：**
- 后端日志显示："警告：未找到千帆AK/SK配置"
- 前端返回："抱歉，智能客服服务暂时不可用"

**解决方法：**
1. 检查Zeabur环境变量中是否已添加 `QIANFAN_AK` 和 `QIANFAN_SK`
2. 确认环境变量值正确（无多余空格、引号）
3. 重新部署服务（修改环境变量后会自动重新部署）
4. 查看后端日志确认环境变量是否加载成功

### 问题3：前端构建失败

**错误信息：**
- `npm ERR!` 或构建命令执行失败

**解决方法：**
1. 检查 `frontend/package.json` 文件是否存在
2. 确认「**Root Directory**」设置为 `frontend`
3. 确认构建命令：`npm install && npm run build`
4. 确认输出目录设置为：`build`
5. 查看构建日志，检查具体错误信息

### 问题4：前端无法调用后端API

**错误信息：**
- 浏览器控制台显示：`Network Error` 或 `CORS Error`
- API请求返回404或500错误

**解决方法：**
1. **检查环境变量配置**
   - 确认前端的 `REACT_APP_API_BASE_URL` 已配置
   - 确认值格式正确：`https://your-backend-service-name-xxxxx.zeabur.app`（无末尾斜杠）

2. **检查后端地址**
   - 确认后端服务已成功部署
   - 访问后端健康检查接口验证：`https://your-backend-service-name-xxxxx.zeabur.app/health`

3. **重新构建前端**
   - 环境变量修改后，前端需要重新构建
   - 在Zeabur中，修改环境变量会自动触发重新部署
   - 等待构建完成后再次测试

4. **检查CORS配置**
   - 后端代码中已配置允许所有来源
   - 如果仍有问题，检查后端日志中的CORS错误信息

### 问题5：前端页面显示空白

**错误信息：**
- 页面加载但显示空白
- 浏览器控制台有JavaScript错误

**解决方法：**
1. 检查浏览器控制台（F12）的错误信息
2. 确认前端构建成功（查看Zeabur构建日志）
3. 确认输出目录设置为 `build`
4. 检查 `frontend/public/index.html` 文件是否存在

### 问题6：服务域名无法访问

**错误信息：**
- 浏览器显示：`This site can't be reached` 或 `404 Not Found`

**解决方法：**
1. 确认服务部署状态为「**Running**」（运行中）
2. 检查Zeabur服务详情页的域名是否正确
3. 确认使用 `https://` 协议访问
4. 等待几分钟后重试（DNS可能需要时间生效）

---

## 📝 部署检查清单

### 后端部署检查

- [ ] GitHub仓库已导入Zeabur
- [ ] 服务类型设置为Python
- [ ] Root Directory设置为 `backend`
- [ ] 启动命令配置：`uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] 环境变量 `QIANFAN_AK` 已添加
- [ ] 环境变量 `QIANFAN_SK` 已添加
- [ ] 服务部署状态为「Running」
- [ ] 健康检查接口可访问：`/health` 返回 `{"status":"ok"}`

### 前端部署检查

- [ ] 前端服务已添加到项目
- [ ] Root Directory设置为 `frontend`
- [ ] 构建命令配置：`npm install && npm run build`
- [ ] 输出目录设置为 `build`
- [ ] 环境变量 `REACT_APP_API_BASE_URL` 已添加（值为后端完整URL）
- [ ] 服务部署状态为「Running」
- [ ] 前端页面可正常访问
- [ ] 前端可以成功调用后端API

---

## 🔗 相关链接

- **Zeabur官方文档：** https://zeabur.com/docs
- **Zeabur控制台：** https://zeabur.com
- **百度千帆控制台：** https://console.bce.baidu.com/qianfan/

---

## 📞 技术支持

如遇到其他问题，请检查：

1. **Zeabur服务日志**
   - 后端服务：服务详情页 → 「Logs」标签
   - 前端服务：服务详情页 → 「Logs」标签

2. **浏览器开发者工具**
   - 按 `F12` 打开
   - 查看「Console」和「Network」标签的错误信息

3. **GitHub仓库**
   - 确认代码已正确提交
   - 检查 `requirements.txt` 和 `package.json` 文件

---

**最后更新：** 2024年

