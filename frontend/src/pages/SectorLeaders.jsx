import React, { useState, useEffect } from 'react'
import { Table, Select, message, Spin } from 'antd'
import { getSectorLeaders } from '../utils/api'

const { Option } = Select

const SectorLeaders = () => {
  const [leaders, setLeaders] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedIndustry, setSelectedIndustry] = useState('银行') // 默认选择银行
  const [industries, setIndustries] = useState(['银行', '房地产开发', '煤炭行业', '航运港口', '教育', '珠宝首饰']) // 暂时硬编码行业列表

  useEffect(() => {
    const fetchLeaders = async () => {
      if (!selectedIndustry) return

      setLoading(true)
      try {
        const data = await getSectorLeaders(selectedIndustry)
        setLeaders(data.leaders)
      } catch (error) {
        message.error(error.message || '获取板块龙头失败')
        setLeaders([])
      } finally {
        setLoading(false)
      }
    }

    fetchLeaders()
  }, [selectedIndustry])

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
      dataIndex: 'score',
      key: 'score',
      sorter: (a, b) => a.score - b.score,
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
      <h1>板块龙一龙二</h1>
      <div style={{ marginBottom: 16 }}>
        选择行业：
        <Select
          showSearch
          style={{ width: 200 }}
          placeholder="选择一个行业"
          optionFilterProp="children"
          onChange={(value) => setSelectedIndustry(value)}
          value={selectedIndustry}
          filterOption={(input, option) =>
            (option?.children ?? '').toLowerCase().includes(input.toLowerCase())
          }
        >
          {industries.map((industry) => (
            <Option key={industry} value={industry}>
              {industry}
            </Option>
          ))}
        </Select>
      </div>
      <Spin spinning={loading}>
        <Table 
          columns={columns} 
          dataSource={leaders} 
          rowKey="code" 
          pagination={false} 
          scroll={{ x: 'max-content' }} // 允许横向滚动
        />
      </Spin>
    </div>
  )
}

export default SectorLeaders