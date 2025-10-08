import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

// 股票列表组件
const StockList = ({ stocks, onStockSelect }) => {
  return (
    <div className="stock-list">
      <h3>股票列表</h3>
      <div className="stock-grid">
        {stocks.map((stock) => (
          <div 
            key={stock.id} 
            className="stock-card"
            onClick={() => onStockSelect(stock)}
          >
            <h4>{stock.name}</h4>
            <p>代码: {stock.symbol}</p>
            <p>行业: {stock.industry || 'N/A'}</p>
            <p>市值: {stock.market_cap ? (stock.market_cap / 1e8).toFixed(2) + '亿' : 'N/A'}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// 技术面图表组件
const TechnicalChart = ({ data }) => {
  return (
    <div className="chart-container">
      <h3>股价走势</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="close" stroke="#8884d8" name="收盘价" />
          <Line type="monotone" dataKey="open" stroke="#82ca9d" name="开盘价" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

// 综合评分图表组件
const ScoreChart = ({ scores }) => {
  const data = [
    { name: '技术面', value: scores.technical_score },
    { name: '基本面', value: scores.fundamental_score },
    { name: '估值面', value: scores.valuation_score }
  ];
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];
  
  return (
    <div className="chart-container">
      <h3>综合评分分析</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" name="评分">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// 行业分布饼图组件
const IndustryPieChart = ({ data }) => {
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];
  
  return (
    <div className="chart-container">
      <h3>行业分布</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

// 龙头股排行榜组件
const DragonRanking = ({ dragons }) => {
  return (
    <div className="ranking-container">
      <h3>板块龙一龙二</h3>
      <table className="ranking-table">
        <thead>
          <tr>
            <th>排名</th>
            <th>股票名称</th>
            <th>股票代码</th>
            <th>行业</th>
            <th>评分</th>
          </tr>
        </thead>
        <tbody>
          {dragons.map((stock, index) => (
            <tr key={stock.stock.id}>
              <td>{index + 1}</td>
              <td>{stock.stock.name}</td>
              <td>{stock.stock.symbol}</td>
              <td>{stock.stock.industry || 'N/A'}</td>
              <td>{stock.score ? stock.score.toFixed(2) : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export { StockList, TechnicalChart, ScoreChart, IndustryPieChart, DragonRanking };