import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';

// 股票排名页面
const RankingPage = () => {
  const [rankingsData, setRankingsData] = useState(null);
  const [limit, setLimit] = useState(20);
  const [loading, setLoading] = useState(false);

  const fetchRankings = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getStockRankings(limit);
      setRankingsData(data);
    } catch (error) {
      console.error('获取股票排名失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, [limit]);

  return (
    <div className="analysis-page">
      <h1>股票综合评分排名</h1>
      
      <div className="analysis-controls">
        <div>
          <label>显示数量: </label>
          <select 
            value={limit} 
            onChange={(e) => setLimit(Number(e.target.value))}
            disabled={loading}
          >
            <option value={10}>10只</option>
            <option value={20}>20只</option>
            <option value={50}>50只</option>
          </select>
        </div>
        <button className="btn" onClick={fetchRankings} disabled={loading}>
          {loading ? '加载中...' : '刷新排名'}
        </button>
      </div>
      
      {rankingsData && rankingsData.rankings && (
        <div className="analysis-summary">
          <p>更新时间: {rankingsData.rankings.timestamp}</p>
          <p>总分析股票数: {rankingsData.rankings.total_analyzed}</p>
          
          <table className="data-table">
            <thead>
              <tr>
                <th>排名</th>
                <th>股票名称</th>
                <th>股票代码</th>
                <th>综合评分</th>
                <th>技术面</th>
                <th>基本面</th>
                <th>估值面</th>
                <th>评级</th>
              </tr>
            </thead>
            <tbody>
              {rankingsData.rankings.rankings.map((item, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{item.stock.name}</td>
                  <td>{item.stock.symbol}</td>
                  <td><strong>{item.comprehensive_score}</strong></td>
                  <td>{item.technical_score}</td>
                  <td>{item.fundamental_score}</td>
                  <td>{item.valuation_score}</td>
                  <td>
                    <span className={`rating ${item.rating.includes('推荐') ? 'positive' : item.rating.includes('回避') ? 'negative' : 'neutral'}`}>
                      {item.rating}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default RankingPage;