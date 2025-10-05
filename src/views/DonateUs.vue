
<template>
  <div class="donate-container">
    <h1>支持我们</h1>
    <p>如果您喜欢我们的项目并希望支持我们，您可以通过以下方式进行捐赠：</p>
    <!--    爱发电-->
    <div class="donate-option">
      <a href="https://afdian.com/a/yzyyz" target="_blank" rel="noopener">
        爱发电
      </a>
      <p>通过爱发电平台支持我们，收益将全部用于项目开发。</p>
      <a href="https://afdian.com/a/yzyyz" target="_blank" rel="noopener">
        <img src="/fadian.png" alt="爱发电二维码" class="donate-qr" />
      </a>
    </div>
  </div>
</template>

<style scoped>
.donate-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}
.donate-option {
  margin-top: 20px;
}
.donate-qr {
  width: 200px;
  margin-top: 10px;
}
.donate-option a {
  text-decoration: none;
  color: #007bff;
}
.donate-option a:hover {
  text-decoration: underline;
}

</style>

<script>
export default {
  name: 'DonateUsView',

}
</script>
