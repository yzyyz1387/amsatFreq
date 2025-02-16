const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  devServer: {
    host: '0.0.0.0',
    port: 8091,
    allowedHosts: 'all'
  },

  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = '卫星频率查询 - 常用业余卫星频率查询助手'
      return args
    })
  },

  pwa: {
    name: '卫星频率查询',
    themeColor: '#1a73e8',
    msTileColor: '#1a73e8',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black-translucent',
  }
}) 