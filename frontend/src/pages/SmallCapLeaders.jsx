import React, { useState, useEffect } from 'react'
import { Table, message, Spin } from 'antd'
import { getSmallCapLeaders } from '../utils/api'

const SmallCapLeaders = () => {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchSmallCapLeaders = async () => {
      setLoading(true)
      try {
        const data = await getSmallCapLeaders()
        setStocks(data.stocks)
      } catch (error) {
        message.error(error.message || '获取中小票龙头失败')
        setStocks([])
      } finally {
        setLoading(false)
      }
    }

    fetchSmallCapLeaders()
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
      title: '中小票评分',
      dataIndex: 'small_cap_score',
      key: 'small_cap_score',
      sorter: (a, b) => a.small_cap_score - b.small_cap_score,
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
      title: '成交额',
      dataIndex: 'volume_amount',
      key: 'volume_amount',
      sorter: (a, b) => a.volume_amount - b.volume_amount,
      render: (text) => (text / 100000000).toFixed(2) + '亿', // 转换为亿元
    },
  ]

  return (
    <div>
      <h1>中小票龙头</h1>
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

export default SmallCapLeaders