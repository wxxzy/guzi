// frontend/src/utils/api.js

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：可以在这里添加认证token
api.interceptors.request.use(
  (config) => {
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误
api.interceptors.response.use(
  (response) => {
    // 后端返回的code为0表示成功
    if (response.data && response.data.code === 0) {
      return response.data.data
    } else {
      // 统一处理业务错误
      return Promise.reject(new Error(response.data.message || '未知错误'))
    }
  },
  (error) => {
    // 统一处理HTTP错误
    if (error.response) {
      // 服务器返回了错误状态码
      console.error('API Response Error:', error.response.status, error.response.data)
      return Promise.reject(new Error(error.response.data.message || `服务器错误: ${error.response.status}`))
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('API Request Error: No response received', error.request)
      return Promise.reject(new Error('网络错误，请检查您的网络连接。'))
    } else {
      // 其他错误
      console.error('API Error:', error.message)
      return Promise.reject(new Error(error.message || '请求失败'))
    }
  }
)

// --- API 调用函数 ---

export const getSectorLeaders = (industry) => {
  return api.get(`/analysis/sector-leaders`, { params: { industry } })
}

export const getInstitutionalHoldings = () => {
  return api.get(`/analysis/institutional-holdings`)
}

export const getSmallCapLeaders = () => {
  return api.get(`/analysis/small-cap-leaders`)
}

export const getUndervaluedStocks = () => {
  return api.get(`/analysis/undervalued-stocks`)
}

export const getComprehensiveScore = () => {
  return api.get(`/analysis/comprehensive-score`)
}

export const getGeminiResponse = (prompt) => {
  return api.get(`/debug/gemini-generate`, { params: { prompt } })
}

// 可以在这里添加其他API调用函数
export const getAllStocksDebug = () => {
  return api.get('/debug/all-stocks')
}

export const getGeminiGenerateDebug = (prompt) => {
  return api.get('/debug/gemini-generate', { params: { prompt } })
}

export default api
