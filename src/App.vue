<template>
  <el-config-provider :locale="zhCn" :button-config="buttonConfig">
    <div class="app-container" :class="{ 'dark-theme': isDarkMode }">
      <el-menu
        :router="true"
        mode="horizontal"
        class="nav-menu"
        :default-active="$route.path"
        fixed
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/changelog">改动日志</el-menu-item>
        <el-menu-item index="/about">关于</el-menu-item>

        <!-- 添加右侧按钮组 -->
        <div class="right-menu">
          <el-tooltip
            content="切换主题"
            placement="bottom"
            :show-after="300"
          >
            <div class="menu-icon-btn" @click="toggleDarkMode">
              <el-icon v-if="!isDarkMode"><Moon /></el-icon>
              <el-icon v-else><Sunny /></el-icon>
            </div>
          </el-tooltip>

          <el-tooltip
            content="GitHub 仓库"
            placement="bottom"
            :show-after="300"
          >
            <a
              href="https://github.com/yzyyz1387/amsatFreq"
              target="_blank"
              class="menu-icon-btn github-icon"
            >
              <svg height="20" width="20" viewBox="0 0 16 16" class="github-svg">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
              </svg>
            </a>
          </el-tooltip>
        </div>
      </el-menu>

      <div class="main-content">
        <router-view />
      </div>

      <AppFooter />
    </div>
  </el-config-provider>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElConfigProvider } from 'element-plus'
import { Moon, Sunny } from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import AppFooter from '@/components/AppFooter.vue'

const isDarkMode = ref(false)
const buttonConfig = ref({
  autoInsertSpace: true
})

// 应用主题
const applyTheme = (darkMode) => {
  // 更新 HTML 根元素的 class
  document.documentElement.classList.toggle('dark', darkMode)
  // 更新 Element Plus 的主题
  const html = document.documentElement
  if (darkMode) {
    html.setAttribute('data-theme', 'dark')
    document.body.setAttribute('class', 'el-theme-dark')
  } else {
    html.removeAttribute('data-theme')
    document.body.removeAttribute('class')
  }
}

// 切换主题
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
  applyTheme(isDarkMode.value)
}

// 监听系统主题变化
const watchSystemTheme = () => {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const handleChange = (e) => {
    if (!localStorage.getItem('theme')) {
      isDarkMode.value = e.matches
      applyTheme(e.matches)
    }
  }
  mediaQuery.addEventListener('change', handleChange)
}

onMounted(() => {
  // 初始化主题
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark'
  } else {
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  applyTheme(isDarkMode.value)
  watchSystemTheme()
})
</script>

<style>
body {
  margin: 0;
  background-color: #f8f9fa;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.nav-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.main-content {
  flex: 1;
  padding-top: 60px;
  background-color: #f8f9fa;
}

.right-menu {
  position: absolute;
  right: 20px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #606266;
}

.menu-icon-btn:hover {
  background-color: rgba(64, 158, 255, 0.1);
  color: #409EFF;
}

.menu-icon-btn .el-icon {
  font-size: 20px;
}

/* 暗色模式样式 */
.dark-theme .menu-icon-btn {
  color: #dcdfe6;
}

.dark-theme .menu-icon-btn:hover {
  background-color: rgba(64, 158, 255, 0.2);
  color: #409EFF;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .right-menu {
    right: 10px;
    gap: 8px;
  }

  .menu-icon-btn {
    width: 32px;
    height: 32px;
  }

  .menu-icon-btn .el-icon {
    font-size: 18px;
  }
}

/* 暗色主题样式 */
.dark-theme {
  background-color: #1a1a1a !important;
  color: #e0e0e0;
}

.dark-theme .nav-menu {
  background-color: #1e1e1e !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-theme .el-menu--horizontal {
  background-color: #1e1e1e !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-theme .el-menu-item {
  color: #e0e0e0 !important;
}

.dark-theme .el-menu-item.is-active {
  color: #409EFF !important;
  background-color: #2d2d2d !important;
}

.dark-theme .main-content {
  background-color: #1a1a1a;
}

/* 移动端暗色主题适配 */
@media (max-width: 768px) {
  .dark-theme .nav-menu {
    background-color: #1e1e1e !important;
  }
}

/* 全局过渡效果 */
body {
  transition: background-color 0.3s ease;
}

.app-container {
  transition: background-color 0.3s ease;
}

.nav-menu {
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.el-menu-item {
  transition: color 0.3s ease, background-color 0.3s ease;
}

.github-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.github-svg {
  fill: currentColor;
  transition: fill 0.3s ease;
}

/* 暗色主题适配 */
.dark-theme .github-svg {
  fill: #dcdfe6;
}

.dark-theme .github-icon:hover .github-svg {
  fill: #409EFF;
}
</style>