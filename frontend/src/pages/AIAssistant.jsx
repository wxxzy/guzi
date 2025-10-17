import React, { useState, useRef, useEffect } from 'react'
import { Input, Button, Space, message, Spin, Card } from 'antd'
import { SendOutlined } from '@ant-design/icons'
import { getGeminiResponse } from '../utils/api'

const { TextArea } = Input

const AIAssistant = () => {
  const [messages, setMessages] = useState([]) // 存储对话历史
  const [inputMessage, setInputMessage] = useState('') // 用户输入
  const [loading, setLoading] = useState(false) // 加载状态
  const messagesEndRef = useRef(null) // 用于自动滚动到底部

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) {
      message.warning('请输入您的问题！')
      return
    }

    const newMessage = { sender: 'user', text: inputMessage }
    setMessages((prevMessages) => [...prevMessages, newMessage])
    setInputMessage('')
    setLoading(true)

    try {
      const response = await getGeminiResponse(inputMessage)
      const aiResponse = { sender: 'ai', text: response.response }
      setMessages((prevMessages) => [...prevMessages, aiResponse])
    } catch (error) {
      message.error(error.message || 'AI助手响应失败')
      setMessages((prevMessages) => [...prevMessages, { sender: 'ai', text: '抱歉，AI助手暂时无法响应。' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>AI智能助手</h1>
      <Card
        style={{ height: 'calc(100vh - 250px)', display: 'flex', flexDirection: 'column' }}
        bodyStyle={{ flex: 1, overflowY: 'auto', padding: '10px' }}
      >
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {messages.map((msg, index) => (
            <div 
              key={index} 
              style={{
                textAlign: msg.sender === 'user' ? 'right' : 'left',
                marginBottom: 8,
              }}
            >
              <Card 
                size="small"
                style={{
                  display: 'inline-block',
                  maxWidth: '70%',
                  backgroundColor: msg.sender === 'user' ? '#e6f7ff' : '#f0f0f0',
                  borderRadius: 8,
                }}
              >
                {msg.text}
              </Card>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </Card>
      <Space style={{ marginTop: 16, width: '100%' }} direction="horizontal">
        <TextArea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onPressEnter={handleSendMessage}
          placeholder="向AI助手提问..."
          autoSize={{ minRows: 1, maxRows: 3 }}
          style={{ flex: 1 }}
        />
        <Button 
          type="primary" 
          icon={<SendOutlined />} 
          onClick={handleSendMessage} 
          loading={loading}
          disabled={loading}
        >
          发送
        </Button>
      </Space>
      {loading && <Spin style={{ marginTop: 16 }} tip="AI助手思考中..." />}
    </div>
  )
}

export default AIAssistant