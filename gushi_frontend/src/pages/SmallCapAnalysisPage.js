import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';

// 中小票龙头股分析页面
const SmallCapAnalysisPage = () => {
  const [smallCapData, setSmallCapData] = useState(null);
  const [maxMarketCap, setMaxMarketCap] = useState(10000000000); // 100亿
  const [loading, setLoading] = useState(false);

  const analyzeSmallCap = async () => {
    try {
      setLoading(true);
      const data = await ApiService.analyzeSmallCapLeaders(maxMarketCap);
      setSmallCapData(data);
    } catch (error) {
      console.error('中小票龙头股分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeSmallCap();
  }, []);

  return (
    <div className="analysis-page">
      <h1>中小票龙头股分析</h1>
      
      <div className="analysis-controls">
        <div>
          <label>最大市值 (元): </label>
          <input
            type="number"
            value={maxMarketCap}
            onChange={(e) => setMaxMarketCap(Number(e.target.value))}
          />
        </div>
        <button className="btn" onClick={analyzeSmallCap} disabled={loading}>
          {loading ? '分析中...' : '开始分析'}
        </button>
      </div>
      
      {smallCapData && (
        <div>
          <div className="analysis-summary">
            <h3>中小票龙头股</h3>
            {smallCapData.top_leaders && (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>排名</th>
                    <th>股票名称</th>
                    <th>股票代码</th>
                    <th>评分</th>
                    <th>价格涨幅%</th>
                    <th>动量指标</th>
                    <th>平均成交量</th>
                  </tr>
                </thead>
                <tbody>
                  {smallCapData.top_leaders.map((item, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{item.stock.name}</td>
                      <td>{item.stock.symbol}</td>
                      <td>{item.score ? item.score.toFixed(2) : 'N/A'}</td>
                      <td>{item.price_change_pct ? item.price_change_pct.toFixed(2) : 'N/A'}</td>
                      <td>{item.momentum ? item.momentum.toFixed(2) : 'N/A'}</td>
                      <td>{item.avg_volume}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SmallCapAnalysisPage;