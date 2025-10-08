import React, { useState } from 'react';
import ApiService from '../utils/apiService';

// 个性化推荐组件
const PersonalizedRecommendation = ({ onRecommendation }) => {
  const [riskTolerance, setRiskTolerance] = useState('medium');
  const [investmentGoal, setInvestmentGoal] = useState('balanced');
  const [investmentHorizon, setInvestmentHorizon] = useState('medium');
  const [capitalSize, setCapitalSize] = useState('medium');
  const [investmentExperience, setInvestmentExperience] = useState('intermediate');
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const userProfile = {
      risk_tolerance: riskTolerance,
      investment_goal: investmentGoal,
      investment_horizon: investmentHorizon,
      capital_size: capitalSize,
      investment_experience: investmentExperience
    };

    try {
      setLoading(true);
      setRecommendation(null);
      
      const response = await ApiService.getPersonalizedRecommendation(userProfile);
      setRecommendation(response);
      
      if (onRecommendation) {
        onRecommendation(response);
      }
    } catch (error) {
      console.error('获取个性化推荐失败:', error);
      setRecommendation({
        error: '推荐失败: ' + error.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="personalized-recommendation">
      <h3>个性化投资建议</h3>
      <form onSubmit={handleSubmit} className="recommendation-form">
        <div className="form-row">
          <div className="form-group">
            <label>风险偏好:</label>
            <select 
              value={riskTolerance} 
              onChange={(e) => setRiskTolerance(e.target.value)}
            >
              <option value="low">低风险</option>
              <option value="medium">中风险</option>
              <option value="high">高风险</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>投资目标:</label>
            <select 
              value={investmentGoal} 
              onChange={(e) => setInvestmentGoal(e.target.value)}
            >
              <option value="capital_preservation">本金保障</option>
              <option value="balanced">平衡增长</option>
              <option value="growth">积极增长</option>
              <option value="aggressive_growth">激进增长</option>
            </select>
          </div>
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label>投资期限:</label>
            <select 
              value={investmentHorizon} 
              onChange={(e) => setInvestmentHorizon(e.target.value)}
            >
              <option value="short">短期(1年以内)</option>
              <option value="medium">中期(1-3年)</option>
              <option value="long">长期(3年以上)</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>资金规模:</label>
            <select 
              value={capitalSize} 
              onChange={(e) => setCapitalSize(e.target.value)}
            >
              <option value="small">小额(10万以下)</option>
              <option value="medium">中等(10-50万)</option>
              <option value="large">大额(50万以上)</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label>投资经验:</label>
          <select 
            value={investmentExperience} 
            onChange={(e) => setInvestmentExperience(e.target.value)}
          >
            <option value="beginner">初级</option>
            <option value="intermediate">中级</option>
            <option value="advanced">高级</option>
          </select>
        </div>
        
        <button type="submit" className="btn" disabled={loading}>
          {loading ? '生成建议中...' : '生成个性化建议'}
        </button>
      </form>

      {recommendation && (
        <div className="recommendation-result">
          <h4>投资建议</h4>
          {recommendation.error ? (
            <div className="error">{recommendation.error}</div>
          ) : (
            <div>
              <div className="user-profile">
                <h5>您的画像:</h5>
                <p>风险偏好: {recommendation.user_profile.risk_tolerance}</p>
                <p>投资目标: {recommendation.user_profile.investment_goal}</p>
                <p>投资期限: {recommendation.user_profile.investment_horizon}</p>
                <p>资金规模: {recommendation.user_profile.capital_size}</p>
                <p>投资经验: {recommendation.user_profile.investment_experience}</p>
              </div>
              
              <div className="recommendation-content">
                <pre>{recommendation.recommendation}</pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PersonalizedRecommendation;