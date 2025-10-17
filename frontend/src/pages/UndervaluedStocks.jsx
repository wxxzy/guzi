import React, { useState, useEffect } from 'react'
import { Table, message, Spin } from 'antd'
import { getUndervaluedStocks } from '../utils/api'

const UndervaluedStocks = () => {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchUndervaluedStocks = async () => {
      setLoading(true)
      try {
        const data = await getUndervaluedStocks()
        setStocks(data.stocks)
      } catch (error) {
        message.error(error.message || '获取低估股票失败')
        setStocks([])
      } finally {
        setLoading(false)
      }
    }

    fetchUndervaluedStocks()
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
      title: '低估评分',
      dataIndex: 'undervalued_score',
      key: 'undervalued_score',
      sorter: (a, b) => a.undervalued_score - b.undervalued_score,
      render: (text) => text.toFixed(2),
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
      <h1>低估股票</h1>
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

export default UndervaluedStocks