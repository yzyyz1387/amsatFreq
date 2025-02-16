<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-sections">
        <!-- 相关链接 -->
        <div class="footer-section">
          <h3>相关链接</h3>
          <ul class="link-list">
            <li v-for="(url, name) in relatedLinks" :key="name">
              <a :href="getUrl(url)" target="_blank" rel="noopener">{{ name }}</a>
            </li>
          </ul>
        </div>

        <!-- 友情链接 -->
        <div class="footer-section">
          <h3>友情链接</h3>
          <ul class="link-list">
            <li v-for="(url, name) in friendlyLinks" :key="name">
              <a :href="getUrl(url)" target="_blank" rel="noopener">{{ name }}</a>
            </li>
          </ul>
        </div>

        <!-- 加入我们 -->
        <div class="footer-section">
          <h3>加入我们</h3>
          <div class="qr-code">
            <img src="/qr.png" alt="QQ扫码加入" />
            <p>QQ扫码，了解更多</p>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© {{ copyrightYear }} yzyyz. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AppFooter',
  data() {
    return {
      relatedLinks: {},
      friendlyLinks: {}
    }
  },
  computed: {
    copyrightYear() {
      const currentYear = new Date().getFullYear()
      const startYear = 2025
      return currentYear === startYear 
        ? startYear.toString()
        : `${startYear}-${currentYear}`
    }
  },
  created() {
    this.loadFooterData()
  },
  methods: {
    async loadFooterData() {
      try {
        const response = await axios.get('/satellite_data.json')
        const { additional_content } = response.data
        this.relatedLinks = additional_content['相关链接'] || {}
        this.friendlyLinks = additional_content['友情链接'] || {}
      } catch (error) {
        console.error('加载页脚数据失败:', error)
      }
    },
    getUrl(urlString) {
      // 移除 "- " 前缀并返回URL
      return urlString.replace('- ', '')
    }
  }
}
</script>

<style scoped>
.app-footer {
  margin-top: auto;
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: white;
  padding: 40px 0 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-sections {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.footer-section {
  text-align: left;
}

.footer-section h3 {
  font-size: 1.3em;
  margin-bottom: 20px;
  position: relative;
  font-weight: 500;
  color: white;
}

.footer-section h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -8px;
  width: 30px;
  height: 2px;
  background-color: rgba(255, 255, 255, 0.6);
}

.link-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.link-list li {
  margin-bottom: 12px;
}

.link-list a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
}

.link-list a:hover {
  color: white;
  transform: translateX(5px);
}

.qr-code {
  text-align: left;
  margin-left: 0;
}

.qr-code img {
  width: 150px;
  height: 150px;
  border-radius: 8px;
  margin-bottom: 10px;
  background-color: white;
  padding: 5px;
}

.qr-code p {
  font-size: 0.9em;
  opacity: 0.9;
  margin: 0;
}

.footer-bottom {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  opacity: 0.8;
  font-size: 0.9em;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-sections {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .footer-section,
  .qr-code {
    text-align: center;
  }

  .footer-section h3::after {
    left: 50%;
    transform: translateX(-50%);
  }

  .link-list a:hover {
    transform: none;
  }

  .app-footer {
    padding: 30px 0 15px;
  }
}
</style> 