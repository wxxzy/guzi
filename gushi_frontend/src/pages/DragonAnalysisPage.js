import React, { useState, useEffect } from 'react';
import ApiService from '../utils/apiService';
import { DragonRanking, IndustryPieChart } from '../components/ChartComponents';

// 龙头股分析页面
const DragonAnalysisPage = () => {
  const [dragonsData, setDragonsData] = useState(null);
  const [sectorData, setSectorData] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeDragons = async () => {
    try {
      setLoading(true);
      const data = await ApiService.analyzeDragons(sectorData);
      setDragonsData(data);
    } catch (error) {
      console.error('龙一龙二分析失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeDragons(); // 默认分析全部
  }, []);

  return (
    <div className="analysis-page">
      <h1>板块龙一龙二分析</h1>
      
      <div className="analysis-controls">
        <input
          type="text"
          placeholder="输入行业名称（留空分析全部）"
          value={sectorData}
          onChange={(e) => setSectorData(e.target.value)}
        />
        <button className="btn" onClick={analyzeDragons} disabled={loading}>
          {loading ? '分析中...' : '开始分析'}
        </button>
      </div>
      
      {dragonsData && (
        <div>
          <div className="analysis-summary">
            <h3>分析结果</h3>
            <p>分析时间: {dragonsData.timestamp}</p>
            {dragonsData.dragons && dragonsData.dragons.length > 0 && (
              <div>
                <h4>板块龙头股</h4>
                <DragonRanking dragons={dragonsData.all_ranked || []} />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DragonAnalysisPage;