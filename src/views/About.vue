<template>
  <div class="about-container">
    <h1>关于本站</h1>
    <div class="content">
      <p>本站提供业余卫星频率查询服务，方便业余无线电爱好者查询各类卫星的频率信息。</p>
      <h2>数据来源</h2>
      <p>本站数据由社区贡献，定期更新。感谢所有为数据更新做出贡献的朋友们。</p>
      <h2>联系方式</h2>
      <p>如果您发现数据有误或需要补充，欢迎联系我们进行更新。</p>
      <div class="button-group">
        <el-button 
          type="primary" 
          @click="openGitHub"
        >
          访问仓库
        </el-button>
        <el-button 
          type="primary" 
          @click="$router.push('/')"
        >
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  methods: {
    openGitHub() {
      window.open('https://github.com/yzyyz1387/amsatFreq', '_blank')
    }
  }
}
</script>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
}

h1 {
  color: #409EFF;
  text-align: center;
  margin-bottom: 30px;
}

h2 {
  color: #666;
  margin: 20px 0 10px;
}

p {
  margin: 10px 0;
  color: #606266;
}

.button-group {
  margin-top: 30px;
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style> 