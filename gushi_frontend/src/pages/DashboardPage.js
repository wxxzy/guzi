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
    setLoading(true); // 开启加载状态
    try {
      await Promise.all([
        fetchStockHistory(stock.symbol),
        fetchComprehensiveScore(stock.symbol)
      ]);
    } catch (error) {
      console.error('获取股票数据失败:', error);
    } finally {
      setLoading(false); // 关闭加载状态
    }
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
      
      // 启动后台任务
      const taskResponse = await ApiService.startTask('dragon', { sector: '' });
      const taskId = taskResponse.task_id;
      
      // 设置初始状态
      setAnalysisResult({
        message: '正在开始板块龙一龙二分析...',
        loading: true,
        taskId: taskId,  // 存储任务ID
        currentStep: '初始化',
        progress: 0,
        analyzedCount: 0,
        totalCount: 0,
        timestamp: new Date().toISOString()
      });
      
      // 定时查询任务状态
      const pollInterval = setInterval(async () => {
        try {
          const status = await ApiService.getTaskStatus(taskId);
          
          if (status.status === 'completed') {
            // 任务完成，清除定时器
            clearInterval(pollInterval);
            setAnalysisResult({
              ...status.result,
              loading: false,
              taskId: taskId
            });
            setLoading(false);
          } else if (status.status === 'failed') {
            // 任务失败，清除定时器
            clearInterval(pollInterval);
            setAnalysisResult({
              error: status.error || '任务执行失败',
              loading: false,
              taskId: taskId
            });
            setLoading(false);
          } else {
            // 更新进度状态
            setAnalysisResult(prev => ({
              ...prev,
              loading: true,
              taskId: taskId,
              progress: status.progress || 0,
              currentStep: status.current_step || '处理中',
              currentItem: status.current_item || null,
              message: status.current_step || '分析进行中...'
            }));
          }
        } catch (error) {
          console.error('获取任务状态失败:', error);
          clearInterval(pollInterval);
          setAnalysisResult({
            error: '获取任务状态失败: ' + error.message,
            loading: false
          });
          setLoading(false);
        }
      }, 1000); // 每秒查询一次状态
      
      // 设置定时器清除（如果任务长时间没有完成）
      setTimeout(() => {
        clearInterval(pollInterval);
      }, 600000); // 10分钟超时
      
    } catch (error) {
      console.error('启动龙一龙二分析任务失败:', error);
      setAnalysisResult({
        error: '启动分析任务失败: ' + (error.message || '未知错误'),
        timestamp: new Date().toISOString()
      });
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
                        <div className="comprehensive-score-container">
                          {/* 综合评分展示区域 */}
                          <div className="score-summary">
                            <div className="score-item">
                              <h4>综合评分</h4>
                              <div className="score-value">{analysisResult.comprehensive_analysis.comprehensive_score}</div>
                              <div className="rating-badge">{analysisResult.comprehensive_analysis.rating}</div>
                            </div>
                            <div className="score-details">
                              <div className="score-detail">
                                <span className="detail-label">技术面:</span>
                                <span className="detail-value">{analysisResult.comprehensive_analysis.technical_score}</span>
                              </div>
                              <div className="score-detail">
                                <span className="detail-label">基本面:</span>
                                <span className="detail-value">{analysisResult.comprehensive_analysis.fundamental_score}</span>
                              </div>
                              <div className="score-detail">
                                <span className="detail-label">估值面:</span>
                                <span className="detail-value">{analysisResult.comprehensive_analysis.valuation_score}</span>
                              </div>
                            </div>
                          </div>
                          
                          {/* 分数图表 */}
                          <ScoreChart scores={analysisResult.comprehensive_analysis} />
                        </div>
                      ) : analysisResult.loading ? (
                        <div className="loading-analysis">
                          <h4>分析进行中...</h4>
                          <p>{analysisResult.message}</p>
                          
                          {/* 进度条 */}
                          <div className="progress-container">
                            <div className="progress-bar">
                              <div 
                                className="progress-fill" 
                                style={{ width: `${analysisResult.progress || 0}%` }}
                              ></div>
                            </div>
                            <div className="progress-text">
                              {analysisResult.progress || 0}%
                            </div>
                          </div>
                          
                          {/* 当前步骤和具体项目 */}
                          {analysisResult.currentStep && (
                            <div className="current-step">
                              当前步骤: {analysisResult.currentStep}
                              {analysisResult.currentItem && (
                                <div className="current-item">
                                  正在处理: {analysisResult.currentItem}
                                </div>
                              )}
                            </div>
                          )}
                          
                          {/* 任务ID显示 */}
                          {analysisResult.taskId && (
                            <div className="task-id">
                              任务ID: {analysisResult.taskId}
                            </div>
                          )}
                        </div>
                      ) : analysisResult.dragons ? (
                        // 龙一龙二分析结果展示
                        <div className="dragon-analysis-result">
                          <h4>板块龙一龙二分析结果</h4>
                          <div className="dragon-stocks">
                            <h5>龙一龙二:</h5>
                            <div className="dragon-list">
                              {analysisResult.dragons.map((dragon, index) => (
                                <div key={dragon.id} className="dragon-item">
                                  <span className="dragon-rank">龙{index === 0 ? '一' : '二'}</span>
                                  <span className="dragon-name">{dragon.name}</span>
                                  <span className="dragon-symbol">{dragon.symbol}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                          
                          {analysisResult.all_ranked && analysisResult.all_ranked.length > 0 && (
                            <div className="top-stocks-section">
                              <h5>前10名股票:</h5>
                              <table className="top-stocks-table">
                                <thead>
                                  <tr>
                                    <th>排名</th>
                                    <th>名称</th>
                                    <th>代码</th>
                                    <th>行业</th>
                                    <th>评分</th>
                                    <th>涨幅%</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {analysisResult.all_ranked.slice(0, 10).map((rankedItem, index) => (
                                    <tr key={rankedItem.stock.id}>
                                      <td>{index + 1}</td>
                                      <td>{rankedItem.stock.name}</td>
                                      <td>{rankedItem.stock.symbol}</td>
                                      <td>{rankedItem.stock.industry || 'N/A'}</td>
                                      <td>{rankedItem.score ? rankedItem.score.toFixed(2) : 'N/A'}</td>
                                      <td>{rankedItem.price_change_pct ? rankedItem.price_change_pct.toFixed(2) : 'N/A'}</td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          )}
                        </div>
                      ) : analysisResult.error ? (
                        <div className="error-analysis">
                          <h4>分析出错</h4>
                          <p className="error-message">{analysisResult.error}</p>
                        </div>
                      ) : (
                        <div className="raw-analysis-result">
                          <h4>分析详情</h4>
                          <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
                        </div>
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