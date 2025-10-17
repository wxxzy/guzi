import React from 'react'
import { Layout, theme, Space, Avatar, Dropdown, Menu } from 'antd'
import { UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons'

const { Header } = Layout

const AppHeader = () => {
  const { token: { colorBgContainer } } = theme.useToken()

  const menu = (
    <Menu
      items={[
        {
          key: '1',
          label: (
            <a target="_blank" rel="noopener noreferrer" href="#">
              <SettingOutlined /> 个人设置
            </a>
          ),
        },
        {
          key: '2',
          label: (
            <a target="_blank" rel="noopener noreferrer" href="#">
              <LogoutOutlined /> 退出登录
            </a>
          ),
        },
      ]}
    />
  )

  return (
    <Header style={{ padding: 0, background: colorBgContainer }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '100%', padding: '0 24px' }}>
        <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
          股票智能分析系统
        </div>
        <Space size="middle">
          <Dropdown overlay={menu} placement="bottomRight" arrow>
            <Avatar size="default" icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
          </Dropdown>
        </Space>
      </div>
    </Header>
  )
}

export default AppHeader
