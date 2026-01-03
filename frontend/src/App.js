import React, { useState, useRef, useEffect } from 'react';
import apiClient from './api/axios';
import './index.css';

function App() {
  const [messages, setMessages] = useState([]); // 对话列表
  const [inputValue, setInputValue] = useState(''); // 输入框内容
  const [isLoading, setIsLoading] = useState(false); // 加载状态
  const messagesEndRef = useRef(null); // 用于滚动到底部
  const inputRef = useRef(null); // 输入框引用

  // 滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // 当消息更新时自动滚动
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 发送消息
  const sendMessage = async () => {
    const userMessage = inputValue.trim();
    if (!userMessage || isLoading) return;

    // 添加用户消息到列表
    const newUserMessage = {
      id: Date.now(),
      type: 'user',
      content: userMessage,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // 调用后端API
      const response = await apiClient.post('/api/chat', {
        question: userMessage,
      });

      // 添加客服回复到列表
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.answer || '抱歉，我暂时无法回答这个问题。',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // 错误处理
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: '抱歉，服务暂时不可用，请稍后再试。',
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // 聚焦输入框
      inputRef.current?.focus();
    }
  };

  // 清空对话
  const clearMessages = () => {
    if (window.confirm('确定要清空所有对话吗？')) {
      setMessages([]);
      inputRef.current?.focus();
    }
  };

  // 回车发送（Shift+Enter换行）
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-container">
      {/* 头部标题栏 */}
      <header className="header">
        <h1 className="header-title">银行智能客服</h1>
        {messages.length > 0 && (
          <button
            onClick={clearMessages}
            className="clear-button"
            title="清空对话"
          >
            清空
          </button>
        )}
      </header>

      {/* 对话列表区域 */}
      <main className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>欢迎使用银行智能客服，有什么问题可以问我哦~</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.type === 'user' ? 'message-user' : 'message-bot'}`}
              >
                <div className="message-content">
                  {message.content}
                </div>
                <div className="message-time">{message.timestamp}</div>
              </div>
            ))}
            {/* 加载状态 */}
            {isLoading && (
              <div className="message message-bot">
                <div className="message-content loading">
                  正在思考...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* 输入区域 */}
      <footer className="input-container">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="请输入您的问题..."
            className="input-field"
            rows="1"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            发送
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;

