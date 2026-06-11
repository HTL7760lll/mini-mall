<template>
  <div class="login-page">
    <div class="login-box">
      <div class="logo">
        <span class="c-o">M</span><span class="c-c">i</span><span class="c-y">n</span><span class="c-c">i</span>
        <span class="c-g">M</span><span class="c-b">a</span><span class="c-p">ll</span>
      </div>
      <div class="title">SIGN IN</div>
      <div class="subtitle">登录您的账号</div>

      <div class="field-wrap">
        <label class="field-label">EMAIL</label>
        <input v-model="form.email" type="email" class="field" placeholder="your@email.com" />
      </div>
      <div class="field-wrap">
        <label class="field-label">PASSWORD</label>
        <input v-model="form.password" type="password" class="field" placeholder="········" @keyup.enter="handleLogin" />
      </div>

      <button class="btn-login" :disabled="loading" @click="handleLogin">
        {{ loading ? 'SIGNING IN...' : 'SIGN IN' }}
      </button>

      <div class="link-row">
        <span class="link" @click="router.push('/register')">CREATE ACCOUNT</span>
        <span class="link" @click="router.push('/')">BACK TO HOME</span>
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
const form = reactive({ email: '', password: '' })

const handleLogin = async () => {
  if (!form.email || !form.password) { showToast('请填写邮箱和密码'); return }
  loading.value = true
  try {
    const data = await request.post('/member/login/', form)
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data))
    showToast('登录成功')
    router.replace('/')
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh; background: #1b2838;
  display: flex; align-items: center; justify-content: center;
}
.login-box { width: 340px; padding: 40px 0; }

.logo { text-align: center; font-size: 26px; font-weight: 800; letter-spacing: -1px; margin-bottom: 8px; }
.c-o{color:#eb6f22}.c-c{color:#67c1f5}.c-y{color:#d4b83b}
.c-g{color:#5c7e10}.c-b{color:#2f7798}.c-p{color:#76428a}

.title { text-align: center; font-size: 18px; color: #acb7c3; font-weight: 600; letter-spacing: 2px; margin-top: 16px; }
.subtitle { text-align: center; font-size: 12px; color: #4f6378; margin-top: 4px; margin-bottom: 32px; }

.field-wrap { margin-bottom: 18px; }
.field-label { display: block; font-size: 10px; color: #4f6378; letter-spacing: 2px; margin-bottom: 6px; }
.field {
  width: 100%; padding: 10px 12px;
  background: #16202d; border: 1px solid #1e2f40; border-radius: 3px;
  outline: none; color: #acb7c3; font-size: 14px;
}
.field:focus { border-color: #67c1f5; }
.field::placeholder { color: #2a3a4a; }

.btn-login {
  width: 100%; margin-top: 8px; padding: 12px 0;
  background: linear-gradient(135deg, #67c1f5, #2f7798); border: none;
  color: #fff; font-size: 14px; font-weight: 600; letter-spacing: 2px;
  cursor: pointer; border-radius: 3px; transition: opacity .15s;
}
.btn-login:hover { opacity: .9; }
.btn-login:disabled { opacity: .5; cursor: not-allowed; }

.link-row { display: flex; justify-content: space-between; margin-top: 24px; }
.link { font-size: 11px; color: #4f6378; cursor: pointer; letter-spacing: 1px; }
.link:hover { color: #67c1f5; }
</style>
