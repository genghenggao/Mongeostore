
<template>
  <!-- 主界面-->
  <div class="maincontent" style="overflow: hidden">
    <!-- 子导航 -->
    <el-container>
      <el-header class="maincontent_header">
        <el-menu
          router
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
        >
          <el-menu-item index="/mongeostore/remotehome"
            ><i class="el-icon-s-home"></i>
            首页
          </el-menu-item>
 
          <el-menu-item index="/mongeostore/remotemetadata"
            ><i class="el-icon-s-data"></i>元数据
          </el-menu-item>

          <el-menu-item index="/mongeostore/remoteupload"
            ><i class="el-icon-upload"></i>上传数据</el-menu-item
          >
        </el-menu>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import RemoteHome from "@/components/remote_sensing/RemoteHome.vue";
export default {
  name: "RemoteInfo",
  components: {
    RemoteHome,
  },
  data() {
    return {
      activeIndex: "",
    };
  },
  mounted() {
    this.activeIndex = "/mongeostore/remotehome";
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<style lang="scss" scoped>

/* 导航子标题 */
.maincontent_header {
  /* 固定高度 */
  height: 46px !important;
  /* 消除边距 */
  padding: 0;
  // 固定内容
}
/* maincontent子导航 */
.maincontent div#nav-tab {
  height: 46px;
  background-color: #870000;
}
.maincontent div#nav-tab a {
  color: #ac8585;
}
.maincontent .el-menu-item i {
  color: #ac8585;
  font-size: 25px;
  padding-bottom: 6px;
}

.el-menu-demo {
  height: 46px;
  background-color: #870000;
}
.el-menu-demo .el-menu-item {
  font-size: 20px;
  color: #b47777;
}
.el-menu--horizontal > .el-menu-item {
  float: left;
  height: 46px;
  line-height: 46px;
  margin: 0;
}
ul.el-menu-demo.el-menu--horizontal.el-menu {
  border-color: #810000;
}
</style>