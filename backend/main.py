"""
银行智能客服 FastAPI 后端
提供健康检查和聊天接口，集成百度千帆大模型
"""

import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import qianfan

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 初始化FastAPI应用
app = FastAPI(
    title="银行智能客服API",
    description="轻量级银行智能客服MVP后端服务",
    version="1.0.0"
)

# 配置跨域（支持React前端调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化千帆客户端
QIANFAN_AK = os.getenv("QIANFAN_AK")
QIANFAN_SK = os.getenv("QIANFAN_SK")

if QIANFAN_AK and QIANFAN_SK:
    qianfan.AK(QIANFAN_AK)
    qianfan.SK(QIANFAN_SK)
    chat_comp = qianfan.ChatCompletion()
    logger.info("✅ 千帆API配置成功！AK已加载（前4位: %s...）", QIANFAN_AK[:4] if len(QIANFAN_AK) > 4 else "****")
else:
    chat_comp = None
    logger.warning("⚠️  未找到千帆AK/SK配置，大模型功能将不可用")
    if not QIANFAN_AK:
        logger.warning("  - QIANFAN_AK 未设置")
    if not QIANFAN_SK:
        logger.warning("  - QIANFAN_SK 未设置")

# 固定问答字典（优先匹配，减少大模型调用）
FAQ_DICT = {
    "办卡": "您可以通过以下方式办理银行卡：1. 前往我行任意网点携带身份证办理；2. 通过手机银行APP在线申请；3. 拨打客服热线400-xxx-xxxx预约办理。",
    "信用卡": "我行提供多种信用卡产品，您可以通过官网、手机银行或网点咨询具体卡种及申请条件。",
    "存款利率": "当前一年期定期存款利率为1.75%，三年期为2.75%，五年期为2.75%。具体利率以我行官网或网点公告为准。",
    "利率": "我行存款利率会根据央行政策调整，您可以登录手机银行或前往网点查询最新利率信息。",
    "网点": "您可以通过以下方式查询网点信息：1. 登录手机银行APP查询附近网点；2. 拨打客服热线400-xxx-xxxx；3. 访问我行官网查询网点地图。",
    "营业时间": "我行网点营业时间通常为：工作日 9:00-17:00，周末部分网点营业。具体营业时间请咨询当地网点或客服热线。",
    "人工客服": "如需人工客服，请拨打客服热线400-xxx-xxxx，按0键转人工服务，工作时间：周一至周日 8:00-20:00。",
    "客服": "您可以通过以下方式联系客服：1. 客服热线400-xxx-xxxx；2. 手机银行在线客服；3. 微信公众号客服。",
    "开户": "您可以通过以下方式开户：1. 携带身份证前往网点办理；2. 通过手机银行APP在线开户。",
    "转账": "您可以通过手机银行、网上银行或网点进行转账操作。手机银行单日转账限额为5万元，如需提高限额请前往网点办理。",
}

# 银行相关关键词（用于过滤无关问题）
BANK_KEYWORDS = [
    "办卡", "信用卡", "借记卡", "存款", "利率", "理财", "贷款", "转账", 
    "网点", "开户", "销户", "挂失", "密码", "客服", "人工", "营业时间",
    "账户", "余额", "明细", "对账单", "网银", "手机银行", "银行"
]


def check_bank_related(question: str) -> bool:
    """检查问题是否与银行相关"""
    question_lower = question.lower()
    for keyword in BANK_KEYWORDS:
        if keyword in question:
            return True
    return False


def search_faq(question: str) -> Optional[str]:
    """在固定问答字典中查找匹配答案"""
    question_lower = question.lower()
    for keyword, answer in FAQ_DICT.items():
        if keyword in question:
            return answer
    return None


def call_qianfan_model(question: str) -> str:
    """调用百度千帆ERNIE-3.5-8K模型"""
    if not chat_comp:
        raise Exception("千帆API未配置，无法调用大模型")
    
    try:
        logger.info("🤖 开始调用千帆API - 问题: %s", question[:50] + "..." if len(question) > 50 else question)
        
        # 构建系统提示词，限制回答范围
        system_prompt = """你是一家银行的智能客服助手。请只回答与银行业务相关的问题，包括：
- 办卡、开户、销户
- 存款利率、理财产品
- 网点查询、营业时间
- 转账、账户查询
- 客服联系方式

如果用户的问题与银行业务无关，请礼貌地告知："抱歉，我只能回答与银行业务相关的问题，如需其他帮助，请联系人工客服。"""

        # 调用千帆API，使用ERNIE-3.5-8K模型
        logger.info("📡 正在调用千帆ERNIE-3.5-8K模型...")
        response = chat_comp.do(
            model="ERNIE-3.5-8K",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.1,  # 降低随机性，减少token消耗
            max_tokens=500,  # 限制输出长度
        )
        
        logger.info("✅ 千帆API调用成功！响应类型: %s", type(response).__name__)
        
        # 提取回答内容
        if response and "body" in response:
            result = response.get("body", {}).get("result", "")
            if result:
                logger.info("📝 成功获取回答，长度: %d 字符", len(result))
                return result
        elif response and "result" in response:
            result = response["result"]
            logger.info("📝 成功获取回答，长度: %d 字符", len(result) if isinstance(result, str) else 0)
            return result
        
        logger.error("❌ 大模型返回格式异常: %s", str(response)[:200])
        raise Exception("大模型返回格式异常")
        
    except Exception as e:
        logger.error("❌ 调用千帆大模型失败: %s", str(e))
        raise Exception(f"调用千帆大模型失败: {str(e)}")


# 请求模型
class ChatRequest(BaseModel):
    question: str


# 响应模型
class ChatResponse(BaseModel):
    answer: str


class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}


@app.get("/api/config/check")
async def check_config():
    """
    检查千帆API配置状态
    用于验证AK/SK是否正确配置
    """
    has_ak = bool(QIANFAN_AK)
    has_sk = bool(QIANFAN_SK)
    is_configured = has_ak and has_sk
    
    return {
        "qianfan_configured": is_configured,
        "has_ak": has_ak,
        "has_sk": has_sk,
        "ak_preview": QIANFAN_AK[:4] + "..." if has_ak and len(QIANFAN_AK) > 4 else "未设置",
        "message": "✅ 千帆API已配置" if is_configured else "⚠️ 千帆API未完全配置"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    银行智能客服聊天接口
    
    参数:
        request: 包含用户提问的请求体 {"question": "用户提问内容"}
    
    返回:
        {"answer": "客服回答内容"}
    """
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    # 检查问题是否与银行相关
    if not check_bank_related(question):
        return ChatResponse(
            answer="抱歉，我只能回答与银行业务相关的问题（如办卡、存款利率、网点查询、人工客服等）。如需其他帮助，请联系人工客服。"
        )
    
    # 优先在固定问答字典中查找
    faq_answer = search_faq(question)
    if faq_answer:
        return ChatResponse(answer=faq_answer)
    
    # 调用大模型生成回答
    try:
        answer = call_qianfan_model(question)
        return ChatResponse(answer=answer)
    except Exception as e:
        # 异常处理：返回友好提示
        error_msg = str(e)
        if "千帆API未配置" in error_msg or "AK" in error_msg or "SK" in error_msg:
            return ChatResponse(
                answer="抱歉，智能客服服务暂时不可用，请联系人工客服：400-xxx-xxxx"
            )
        else:
            return ChatResponse(
                answer="抱歉，智能客服暂时无法回答您的问题，请稍后再试或联系人工客服：400-xxx-xxxx"
            )


if __name__ == "__main__":
    import uvicorn
    # 启动命令：uvicorn main:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

