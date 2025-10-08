import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';
import DragonAnalysisPage from '../pages/DragonAnalysisPage';
import InstitutionalAnalysisPage from '../pages/InstitutionalAnalysisPage';
import SmallCapAnalysisPage from '../pages/SmallCapAnalysisPage';
import UndervaluedAnalysisPage from '../pages/UndervaluedAnalysisPage';
import RankingPage from '../pages/RankingPage';

// 导航组件
const Navigation = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="main-nav">
      <div className="nav-brand">
        <Link to="/">智投AI</Link>
      </div>
      <ul className="nav-menu">
        <li>
          <Link to="/" className={isActive('/')}>仪表板</Link>
        </li>
        <li>
          <Link to="/dragons" className={isActive('/dragons')}>龙一龙二</Link>
        </li>
        <li>
          <Link to="/institutional" className={isActive('/institutional')}>机构重仓</Link>
        </li>
        <li>
          <Link to="/smallcap" className={isActive('/smallcap')}>中小票龙头</Link>
        </li>
        <li>
          <Link to="/undervalued" className={isActive('/undervalued')}>低估股票</Link>
        </li>
        <li>
          <Link to="/rankings" className={isActive('/rankings')}>综合排名</Link>
        </li>
      </ul>
    </nav>
  );
};

// 主应用路由
const AppRouter = () => {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dragons" element={<DragonAnalysisPage />} />
            <Route path="/institutional" element={<InstitutionalAnalysisPage />} />
            <Route path="/smallcap" element={<SmallCapAnalysisPage />} />
            <Route path="/undervalued" element={<UndervaluedAnalysisPage />} />
            <Route path="/rankings" element={<RankingPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default AppRouter;