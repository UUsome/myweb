<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-links">
        <router-link to="/experts" class="footer-link">专家库</router-link>
        <router-link to="/contact" class="footer-link">联系我们</router-link>
      </div>
      <p class="copyright">&copy; {{ year }} win. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  border-top: 1px solid #E8E2D8;
  background: #F5F0E8;
  margin-top: 40px;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 12px;
}

.footer-link {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #1B2A4A;
}

.copyright {
  color: #888880;
  font-size: 13px;
}
</style>
