<template>
  <el-container style="min-width: 1100px; overflow: hidden">
    <el-header>
      <h2
        style="
          font-size: 30px;
          padding-top: 10px;
          color: #870000;
          min-width: 1100px;
          overflow: hidden;
          text-align: left;
        "
      >
        <i class="el-icon-caret-right" /> 相关信息上传
      </h2>
    </el-header>
    <el-main style="padding-top: 10px; min-width: 1100px; overflow: hidden">

      <el-row :gutter="20" style="margin: 0">
        <el-col :span="16" :offset="4">
          <el-tabs :tab-position="tabPosition">
            <el-tab-pane label="解释数据上传">
              <SeiInterpretationMetaUpload />
            </el-tab-pane>
            <el-tab-pane label="项目信息上传">
            </el-tab-pane>
            <el-tab-pane label="单位信息上传">
            </el-tab-pane>
            <el-tab-pane label="其他信息上传">其他信息上传</el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";
import SeiInterpretationMetaUpload from "@/components/seismic/SeiInterpretationMetaUpload.vue";
export default {
  name: "SeiInterpretationUpload",
  components: {
    SeiInterpretationMetaUpload,
  },
  data() {
    return {
      tabPosition: "right", //标签页位置设置
    };
  },
  created() {},
  methods: {},
};
</script>

<style  lang='scss' scoped>
.myTable {
  border-collapse: collapse;
  margin: 0 auto;
  text-align: center;
}

.myTable td,
.myTable th {
  border: 1px solid #cad9ea;
  color: #666;
  height: 60px;
  width: 450px;
  padding-top: 20px; //设置文字居中
}
.el-scrollbar__wrap {
  overflow-x: hidden; //设置滚动条隐藏
}
</style>