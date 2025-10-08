import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';
import { StockList, TechnicalChart, ScoreChart, IndustryPieChart, DragonRanking } from '../components/ChartComponents';
import NaturalLanguageQuery from '../components/NaturalLanguageQuery';
import PersonalizedRecommendation from '../components/PersonalizedRecommendation';

// 仪表板页面
const DashboardPage = () => {
  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockHistory, setStockHistory] = useState([]);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getStockList();
      setStocks(data || []);
    } catch (error) {
      console.error('获取股票列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStockSelect = async (stock) => {
    setSelectedStock(stock);
    await fetchStockHistory(stock.symbol);
    await fetchComprehensiveScore(stock.symbol);
  };

  const fetchStockHistory = async (symbol) => {
    try {
      setLoading(true);
      // 获取最近30天的数据
      const endDate = new Date().toISOString().split('T')[0];
      const startDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      
      const data = await ApiService.getStockHistory(symbol, startDate, endDate);
      // 格式化数据给图表使用
      const formattedData = (data || []).map(item => ({
        date: item.date,
        open: item.open_price,
        close: item.close_price,
        high: item.high_price,
        low: item.low_price,
        volume: item.volume
      }));
      setStockHistory(formattedData);
    } catch (error) {
      console.error(`获取股票 ${symbol} 历史数据失败:`, error);
    } finally {
      setLoading(false);
    }
  };

  const fetchComprehensiveScore = async (symbol) => {
    try {
      setLoading(true);
      const result = await ApiService.getComprehensiveScore(symbol);
      setAnalysisResult(result);
    } catch (error) {
      console.error(`获取股票 ${symbol} 综合评分失败:`, error);
    } finally {
      setLoading(false);
    }
  };

  const handleAIAnalysis = async (type = 'comprehensive') => {
    if (!selectedStock) return;
    
    try {
      setLoading(true);
      const result = await ApiService.aiStockAnalysis(selectedStock.symbol, type);
      setAnalysisResult(result);
    } catch (error) {
      console.error('AI分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDragonAnalysis = async () => {
    try {
      setLoading(true);
      const result = await ApiService.analyzeDragons();
      setAnalysisResult(result);
    } catch (error) {
      console.error('龙一龙二分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>智投AI - 股票智能分析系统</h1>
        <div className="dashboard-controls">
          <button className="btn" onClick={handleDragonAnalysis} disabled={loading}>
            {loading ? '分析中...' : '板块龙一龙二分析'}
          </button>
        </div>
      </div>

      {loading && <div className="loading">加载中...</div>}

      <div className="dashboard-content">
        <div className="main-content">
          {/* 股票列表 */}
          <div className="section">
            <StockList 
              stocks={stocks} 
              onStockSelect={handleStockSelect} 
            />
          </div>

          {/* 选项卡 */}
          <div className="tabs">
            <button 
              className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              综览
            </button>
            <button 
              className={`tab-btn ${activeTab === 'technical' ? 'active' : ''}`}
              onClick={() => setActiveTab('technical')}
            >
              技术面
            </button>
            <button 
              className={`tab-btn ${activeTab === 'fundamental' ? 'active' : ''}`}
              onClick={() => setActiveTab('fundamental')}
            >
              基本面
            </button>
          </div>

          {/* 内容区域 */}
          {activeTab === 'overview' && (
            <div className="tab-content">
              {selectedStock && (
                <div className="stock-detail">
                  <h2>{selectedStock.name} ({selectedStock.symbol})</h2>
                  <div className="stock-info">
                    <p><strong>行业:</strong> {selectedStock.industry || 'N/A'}</p>
                    <p><strong>市值:</strong> {selectedStock.market_cap ? (selectedStock.market_cap / 1e8).toFixed(2) + '亿' : 'N/A'}</p>
                    <p><strong>PE:</strong> {selectedStock.pe_ratio ? selectedStock.pe_ratio.toFixed(2) : 'N/A'}</p>
                    <p><strong>PB:</strong> {selectedStock.pb_ratio ? selectedStock.pb_ratio.toFixed(2) : 'N/A'}</p>
                  </div>
                  
                  <div className="analysis-controls">
                    <button className="btn" onClick={() => handleAIAnalysis('comprehensive')}>
                      AI综合分析
                    </button>
                    <button className="btn" onClick={() => handleAIAnalysis('technical')}>
                      AI技术面分析
                    </button>
                    <button className="btn" onClick={() => handleAIAnalysis('fundamental')}>
                      AI基本面分析
                    </button>
                  </div>
                  
                  {analysisResult && (
                    <div className="analysis-result">
                      <h3>分析结果</h3>
                      {analysisResult.comprehensive_analysis ? (
                        <div>
                          <h4>综合评分: {analysisResult.comprehensive_analysis.comprehensive_score}</h4>
                          <p>评级: {analysisResult.comprehensive_analysis.rating}</p>
                          <ScoreChart scores={analysisResult.comprehensive_analysis} />
                        </div>
                      ) : (
                        <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'technical' && (
            <div className="tab-content">
              {stockHistory.length > 0 && (
                <TechnicalChart data={stockHistory} />
              )}
            </div>
          )}

          {activeTab === 'fundamental' && (
            <div className="tab-content">
              <div className="fundamental-analysis">
                <h3>基本面分析</h3>
                <p>当前选择的股票: {selectedStock ? `${selectedStock.name} (${selectedStock.symbol})` : '请选择股票'}</p>
                {selectedStock && (
                  <div className="fundamental-data">
                    <p><strong>市盈率 (PE):</strong> {selectedStock.pe_ratio ? selectedStock.pe_ratio.toFixed(2) : 'N/A'}</p>
                    <p><strong>市净率 (PB):</strong> {selectedStock.pb_ratio ? selectedStock.pb_ratio.toFixed(2) : 'N/A'}</p>
                    <p><strong>行业:</strong> {selectedStock.industry || 'N/A'}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="sidebar">
            <div className="sidebar-widget">
              <NaturalLanguageQuery />
            </div>
            
            <div className="sidebar-widget">
              <PersonalizedRecommendation />
            </div>
            
            <div className="sidebar-widget">
              <h3>市场概况</h3>
              <p>今日A股整体表现...</p>
            </div>
            
            <div className="sidebar-widget">
              <h3>热门板块</h3>
              <ul>
                <li>科技板块 +2.3%</li>
                <li>消费板块 +1.2%</li>
                <li>金融板块 -0.5%</li>
              </ul>
            </div>
          </div>
      </div>
    </div>
  );
};

export default DashboardPage;