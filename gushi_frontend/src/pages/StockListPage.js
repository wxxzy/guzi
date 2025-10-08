import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';

const StockListPage = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStockList();
  }, []);

  const fetchStockList = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getStockList();
      setStocks(data || []);
      setError(null);
    } catch (err) {
      setError('获取股票列表失败: ' + err.message);
      console.error('获取股票列表失败:', err);
    } finally {
      setLoading(false);
    }
  };

  // 表格列定义
  const columns = [
    { key: 'symbol', label: '股票代码', width: '120px' },
    { key: 'name', label: '股票名称', width: '150px' },
    { key: 'industry', label: '行业', width: '150px' },
    { key: 'market_cap', label: '市值(亿)', width: '100px' },
    { key: 'pe_ratio', label: '市盈率', width: '100px' },
    { key: 'pb_ratio', label: '市净率', width: '100px' }
  ];

  // 格式化市值
  const formatMarketCap = (marketCap) => {
    if (marketCap === null || marketCap === undefined) return 'N/A';
    return (marketCap / 1e8).toFixed(2);
  };

  // 格式化数值
  const formatValue = (value, precision = 2) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    if (value === 0) return '0';
    return Number(value).toFixed(precision);
  };

  return (
    <div className="stock-list-page">
      <div className="page-header">
        <h1>股票列表</h1>
        <div className="page-controls">
          <button className="btn" onClick={fetchStockList} disabled={loading}>
            {loading ? '加载中...' : '刷新数据'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button className="btn" onClick={fetchStockList}>重试</button>
        </div>
      )}

      <div className="stock-list-container">
        {loading ? (
          <div className="loading">加载中...</div>
        ) : (
          <div className="table-container">
            <table className="stock-table">
              <thead>
                <tr>
                  {columns.map((column) => (
                    <th key={column.key} style={{ width: column.width }}>
                      {column.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {stocks && stocks.length > 0 ? (
                  stocks.map((stock) => (
                    <tr key={stock.symbol}>
                      <td>{stock.symbol}</td>
                      <td>{stock.name}</td>
                      <td>{stock.industry || 'N/A'}</td>
                      <td>{formatMarketCap(stock.market_cap)}</td>
                      <td>{formatValue(stock.pe_ratio)}</td>
                      <td>{formatValue(stock.pb_ratio)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={columns.length} style={{ textAlign: 'center' }}>
                      暂无股票数据
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {stocks && stocks.length > 0 && (
        <div className="table-footer">
          <p>共 {stocks.length} 只股票</p>
        </div>
      )}
    </div>
  );
};

export default StockListPage;