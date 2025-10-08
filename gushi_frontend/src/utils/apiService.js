import axios from 'axios';

// API基础URL - 开发环境下使用后端代理
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com' 
  : 'http://localhost:5000';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么，比如添加认证token
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response.data;
  },
  (error) => {
    // 对响应错误做点什么
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API服务类
class ApiService {
  // 获取股票列表
  static async getStockList() {
    try {
      const response = await apiClient.get('/api/stock/list');
      return response;
    } catch (error) {
      console.error('获取股票列表失败:', error);
      throw error;
    }
  }

  // 获取股票详情
  static async getStockDetail(symbol) {
    try {
      const response = await apiClient.get(`/api/stock/${symbol}`);
      return response;
    } catch (error) {
      console.error(`获取股票 ${symbol} 详情失败:`, error);
      throw error;
    }
  }

  // 获取股票历史数据
  static async getStockHistory(symbol, startDate, endDate) {
    try {
      const response = await apiClient.get(`/api/stock/${symbol}/history`, {
        params: { start_date: startDate, end_date: endDate }
      });
      return response;
    } catch (error) {
      console.error(`获取股票 ${symbol} 历史数据失败:`, error);
      throw error;
    }
  }

  // 板块龙一龙二分析
  static async analyzeDragons(sector = '') {
    try {
      const response = await apiClient.post('/api/analysis/dragon', { sector });
      return response;
    } catch (error) {
      console.error('龙一龙二分析失败:', error);
      throw error;
    }
  }

  // 机构重仓股分析
  static async analyzeInstitutionalStocks(filters = {}) {
    try {
      const response = await apiClient.post('/api/analysis/institutional', { filters });
      return response;
    } catch (error) {
      console.error('机构重仓股分析失败:', error);
      throw error;
    }
  }

  // 中小票龙头股分析
  static async analyzeSmallCapLeaders(maxMarketCap = 10000000000) {
    try {
      const response = await apiClient.post('/api/analysis/small_cap_leader', { 
        max_market_cap: maxMarketCap 
      });
      return response;
    } catch (error) {
      console.error('中小票龙头股分析失败:', error);
      throw error;
    }
  }

  // 低估股票分析
  static async analyzeUndervaluedStocks(criteria = {}) {
    try {
      const response = await apiClient.post('/api/analysis/undervalued', { criteria });
      return response;
    } catch (error) {
      console.error('低估股票分析失败:', error);
      throw error;
    }
  }

  // AI股票分析
  static async aiStockAnalysis(symbol, type = 'comprehensive') {
    try {
      const response = await apiClient.post(`/api/analysis/${symbol}/ai`, { type });
      return response;
    } catch (error) {
      console.error(`AI分析股票 ${symbol} 失败:`, error);
      throw error;
    }
  }

  // 获取股票综合评分
  static async getComprehensiveScore(symbol) {
    try {
      const response = await apiClient.post('/api/analysis/comprehensive_score', { symbol });
      return response;
    } catch (error) {
      console.error(`获取股票 ${symbol} 综合评分失败:`, error);
      throw error;
    }
  }

  // 获取股票排名
  static async getStockRankings(limit = 20) {
    try {
      const response = await apiClient.post('/api/analysis/stock_ranking', { limit });
      return response;
    } catch (error) {
      console.error('获取股票排名失败:', error);
      throw error;
    }
  }

  // 获取市场趋势分析
  static async analyzeMarketTrend() {
    try {
      const response = await apiClient.get('/api/analysis/market_trend');
      return response;
    } catch (error) {
      console.error('市场趋势分析失败:', error);
      throw error;
    }
  }

  // 自然语言查询
  static async processNaturalLanguageQuery(query, userContext = {}) {
    try {
      const response = await apiClient.post('/api/analysis/natural_language', {
        query,
        user_context: userContext
      });
      return response;
    } catch (error) {
      console.error('自然语言查询失败:', error);
      throw error;
    }
  }

  // 个性化推荐
  static async getPersonalizedRecommendation(userProfile = {}) {
    try {
      const response = await apiClient.post('/api/analysis/personalized_recommendation', {
        user_profile: userProfile
      });
      return response;
    } catch (error) {
      console.error('个性化推荐失败:', error);
      throw error;
    }
  }

  // 情绪分析
  static async performSentimentAnalysis(text) {
    try {
      const response = await apiClient.post('/api/analysis/sentiment_analysis', {
        text
      });
      return response;
    } catch (error) {
      console.error('情绪分析失败:', error);
      throw error;
    }
  }

  // 小票热门股分析
  static async analyzeSmallCapHot(maxMarketCap = 5000000000) {
    try {
      const response = await apiClient.post('/api/analysis/small_cap_hot', { 
        max_market_cap: maxMarketCap 
      });
      return response;
    } catch (error) {
      console.error('小票热门股分析失败:', error);
      throw error;
    }
  }
}

export default ApiService;