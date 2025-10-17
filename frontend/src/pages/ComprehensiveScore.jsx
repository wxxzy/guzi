import React, { useState, useEffect } from 'react'
import { Table, message, Spin } from 'antd'
import { getComprehensiveScore } from '../utils/api'

const ComprehensiveScore = () => {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchComprehensiveScores = async () => {
      setLoading(true)
      try {
        const data = await getComprehensiveScore()
        setStocks(data.stocks)
      } catch (error) {
        message.error(error.message || '获取综合评分失败')
        setStocks([])
      } finally {
        setLoading(false)
      }
    }

    fetchComprehensiveScores()
  }, [])

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '所属行业',
      dataIndex: 'industry',
      key: 'industry',
    },
    {
      title: '综合评分',
      dataIndex: 'comprehensive_score',
      key: 'comprehensive_score',
      sorter: (a, b) => a.comprehensive_score - b.comprehensive_score,
      render: (text) => text.toFixed(2),
    },
    {
      title: '总市值',
      dataIndex: 'market_cap',
      key: 'market_cap',
      sorter: (a, b) => a.market_cap - b.market_cap,
      render: (text) => (text / 100000000).toFixed(2) + '亿', // 转换为亿元
    },
    {
      title: '涨跌幅',
      dataIndex: 'change_percent',
      key: 'change_percent',
      sorter: (a, b) => a.change_percent - b.change_percent,
      render: (text) => `${text.toFixed(2)}%`,
    },
    {
      title: '市盈率 (PE)',
      dataIndex: 'pe',
      key: 'pe',
      sorter: (a, b) => a.pe - b.pe,
      render: (text) => text.toFixed(2),
    },
    {
      title: '市净率 (PB)',
      dataIndex: 'pb',
      key: 'pb',
      sorter: (a, b) => a.pb - b.pb,
      render: (text) => text.toFixed(2),
    },
  ]

  return (
    <div>
      <h1>综合评分</h1>
      <Spin spinning={loading}>
        <Table 
          columns={columns} 
          dataSource={stocks} 
          rowKey="code" 
          pagination={{ pageSize: 10 }} 
          scroll={{ x: 'max-content' }} // 允许横向滚动
        />
      </Spin>
    </div>
  )
}

export default ComprehensiveScore