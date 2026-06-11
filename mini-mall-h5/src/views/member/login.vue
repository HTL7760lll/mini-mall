<template>
  <div class="login-dark">
    <div class="login-card">
      <div class="login-logo">
        <span class="l-m">M</span><span class="l-i">i</span><span class="l-n">n</span><span class="l-i2">i</span>
        <span class="l-m2">M</span><span class="l-a">a</span><span class="l-ll">ll</span>
      </div>
      <div class="login-title">用户登录</div>

      <input class="field" v-model="form.username" placeholder="USERNAME" />
      <input class="field" v-model="form.password" type="password" placeholder="PASSWORD" />

      <button class="submit-btn" :disabled="loading" @click="handleLogin">
        {{ loading ? '...' : '登 录' }}
      </button>

      <div class="link-text">
        还没有账号？<span class="link" @click="router.push('/register')">REGISTER</span>
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
  if (!form.username || !form.password) { showToast('请填写完整信息'); return }
  loading.value = true
  try {
    const data = await request.post('/member/login/', { username: form.username, password: form.password })
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data))
    showToast('登录成功')
    router.replace('/')
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}
</script>

<style scoped>
.login-dark { min-height:100vh; background:#0d1117; display:flex; align-items:center; justify-content:center; }
.login-card { width: 320px; padding: 40px 32px; }

.login-logo { text-align:center; font-size:28px; font-weight:800; letter-spacing:-1px; margin-bottom: 4px; }
.l-m{color:#ff6b35}.l-i,.l-i2{color:#00d4ff}.l-n{color:#ffd700}
.l-m2{color:#4caf50}.l-a{color:#2196f3}.l-ll{color:#9c27b0}

.login-title { text-align:center; font-size:13px; color:#484f58; margin-bottom: 32px; letter-spacing:4px; }

.field {
  width:100%; padding: 10px 0; margin-bottom: 16px;
  background:none; border:none; border-bottom:1px solid #21262d;
  outline:none; color:#c9d1d9; font-size:14px;
}
.field::placeholder { color:#30363d; letter-spacing:2px; }
.field:focus { border-bottom-color:#ff6b35; }

.submit-btn {
  width:100%; margin-top:12px; padding:10px 0;
  background:#ff6b35; color:#0d1117; border:none; font-size:15px; font-weight:700;
  cursor:pointer; transition:opacity .15s;
}
.submit-btn:hover { opacity:.9; }
.submit-btn:disabled { opacity:.5; }

.link-text { text-align:center; margin-top:20px; font-size:12px; color:#484f58; }
.link { color:#00d4ff; cursor:pointer; }
</style>
