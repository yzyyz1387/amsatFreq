<template>
  <div class="changelog-container">
    <div class="header-section">
      <h1>改动日志</h1>
      <p class="subtitle">感谢以下贡献者的支持</p>
    </div>

    <div class="content-section">
      <div class="changelog-list">
        <div v-for="(log, index) in parsedLogs" :key="index" class="log-item">
          <div class="contributor">{{ log.contributor }}</div>
          <ul class="changes-list">
            <li v-for="(change, idx) in log.changes" :key="idx">
              {{ change }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ChangelogView',
  data() {
    return {
      logs: ''
    }
  },
  computed: {
    parsedLogs() {
      if (!this.logs) return []
      return this.logs.split('\n').map(line => {
        const [contributor, ...changes] = line.replace('- ', '').split('[(').map(part => part.replace(')]', ''))
        return {
          contributor,
          changes: changes[0]?.split('、') || []
        }
      })
    }
  },
  async created() {
    try {
      const response = await axios.get('/satellite_data.json')
      this.logs = response.data.additional_content?.信息?.改动日志 || ''
    } catch (error) {
      console.error('加载改动日志失败:', error)
    }
  }
}
</script>

<style scoped>
.changelog-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0;
  background: linear-gradient(120deg, #1a73e8 0%, #34a853 100%);
  border-radius: 16px;
  color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.content-section {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.log-item {
  margin-bottom: 30px;
}

.contributor {
  font-size: 18px;
  font-weight: 500;
  color: #409EFF;
  margin-bottom: 12px;
}

.changes-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.changes-list li {
  color: #606266;
  line-height: 1.8;
  padding-left: 20px;
  position: relative;
  margin-bottom: 8px;
}

.changes-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #409EFF;
}

@media (max-width: 768px) {
  .content-section {
    padding: 20px;
  }

  .contributor {
    font-size: 16px;
  }

  .changes-list li {
    font-size: 14px;
  }
}
</style> 