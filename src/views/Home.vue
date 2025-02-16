<template>
  <div class="home-container">
    <div class="header-section">
      <h1>卫星频率查询</h1>
      <p class="subtitle">常用业余卫星频率查询助手</p>
    </div>

    <!-- 在 header-section 下方添加公告栏 -->
    <div v-if="latestAnnouncement" class="announcement-bar">
      <div class="announcement-content">
        <el-icon class="announcement-icon"><Bell /></el-icon>
        <span class="announcement-date">{{ latestAnnouncement.date }}</span>
        <span class="announcement-text">{{ latestAnnouncement.text }}</span>
      </div>
      <el-button 
        v-if="latestAnnouncement.link"
        type="primary" 
        size="small" 
        class="go-button"
        @click="openAnnouncementLink(latestAnnouncement.link)"
      >
        Go
      </el-button>
    </div>

    <div class="search-section">
      <el-input
        v-model="searchQuery"
        placeholder="输入卫星名称搜索..."
        class="search-input"
        @input="handleSearch"
        size="large"
      >
        <template #prefix>
          <el-icon class="search-icon"><Search /></el-icon>
        </template>
      </el-input>
      
      <div class="filter-tags">
        <el-radio-group v-model="statusFilter" size="large">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="favorite">收藏</el-radio-button>
          <el-radio-button label="available">可用</el-radio-button>
          <el-radio-button label="unavailable">不可用</el-radio-button>
          <el-radio-button label="never">未启用</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    
    <div class="satellite-list">
      <!-- PC端表格 -->
      <el-table 
        v-if="!isMobile"
        :data="filteredSatellites" 
        style="width: 100%"
        :header-cell-style="{
          background: '#f5f7fa',
          color: '#606266',
          fontWeight: 'bold'
        }"
      >
        <el-table-column prop="name" label="卫星名称" min-width="180">
          <template #default="{ row }">
            <div class="satellite-name">
              <span class="name-text">{{ row.name }}</span>
              <el-tag 
                :type="getStatusType(row.status)" 
                size="small" 
                effect="light"
                class="status-tag"
              >
                {{ getStatusText(row.status) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="频率信息" min-width="600">
          <template #default="{ row }">
            <el-collapse>
              <el-collapse-item>
                <template #title>
                  <div class="frequency-title">
                    <el-icon><ArrowRight class="collapse-arrow" /></el-icon>
                    <span>频率详情</span>
                    <el-tag 
                      class="frequency-count" 
                      :type="getStatusType(row.status)" 
                      effect="plain" 
                      size="small"
                    >
                      {{ row.frequencies.length }} 个配置
                    </el-tag>
                  </div>
                </template>
                <div class="frequency-content">
                  <el-table 
                    :data="row.frequencies" 
                    border 
                    size="small"
                    class="frequency-table"
                    :header-cell-style="frequencyHeaderStyle"
                  >
                    <el-table-column prop="stage" label="阶段" width="120">
                      <template #default="{ row }">
                        <span class="stage-text">{{ row.stage }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="uplink" label="上行频率" width="140">
                      <template #default="{ row }">
                        <div class="frequency-value">
                          <span>{{ row.uplink }}</span>
                          <span class="unit">MHz</span>
                        </div>
                      </template>
                    </el-table-column>
                    <el-table-column prop="downlink" label="下行频率" width="140">
                      <template #default="{ row }">
                        <div class="frequency-value">
                          <span>{{ row.downlink }}</span>
                          <span class="unit">MHz</span>
                        </div>
                      </template>
                    </el-table-column>
                    <el-table-column prop="tone" label="亚音" width="100">
                      <template #default="{ row }">
                        <el-tag 
                          size="small" 
                          effect="plain" 
                          :type="row.tone ? 'warning' : 'info'"
                        >
                          {{ row.tone || '无' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="shift" label="频差" width="120">
                      <template #default="{ row }">
                        <div class="shift-value" :class="{'negative': row.shift.startsWith('-')}">
                          {{ row.shift }}
                        </div>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-collapse-item>
            </el-collapse>
          </template>
        </el-table-column>
        
        <el-table-column prop="note" label="备注" min-width="150">
          <template #default="{ row }">
            <a 
              v-if="isValidUrl(row.note)" 
              :href="row.note" 
              target="_blank" 
              class="note-link"
            >
              {{ row.note }}
            </a>
            <span v-else class="note">{{ row.note || '-' }}</span>
          </template>
        </el-table-column>

        <el-table-column label="收藏" width="80" align="center">
          <template #default="{ row }">
            <el-icon 
              class="favorite-icon" 
              :class="{ 'is-favorite': isFavorite(row.name) }"
              @click.stop="toggleFavorite(row.name)"
            >
              <Star />
            </el-icon>
          </template>
        </el-table-column>
      </el-table>

      <!-- 移动端卡片列表 -->
      <div v-else class="mobile-satellite-list">
        <div 
          v-for="satellite in filteredSatellites" 
          :key="satellite.name"
          class="satellite-card"
        >
          <div class="card-header">
            <div class="card-title">
              <span class="name-text">{{ satellite.name }}</span>
              <el-tag 
                :type="getStatusType(satellite.status)" 
                size="small" 
                effect="light"
              >
                {{ getStatusText(satellite.status) }}
              </el-tag>
            </div>
            <el-icon 
              class="favorite-icon" 
              :class="{ 'is-favorite': isFavorite(satellite.name) }"
              @click.stop="toggleFavorite(satellite.name)"
            >
              <Star />
            </el-icon>
          </div>

          <div class="card-content">
            <el-collapse>
              <el-collapse-item>
                <template #title>
                  <div class="frequency-title">
                    <el-icon><ArrowRight class="collapse-arrow" /></el-icon>
                    <span>频率配置 ({{ satellite.frequencies.length }})</span>
                  </div>
                </template>
                
                <div class="frequency-table-mobile">
                  <el-table 
                    :data="satellite.frequencies" 
                    border 
                    size="small"
                    :header-cell-style="frequencyHeaderStyle"
                  >
                    <el-table-column prop="stage" label="阶段" width="70" />
                    <el-table-column label="上行" min-width="100">
                      <template #default="{ row }">
                        <span class="freq-value">{{ row.uplink }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column label="下行" min-width="100">
                      <template #default="{ row }">
                        <span class="freq-value">{{ row.downlink }}</span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="tone" label="亚音" width="70">
                      <template #default="{ row }">
                        {{ row.tone || '-' }}
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>

          <div class="card-footer" v-if="satellite.note">
            <div class="note-label">备注：</div>
            <template v-if="isValidUrl(satellite.note)">
              <a :href="satellite.note" target="_blank" class="note-link">
                {{ satellite.note }}
              </a>
            </template>
            <template v-else>
              <span class="note">{{ satellite.note }}</span>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 在 home-container 最后添加返回顶部按钮 -->
    <el-backtop 
      :right="20" 
      :bottom="20"
      :visibility-height="300"
      class="back-to-top"
    >
      <el-icon><ArrowUpBold /></el-icon>
    </el-backtop>
  </div>
</template>

<script>
import { Search, ArrowRight, Star, Bell, ArrowUpBold } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'HomeView',
  components: {
    Search,
    ArrowRight,
    Star,
    Bell,
    ArrowUpBold
  },
  data() {
    return {
      searchQuery: '',
      satellites: [],
      statusFilter: 'all',
      favorites: JSON.parse(localStorage.getItem('favorites') || '[]'),
      isMobile: false,
      announcements: []
    }
  },
  computed: {
    filteredSatellites() {
      let satellites = this.satellites;
      
      // 先按状态和收藏筛选
      if (this.statusFilter === 'favorite') {
        satellites = satellites.filter(satellite => 
          this.favorites.includes(satellite.name)
        );
      } else if (this.statusFilter !== 'all') {
        satellites = satellites.filter(satellite => 
          satellite.status === this.statusFilter
        );
      }
      
      // 再按搜索关键词筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        satellites = satellites.filter(satellite => 
          satellite.name.toLowerCase().includes(query)
        );
      }
      
      return satellites.sort((a, b) => {
        const statusPriority = {
          'available': 1,
          'unavailable': 2,
          'never': 3
        };
        return statusPriority[a.status] - statusPriority[b.status];
      });
    },
    latestAnnouncement() {
      const activeAnnouncements = this.announcements
        .filter(a => a.active)
        .sort((a, b) => new Date(b.date) - new Date(a.date))
      return activeAnnouncements[0] || null
    }
  },
  created() {
    this.loadSatelliteData()
    this.checkMobile()
    window.addEventListener('resize', this.checkMobile)
  },
  unmounted() {
    window.removeEventListener('resize', this.checkMobile)
  },
  methods: {
    async loadSatelliteData() {
      try {
        const response = await axios.get('/satellite_data.json')
        this.satellites = response.data.satellites

        // 处理公告数据
        const announcements = Object.entries(response.data.additional_content?.公告 || {}).map(([text, info]) => {
          const [date, link, active] = info.split('\n').map(i => i.replace('- ', ''))
          return {
            text,
            date,
            link,
            active: active === 'True'
          }
        })
        this.announcements = announcements
      } catch (error) {
        console.error('加载数据失败:', error)
      }
    },
    handleSearch() {
      // 搜索逻辑已经在 computed 属性中实现
    },
    getStatusText(status) {
      const statusMap = {
        'available': '可用',
        'unavailable': '不可用',
        'never': '未启用'
      }
      return statusMap[status] || status
    },
    getStatusType(status) {
      const typeMap = {
        'available': 'success',
        'unavailable': 'danger',
        'never': 'info'
      }
      return typeMap[status] || 'info'
    },
    frequencyHeaderStyle() {
      return {
        background: '#f5f7fa',
        color: '#606266',
        fontWeight: '600',
        borderBottom: '2px solid #ebeef5'
      }
    },
    isFavorite(satelliteName) {
      return this.favorites.includes(satelliteName)
    },
    toggleFavorite(satelliteName) {
      const index = this.favorites.indexOf(satelliteName)
      if (index === -1) {
        this.favorites.push(satelliteName)
      } else {
        this.favorites.splice(index, 1)
      }
      localStorage.setItem('favorites', JSON.stringify(this.favorites))
    },
    isValidUrl(str) {
      if (!str) return false
      try {
        new URL(str)
        return true
      } catch {
        return false
      }
    },
    checkMobile() {
      this.isMobile = window.innerWidth <= 768
    },
    openAnnouncementLink(link) {
      if (this.isValidUrl(link)) {
        window.open(link, '_blank')
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 160px);
}

.header-section {
  text-align: center;
  margin-bottom: 0;
  padding: 40px 0;
  background: linear-gradient(120deg, #1a73e8 0%, #34a853 100%);
  border-radius: 16px 16px 0 0;
  color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(120deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  transform: translateX(-100%);
  animation: shine 3s infinite;
}

@keyframes shine {
  100% {
    transform: translateX(100%);
  }
}

h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  font-weight: 600;
}

.subtitle {
  font-size: 1.1em;
  opacity: 0.9;
}

.search-section {
  position: sticky;
  top: 60px;
  z-index: 99;
  margin: 30px 0;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.search-input {
  width: 600px;
  max-width: 100%;
}

:deep(.el-input__wrapper) {
  padding: 4px 15px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409EFF !important;
}

.search-icon {
  font-size: 18px;
  color: #909399;
  margin-right: 8px;
}

.filter-tags {
  margin-top: 10px;
}

:deep(.el-radio-button__inner) {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
}

:deep(.el-tag) {
  margin: 0;
  border: none;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  box-shadow: none;
}

@media (max-width: 768px) {
  .home-container {
    padding: 0;
  }

  .header-section {
    margin: 0;
    border-radius: 0;
    padding: 30px 0;
  }

  .announcement-bar {
    margin: 0;
    border-radius: 0;
    background: rgba(26, 115, 232, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .announcement-content {
    gap: 8px;
  }

  .announcement-date {
    font-size: 12px;
  }

  .announcement-text {
    font-size: 13px;
  }

  .go-button {
    padding: 3px 10px;
    margin-left: 8px;
  }

  .search-section {
    margin: 10px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    gap: 10px;
  }

  .search-input {
    width: 100%;
  }

  :deep(.el-input__wrapper) {
    padding: 2px 12px;
  }

  :deep(.el-input__inner) {
    font-size: 14px;
    height: 36px;
  }

  .search-icon {
    font-size: 16px;
  }

  .filter-tags {
    margin-top: 5px;
  }

  :deep(.el-radio-button__inner) {
    height: 32px;
    padding: 0 12px;
    font-size: 13px;
  }

  :deep(.el-radio-group) {
    white-space: nowrap;
    overflow-x: auto;
    padding-bottom: 5px;
    -webkit-overflow-scrolling: touch;
  }

  .mobile-satellite-list {
    margin-top: 8px;
    gap: 8px;
    padding: 8px;
  }

  .satellite-card {
    margin: 0;
    border-radius: 8px;
  }

  .card-header {
    padding: 8px 12px;
  }

  .name-text {
    font-size: 15px;
  }

  .frequency-table-mobile {
    padding: 8px;
  }

  :deep(.el-table--small) {
    font-size: 13px;
  }

  :deep(.el-table .cell) {
    padding: 4px;
  }

  .freq-value {
    padding: 2px 6px;
    font-size: 13px;
  }

  :deep(.el-collapse-item__header) {
    height: 40px;
    padding: 0 12px;
  }

  .frequency-title {
    gap: 8px;
    font-size: 14px;
  }

  .card-footer {
    padding: 8px 12px;
    font-size: 12px;
  }

  .note-label {
    margin-bottom: 2px;
  }

  .favorite-icon {
    font-size: 18px;
    padding: 6px;
  }
}

@media (prefers-color-scheme: dark) and (max-width: 768px) {
  .announcement-bar {
    background: rgba(26, 115, 232, 0.9);
  }

  .search-section {
    background: rgba(30, 30, 30, 0.95);
  }
}

.satellite-name {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}

.name-text {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.favorite-icon {
  cursor: pointer;
  font-size: 20px;
  padding: 8px;
  margin: 0 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.favorite-icon:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: scale(1.1);
}

.favorite-icon.is-favorite {
  color: #f1c40f;
  animation: favorite-pop 0.3s ease;
}

@keyframes favorite-pop {
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.status-tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.frequency-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #409EFF;
  font-weight: 500;
}

.collapse-arrow {
  transition: transform 0.3s;
}

:deep(.el-collapse-item.is-active .collapse-arrow) {
  transform: rotate(90deg);
}

.frequency-count {
  padding: 2px 8px;
  font-size: 12px;
}

.frequency-content {
  padding: 16px;
}

:deep(.el-collapse-item__header) {
  height: 48px;
  padding: 0 16px;
  margin: 4px 0;
  background: #f8f9fa;
  border-radius: 6px;
}

:deep(.el-collapse-item__header:hover) {
  background: #ecf5ff;
  border-color: #409EFF;
}

:deep(.el-collapse-item.is-active .el-collapse-item__header) {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.frequency-table {
  margin: 8px 0;
}

.stage-text {
  color: #606266;
  font-weight: 500;
}

.frequency-value {
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: 'Monaco', 'Menlo', monospace;
  color: #409EFF;
  font-weight: 500;
  font-size: 15px;
}

.unit {
  color: #909399;
  font-size: 13px;
  font-weight: normal;
}

.shift-value {
  font-family: 'Monaco', 'Menlo', monospace;
  color: #67C23A;
  font-weight: 500;
  font-size: 15px;
}

.shift-value.negative {
  color: #F56C6C;
}

:deep(.el-table--small .el-table__cell) {
  padding: 10px 0;
}

:deep(.el-collapse-item__content) {
  padding: 0;
  background: #fff;
  border: 1px solid #ebeef5;
  border-top: none;
  border-bottom-left-radius: 6px;
  border-bottom-right-radius: 6px;
}

/* 添加动画效果 */
:deep(.el-collapse-item__wrap) {
  transition: all 0.3s ease-out;
}

:deep(.el-collapse-item__content) {
  transition: all 0.3s ease-out;
}

.note {
  padding: 4px 0;
  font-size: 13px;
  line-height: 1.5;
}

.note-link {
  color: #409EFF;
  text-decoration: none;
}

.note-link:hover {
  text-decoration: underline;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  margin-top: 20px;
  background-color: #ffffff;
}

:deep(.el-table:hover) {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

:deep(.el-table th.el-table__cell) {
  padding: 12px 0;
  background: linear-gradient(to right, #f5f7fa, #ffffff) !important;
}

/* 添加平滑滚动效果 */
html {
  scroll-behavior: smooth;
}

/* 添加暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .header-section {
    background: linear-gradient(120deg, #1a73e8 0%, #188038 100%);
  }

  .search-section {
    background: rgba(30, 30, 30, 0.9);
  }

  .satellite-card {
    background: #1e1e1e;
    border-color: rgba(255, 255, 255, 0.1);
  }

  .card-header {
    background: linear-gradient(to right, #2d2d2d, #1e1e1e);
  }

  .freq-value {
    background: #1a1a1a;
    color: #4285f4;
  }

  :deep(.el-table) {
    background-color: #1e1e1e;
    color: #ffffff;
  }

  :deep(.el-table th.el-table__cell) {
    background: linear-gradient(to right, #2d2d2d, #1e1e1e) !important;
  }

  .name-text {
    color: #e0e0e0;
  }
}

/* 移动端卡片样式 */
.mobile-satellite-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 10px;
}

.satellite-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.satellite-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(to right, #f8f9fa, #ffffff);
  border-bottom: 1px solid #ebeef5;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-content {
  padding: 0;
}

.frequency-table-mobile {
  padding: 10px;
}

.freq-values,
.freq-item,
.freq-label {
  display: none;
}

.freq-value {
  font-family: 'JetBrains Mono', 'Monaco', monospace;
  background: #f0f7ff;
  padding: 4px 8px;
  border-radius: 4px;
  color: #1a73e8;
  font-size: 14px;
  font-weight: 500;
}

.card-footer {
  padding: 12px 16px;
  border-top: 1px solid #ebeef5;
  font-size: 13px;
}

.note-label {
  color: #606266;
  font-weight: 500;
  margin-bottom: 4px;
}

.note, .note-link {
  color: #606266;
  word-break: break-all;
  padding-left: 4px;
}

.note-link {
  color: #409EFF;
}

@media (max-width: 768px) {
  .header-section {
    margin: 0;
    border-radius: 0;
    padding: 30px 0;
  }

  .announcement-bar {
    margin: 0;
    border-radius: 0;
    background: rgba(26, 115, 232, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .announcement-content {
    gap: 8px;
  }

  .announcement-date {
    font-size: 12px;
  }

  .announcement-text {
    font-size: 13px;
  }

  .go-button {
    padding: 3px 10px;
    margin-left: 8px;
  }

  .search-section {
    margin: 10px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    gap: 10px;
  }

  .search-input {
    width: 100%;
  }

  :deep(.el-input__wrapper) {
    padding: 2px 12px;
  }

  :deep(.el-input__inner) {
    font-size: 14px;
    height: 36px;
  }

  .search-icon {
    font-size: 16px;
  }

  .filter-tags {
    margin-top: 5px;
  }

  :deep(.el-radio-button__inner) {
    height: 32px;
    padding: 0 12px;
    font-size: 13px;
  }

  :deep(.el-radio-group) {
    white-space: nowrap;
    overflow-x: auto;
    padding-bottom: 5px;
    -webkit-overflow-scrolling: touch;
  }

  .mobile-satellite-list {
    margin-top: 10px;
  }

  .satellite-card {
    margin: 0 10px 10px;
    border-radius: 12px;
  }

  :deep(.el-table .cell) {
    padding: 6px;
  }

  .freq-value {
    padding: 3px 8px;
  }
}

@media (prefers-color-scheme: dark) and (max-width: 768px) {
  .announcement-bar {
    background: rgba(26, 115, 232, 0.9);
  }

  .search-section {
    background: rgba(30, 30, 30, 0.95);
  }
}

.announcement-bar {
  background: linear-gradient(120deg, #1a73e8 0%, #34a853 100%);
  padding: 8px 20px;
  margin: 0 auto 20px;
  border-radius: 0 0 16px 16px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.announcement-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.announcement-icon {
  font-size: 16px;
}

.announcement-date {
  opacity: 0.8;
  font-size: 13px;
  white-space: nowrap;
}

.announcement-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.go-button {
  margin-left: 16px;
  padding: 4px 12px;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
}

.go-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 返回顶部按钮样式 */
:deep(.el-backtop) {
  background: linear-gradient(120deg, #1a73e8 0%, #34a853 100%);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

:deep(.el-backtop:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  background: linear-gradient(120deg, #1a73e8 0%, #34a853 100%);
}

:deep(.el-backtop .el-icon) {
  font-size: 20px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  :deep(.el-backtop) {
    width: 36px;
    height: 36px;
  }

  :deep(.el-backtop .el-icon) {
    font-size: 18px;
  }
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
  :deep(.el-backtop),
  :deep(.el-backtop:hover) {
    background: linear-gradient(120deg, #1a73e8 0%, #188038 100%);
  }
}
</style> 