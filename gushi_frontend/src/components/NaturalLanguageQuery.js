import React, { useState } from 'react';
import ApiService from '../utils/apiService';

// 自然语言查询组件
const NaturalLanguageQuery = ({ onResult }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setLoading(true);
      setResult(null);
      
      const response = await ApiService.processNaturalLanguageQuery(query);
      setResult(response);
      
      if (onResult) {
        onResult(response);
      }
    } catch (error) {
      console.error('自然语言查询失败:', error);
      setResult({
        error: '查询失败: ' + error.message,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="natural-language-query">
      <h3>智能问答</h3>
      <form onSubmit={handleQuerySubmit} className="query-form">
        <div className="query-input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="请输入您的问题，例如：'600519股价如何'、'比较000001和000002'等"
            className="query-input"
          />
          <button type="submit" className="btn" disabled={loading}>
            {loading ? '分析中...' : '查询'}
          </button>
        </div>
      </form>

      {result && (
        <div className="query-result">
          <h4>分析结果</h4>
          {result.error ? (
            <div className="error">{result.error}</div>
          ) : (
            <div>
              <div className="result-type">类型: {result.type}</div>
              {result.type === 'stock_info' && (
                <div>
                  <p>{result.message}</p>
                  {result.symbols && <p>涉及股票: {result.symbols.join(', ')}</p>}
                </div>
              )}
              {result.type === 'analysis_result' && (
                <div className="analysis-content">
                  <pre>{result.analysis}</pre>
                </div>
              )}
              {result.type === 'comparison_result' && (
                <div className="comparison-content">
                  <pre>{result.comparison}</pre>
                </div>
              )}
              {result.type === 'market_analysis' && (
                <div className="market-content">
                  <pre>{result.analysis}</pre>
                </div>
              )}
              {result.type === 'general_response' && (
                <div className="general-content">
                  <pre>{result.response}</pre>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NaturalLanguageQuery;