<template>
  <div class="login-page">
    <van-nav-bar title="登录" left-text="返回" left-arrow @click-left="router.back" />

    <div class="form-wrap">
      <div class="logo">Mini Mall</div>

      <van-field v-model="form.username" label="用户名" placeholder="请输入用户名" clearable />
      <van-field v-model="form.password" label="密码" type="password" placeholder="请输入密码" />

      <div class="btn-wrap">
        <van-button type="danger" round block size="large" :loading="loading" @click="handleLogin">
          登 录
        </van-button>
      </div>

      <div class="link-wrap">
        还没有账号？<span class="link" @click="router.push('/register')">立即注册</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import request from '../../api/request'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    showToast('请填写完整信息')
    return
  }
  loading.value = true
  try {
    const data = await request.post('/member/login/', {
      username: form.username,
      password: form.password,
    })
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data))
    showToast('登录成功')
    router.replace('/')
  } catch (e) {
    console.error('登录失败:', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; background: #f5f5f5; }
.form-wrap { padding: 40px 24px; }
.logo { text-align: center; font-size: 28px; font-weight: 800; color: #ee0a24; margin-bottom: 32px; }
.btn-wrap { margin-top: 24px; }
.link-wrap { text-align: center; margin-top: 20px; font-size: 14px; color: #999; }
.link { color: #1989fa; cursor: pointer; }
</style>
