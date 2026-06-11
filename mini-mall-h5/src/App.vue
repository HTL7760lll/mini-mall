<template>
  <div id="app-container">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #0d1117;
  color: #c9d1d9;
  -webkit-font-smoothing: antialiased;
}

#app-container {
  min-height: 100vh;
  background: #0d1117;
}
</style>
