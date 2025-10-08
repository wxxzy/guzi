import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';

// 低估股票分析页面
const UndervaluedAnalysisPage = () => {
  const [undervaluedData, setUndervaluedData] = useState(null);
  const [criteria, setCriteria] = useState({
    pe_threshold: 15,
    pb_threshold: 1.5,
  });
  const [loading, setLoading] = useState(false);

  const analyzeUndervalued = async () => {
    try {
      setLoading(true);
      const data = await ApiService.analyzeUndervaluedStocks(criteria);
      setUndervaluedData(data);
    } catch (error) {
      console.error('低估股票分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeUndervalued();
  }, []);

  return (
    <div className="analysis-page">
      <h1>低估股票分析</h1>
      
      <div className="analysis-controls">
        <div>
          <label>PE阈值: </label>
          <input
            type="number"
            step="0.1"
            value={criteria.pe_threshold}
            onChange={(e) => setCriteria({...criteria, pe_threshold: Number(e.target.value)})}
          />
        </div>
        <div>
          <label>PB阈值: </label>
          <input
            type="number"
            step="0.1"
            value={criteria.pb_threshold}
            onChange={(e) => setCriteria({...criteria, pb_threshold: Number(e.target.value)})}
          />
        </div>
        <button className="btn" onClick={analyzeUndervalued} disabled={loading}>
          {loading ? '分析中...' : '开始分析'}
        </button>
      </div>
      
      {undervaluedData && (
        <div>
          <div className="analysis-summary">
            <h3>低估股票</h3>
            {undervaluedData.detailed_analysis && (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>股票名称</th>
                    <th>股票代码</th>
                    <th>估值评分</th>
                    <th>PE</th>
                    <th>PB</th>
                  </tr>
                </thead>
                <tbody>
                  {undervaluedData.detailed_analysis.map((item, index) => (
                    <tr key={index}>
                      <td>{item.stock.name}</td>
                      <td>{item.stock.symbol}</td>
                      <td>{item.valuation_score ? item.valuation_score.toFixed(2) : 'N/A'}</td>
                      <td>{item.pe_ratio ? item.pe_ratio.toFixed(2) : 'N/A'}</td>
                      <td>{item.pb_ratio ? item.pb_ratio.toFixed(2) : 'N/A'}</td>
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

export default UndervaluedAnalysisPage;