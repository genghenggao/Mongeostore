<!--
 * @Description: henggao_learning
 * @version: v1.0.0
 * @Author: henggao
 * @Date: 2020-09-28 20:21:57
 * @LastEditors: henggao
 * @LastEditTime: 2022-05-13 11:04:51
-->
<template>
  <div class="fixed-bottom">

    <ul class="nav justify-content-center">
      <li class="nav-item">
        友情链接：
        <a href="https://www.cumtb.edu.cn/">中国矿业大学（北京）</a>
      </li>
      <li class="nav-item">
        <span class="text-muted"> Copyright © 2020.中国矿业大学(北京)</span>
      </li>
      <li class="nav-item">
        <span class="text-muted"> 京公网安备：110402430067号</span>
      </li>
      <li class="nav-item">
        <span class="text-muted"> 学校地址：北京市海淀区学院路丁11号</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Footbar",
  props: {
    msg: String
  }
};
</script>

<style lang="scss" scoped>
.fixed-bottom {
  background: #70624f;

}
</style>