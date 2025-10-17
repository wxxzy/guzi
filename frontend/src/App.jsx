import React from 'react'
import { Layout, theme } from 'antd'
import { Routes, Route } from 'react-router-dom'
import AppHeader from './components/AppHeader'
import Sidebar from './components/Sidebar'

// 导入页面组件
import Dashboard from './pages/Dashboard'
import SectorLeaders from './pages/SectorLeaders'
import InstitutionalHoldings from './pages/InstitutionalHoldings'
import UndervaluedStocks from './pages/UndervaluedStocks'
import ComprehensiveScore from './pages/ComprehensiveScore'
import AIAssistant from './pages/AIAssistant'
import Watchlist from './pages/Watchlist'
import SmallCapLeaders from './pages/SmallCapLeaders'

const { Content, Footer, Sider } = Layout

const App = () => {
  const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken()

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        breakpoint="lg"
        collapsedWidth="0"
        onBreakpoint={(broken) => {
          console.log(broken)
        }}
        onCollapse={(collapsed, type) => {
          console.log(collapsed, type)
        }}
      >
        <div className="demo-logo-vertical" />
        <Sidebar />
      </Sider>
      <Layout>
        <AppHeader />
        <Content style={{ margin: '24px 16px 0' }}>
          <div
            style={{
              padding: 24,
              minHeight: 360,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/analysis/sector-leaders" element={<SectorLeaders />} />
              <Route path="/analysis/institutional-holdings" element={<InstitutionalHoldings />} />
              <Route path="/analysis/small-cap-leaders" element={<SmallCapLeaders />} />
              <Route path="/analysis/undervalued-stocks" element={<UndervaluedStocks />} />
              <Route path="/analysis/comprehensive-score" element={<ComprehensiveScore />} />
              <Route path="/ai-assistant" element={<AIAssistant />} />
              <Route path="/watchlist" element={<Watchlist />} />
              {/* 可以添加404页面 */}
              <Route path="*" element={<div>404 Not Found</div>} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          Guzi Stock Analysis System ©{new Date().getFullYear()} Created by Gemini
        </Footer>
      </Layout>
    </Layout>
  )
}

export default App
