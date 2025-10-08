import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';

// 机构重仓股分析页面
const InstitutionalAnalysisPage = () => {
  const [institutionalData, setInstitutionalData] = useState(null);
  const [filters, setFilters] = useState({
    min_market_cap: 5000000000, // 50亿
    min_roe: 0.08, // 8%
  });
  const [loading, setLoading] = useState(false);

  const analyzeInstitutional = async () => {
    try {
      setLoading(true);
      const data = await ApiService.analyzeInstitutionalStocks(filters);
      setInstitutionalData(data);
    } catch (error) {
      console.error('机构重仓股分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeInstitutional();
  }, []);

  return (
    <div className="analysis-page">
      <h1>机构重仓股分析</h1>
      
      <div className="analysis-controls">
        <div>
          <label>最低市值 (元): </label>
          <input
            type="number"
            value={filters.min_market_cap}
            onChange={(e) => setFilters({...filters, min_market_cap: Number(e.target.value)})}
          />
        </div>
        <div>
          <label>最低ROE: </label>
          <input
            type="number"
            step="0.01"
            value={filters.min_roe}
            onChange={(e) => setFilters({...filters, min_roe: Number(e.target.value)})}
          />
        </div>
        <button className="btn" onClick={analyzeInstitutional} disabled={loading}>
          {loading ? '分析中...' : '开始分析'}
        </button>
      </div>
      
      {institutionalData && (
        <div>
          <div className="analysis-summary">
            <h3>机构重仓股候选</h3>
            {institutionalData.top_candidates && (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>股票名称</th>
                    <th>股票代码</th>
                    <th>评分</th>
                    <th>平均成交量</th>
                    <th>价格波动率</th>
                  </tr>
                </thead>
                <tbody>
                  {institutionalData.top_candidates.slice(0, 10).map((item, index) => (
                    <tr key={index}>
                      <td>{item.stock.name}</td>
                      <td>{item.stock.symbol}</td>
                      <td>{item.score ? item.score.toFixed(2) : 'N/A'}</td>
                      <td>{item.avg_volume}</td>
                      <td>{item.price_volatility ? item.price_volatility.toFixed(4) : 'N/A'}</td>
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

export default InstitutionalAnalysisPage;