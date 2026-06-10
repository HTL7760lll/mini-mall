<template>
  <div class="register-page">
    <van-nav-bar title="注册" left-text="返回" left-arrow @click-left="router.back" />

    <div class="form-wrap">
      <div class="logo">创建账号</div>

      <van-field v-model="form.username" label="用户名" placeholder="3-20位字母或数字" clearable />
      <van-field v-model="form.password" label="密码" type="password" placeholder="6-20位密码" />
      <van-field v-model="form.nickname" label="昵称" placeholder="选填" clearable />

      <div class="btn-wrap">
        <van-button type="danger" round block size="large" :loading="loading" @click="handleRegister">
          注 册
        </van-button>
      </div>

      <div class="link-wrap">
        已有账号？<span class="link" @click="router.push('/login')">立即登录</span>
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
const form = reactive({ username: '', password: '', nickname: '' })

const handleRegister = async () => {
  if (!form.username || !form.password) {
    showToast('用户名和密码不能为空')
    return
  }
  if (form.username.length < 3) { showToast('用户名至少3位'); return }
  if (form.password.length < 6) { showToast('密码至少6位'); return }

  loading.value = true
  try {
    const data = await request.post('/member/register/', {
      username: form.username,
      password: form.password,
      nickname: form.nickname || form.username,
    })
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data))
    showToast('注册成功')
    router.replace('/')
  } catch (e) {
    console.error('注册失败:', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page { min-height: 100vh; background: #f5f5f5; }
.form-wrap { padding: 40px 24px; }
.logo { text-align: center; font-size: 24px; font-weight: 700; color: #333; margin-bottom: 32px; }
.btn-wrap { margin-top: 24px; }
.link-wrap { text-align: center; margin-top: 20px; font-size: 14px; color: #999; }
.link { color: #1989fa; cursor: pointer; }
</style>
