import React from 'react'
import { Menu } from 'antd'
import { 
  DashboardOutlined,
  StockOutlined,
  TeamOutlined,
  DollarOutlined,
  LineChartOutlined,
  RobotOutlined,
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const Sidebar = () => {
  const navigate = useNavigate()

  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: '仪表板',
      onClick: () => navigate('/dashboard'),
    },
    {
      key: '2',
      icon: <LineChartOutlined />,
      label: '股票分析',
      children: [
        {
          key: '2.1',
          label: '板块龙一龙二',
          onClick: () => navigate('/analysis/sector-leaders'),
        },
        {
          key: '2.2',
          label: '机构重仓股',
          onClick: () => navigate('/analysis/institutional-holdings'),
        },
        {
          key: '2.3',
          label: '中小票龙头',
          onClick: () => navigate('/analysis/small-cap-leaders'),
        },
        {
          key: '2.4',
          label: '低估股票',
          onClick: () => navigate('/analysis/undervalued-stocks'),
        },
        {
          key: '2.5',
          label: '综合评分',
          onClick: () => navigate('/analysis/comprehensive-score'),
        },
      ],
    },
    {
      key: '3',
      icon: <StockOutlined />,
      label: '自选股',
      onClick: () => navigate('/watchlist'), // 待实现页面
    },
    {
      key: '4',
      icon: <RobotOutlined />,
      label: 'AI智能助手',
      onClick: () => navigate('/ai-assistant'),
    },
  ]

  return (
    <Menu 
      theme="dark" 
      defaultSelectedKeys={['1']} 
      mode="inline" 
      items={menuItems} 
    />
  )
}

export default Sidebar
