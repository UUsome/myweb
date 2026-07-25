<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <p>&copy; {{ year }} MyWeb. All rights reserved.</p>
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
  color: #888880;
  font-size: 13px;
}
</style>
