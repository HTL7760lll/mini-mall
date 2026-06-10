import axios from 'axios'
import { showToast } from 'vant'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// 请求拦截器 — 自动注入 JWT
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器 — 统一错误处理
request.interceptors.response.use(
  res => {
    const { code, msg, data } = res.data
    if (code === 200) return data
    showToast(msg || '请求失败')
    return Promise.reject(new Error(msg))
  },
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
    }
    showToast('网络异常，请稍后重试')
    return Promise.reject(err)
  }
)

export default request
