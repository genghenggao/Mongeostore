<template>
  <div class="DataShow">
    <el-container>
      <el-header class="data_search">
        <!--搜索头 开始-->
        <section id="search-title" style="min-width: 500px">
          <el-form
            :inline="true"
            :model="searchCondition"
            class="demo-form-inline"
            @submit.native.prevent
          >
            <el-form-item label="关键字:">
              <el-input
                v-model="searchCondition.filter_key"
                suffix-icon="el-icon-view"
                placeholder="请输入关键字"
                @keyup.enter.native="onSearchSubmit"
              ></el-input>
            </el-form-item>
            <el-form-item id="submit-item">
              <el-button
                type="info"
                plain
                icon="el-icon-search"
                @click="onSearchSubmit"
                >查询</el-button
              >
            </el-form-item>
            <el-form-item id="submit-reset">
              <el-button
                type="info"
                plain
                icon="el-icon-refresh"
                @click="showData"
                >重置</el-button
              >
            </el-form-item>
            <el-form-item id="addNew-item">
              <el-button
                type="info"
                plain
                icon="el-icon-edit"
                @click="dialogVisible = true"
                >新增</el-button
              >
            </el-form-item>
          </el-form>
        </section>
        <!--搜索头 结束-->
        <!-- <SearchData /> -->
      </el-header>
      <el-main class="data_content">
        <div class="data_table" style="overflow: hidden">
          <!-- 注意里面max-height字段设置高度  tableData放列表数据 -->
          <el-table
            class="tb-edit"
            highlight-current-row
            :data="
              tableData.slice(
                (currentPage - 1) * PageSize,
                currentPage * PageSize
              )
            "
            style="width: 100%"
            max-height="690px"
            @selection-change="handleSelectionChange"
            lazy
          >
            <!-- 选择框设置 -->
            <el-table-column type="selection" width="55"> </el-table-column>
            <!-- 添加_id字段 -->
            <el-table-column label="_id" prop="_id.$oid"> </el-table-column>
            <template v-for="col in cols">
              <!-- 设置排序字段 -->
              <el-table-column
                :key="col._id"
                :prop="col.prop"
                sortable
                :label="col.label"
                align="center"
              >
                <!-- 每一行数据 -->
                <template slot-scope="scope">
                  <div v-if="!scope.row.isEdit">{{ scope.row[col.prop] }}</div>
                  <div v-else>
                    <el-input v-model="scope.row[col.prop]"></el-input>
                  </div>
                </template>
              </el-table-column>
            </template>
            <el-table-column fixed="right" label="操作" width="160">
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  plain
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)"
                  >{{ scope.row.isEdit ? "保存" : "编辑" }}</el-button
                >
                <el-button
                  @click.native.prevent="
                    deleteRow(scope.$index, tableData, scope.row)
                  "
                  type="danger"
                  plain
                  size="mini"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <!-- 分页 -->
        <div class="block" style="overflow: hidden">
          <el-pagination
            small
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="pageSizes"
            :page-size="PageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalCount"
          >
          </el-pagination>
        </div>

        <el-dialog
          title="添加数据"
          :visible.sync="dialogVisible"
          width="30%"
          @close="addDialogClosed"
        >
          <!-- 内容的主体区域 -->
          <!--去掉:rules="addFormRules" -->
          <el-form
            ref="addFormRef"
            :model="add_to_data"
            :rules="addFormRules"
            label-width="100px"
          >
            <template v-for="(item, key) of addForm">
 
              <el-form-item
                v-if="key !== '_id'"
                :label="key"
                :prop="key"
                :key="key"
              >
                <el-input v-model="add_to_data[key]"></el-input>
              </el-form-item>
 
            </template>
          </el-form>
          <!-- 底部区域 -->
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button
              type="primary"
              :disabled="true"
              v-if="!add_button_state"
              @click="addData"
              >确 定</el-button
            >
            <el-button
              type="primary"
              v-else-if="add_button_state"
              @click="addData"
              >确 定</el-button
            >
          </span>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";

export default {
  name: "CommonData",
  components: {
    // SearchData
  },
  data() {
    // 校验添加信息
    let checkKey_word = (rule, value, callback) => {
      // const regZK_num = /^ZK[0-9]{1,6}/;
      const regKey_word = /^[A-Za-z0-9\u4e00-\u9fa5]{3,}$/;
      if (regKey_word.test(value)) {
        // 验证通过，合法
        return callback();
      }
      // 验证不通过，不合法
      callback(new Error("请输入正确的信息"));
    };

    return {
      // cols prop属性值都是作为 tableData的属性
      cols: [
        { label: "节点编号_id", prop: "_id.$oid", nickname: "normal" },
        { label: "名称nickname", prop: "nickname", nickname: "sort" },
        { label: "类型combat", prop: "combat", nickname: "normal" },
        { label: "状态level", prop: "level", nickname: "normal" },
        { label: "坐标rid", prop: "rid", nickname: "normal" },
      ],
      //   表格数据
      tableData: [
        {
          node: "0051",
          name: " 机库顶",
          type: "UWB",
          status: "正常",
          coordinate: "12.21,34.45,34.6",
        },
        {
          node: "0061",
          name: "机库门",
          type: "GPS",
          status: "低电",
          coordinate: "45.41,67.45,78.6",
        },
        {
          node: "0061",
          name: "机库门",
          type: "GPS",
          status: "低电",
          coordinate: "45.41,67.45,78.6",
        },
      ],
      // 筛选字段
      filter_data: [
        { text: "ZK1", value: "ZK1" },
        { text: "ZK2", value: "ZK2" },
        { text: "ZK3", value: "ZK3" },
        { text: "ZK4", value: "ZK4" },
      ],
      // 分页数据，默认第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 400,
      // 个数选择器（可修改）
      pageSizes: [10, 20, 50, 100],
      // 默认每页显示的条数（可修改)
      PageSize: 10,
      // 控制添加用户对话框的显示与隐藏，默认为隐藏
      dialogVisible: false,
      // 添加对象
      addForm: {
        filter_key: "",
        _id: "",
        Depth: "",
        Azimuth: "",
        Inclination: "",
      },
      // 添加数据框的字段,用来判断是否为空，确定按钮
      add_to_data: {
        filter_key: "",
        Depth: "",
        Azimuth: "",
        Inclination: "",
      },
      // 通过add_button_state值判断确定按钮是否激活
      add_button_state: false,
      // // 添加表单的验证规则对象
      addFormRules: {
        filter_key: [
          { required: true, message: "请输入相关信息", trigger: "blur" },
          { min: 3, max: 10, message: "数据格式有误", trigger: "blur" },
          { validator: checkKey_word, trigger: "blur" },
        ],
      },
      // 搜索对象
      searchCondition: {
        filter_key: "",
        Depth: "",
        _id: "",
      },
      // 用于判断是否点击过搜索按钮
      flag: false,
    };
  },
  watch: {
    add_to_data: {
      handler(curval, oldval) {
        // console.log(curval);
        if (curval[0] != "") {
          this.add_button_state = true;
        } else {
          this.add_button_state = false;
        }
      },
      deep: true,
    },
  },
  created() {
    this.showData();
  },
  methods: {
    // 展示数据
    showData() {
      const url = "http://127.0.0.1:8000/load/commonmetashow/";
      axios
        .get(url, {
  
          params: {
            // 设置上传到后端的数据库和集合名称
            dbname: this.$store.state.title_message,
          },
        })
        .then((response) => {

          this.tableData = response.data;

          this.totalCount = this.tableData.length; //分页总数
          //渲染表格,根据值
          this.currentChangePage(this.tableData);
  
          let tmp = this.tableData[0];
          // console.log(tmp);
          var listcol = [];
          for (var key in tmp) {
  
            listcol.push({
              label: key,
              prop: key,
              // Depth: "normal",
            });
          }

          listcol[0].prop = "_id"; //_id是一个对象，取值，使用这个为了取值
          listcol.splice(0, 1); //去掉_id、ZK_num字段,自己在页面添加，为了更好的遍历

          this.cols = listcol;

          this.addForm = tmp;

          let tem_list = [];
          for (let i = 0; i < 55; i++) {
            let ZK = "ZK";
            let ZKX = ZK + i;
            let json_data = { text: ZKX, value: ZKX };
            tem_list.push(json_data);
          }
          this.filter_data = tem_list;
        });
    },

    // 选择框
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    // 排序
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },

    // 点击按钮，添加数据
    addData() {
      const url = "http://127.0.0.1:8000/load/commonadd_data/";
      let tmp_data = this.add_to_data;
      console.log(tmp_data); //这个取得值是undefined，但可以成功发送到后端
      axios
        .post(url, {
          tmp_data,
          // 设置上传到后端的数据库和集合名称
          colname: this.$store.state.title_message,
          dbname: this.$store.state.temp_database,
        })
        .then((res) => {
          console.log("Success");
        });

      // 隐藏添加用户的对话框
      this.dialogVisible = false;
      // 重新获取用户列表数据
      // this.showData();
      //通过flag判断,刷新数据
      if (!this.flag) {
        this.showData();
      } else {
        this.onSearchSubmit();
      }
    },
    // 监听添加用户对话框的关闭事件
    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    },
    // 编辑（修改）按钮
    handleEdit(index, row) {
      // console.log(index, row);
      // 动态设置数据并通过这个数据判断显示方式
      if (row.isEdit) {
        // 点击保存的
        this.$delete(row, "isEdit");

        let json_data = JSON.stringify(row);

        const url = "http://127.0.0.1:8000/load/commoneditdata/";
        axios
          .post(
            url,
            {
              // data: JSON.stringify(row) //data用于post请求
              json_data,
              // 设置上传到后端的数据库和集合名称
              colname: this.$store.state.title_message,
              dbname: this.$store.state.temp_database,
            },
            {
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
            }
            // console.log(postData)
          )
          .then((res) => {
            console.log("编辑成功");
          });
      } else {
        // 点击编辑
        this.$set(row, "isEdit", true);

      }
    },
    // 删除按钮
    deleteRow(index, rows, row) {
      // 添加确认删除框
      this.$confirm("永久删除，是否继续？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          // 删除操作
          rows.splice(index, 1);
          let json_data = JSON.stringify(row);
          console.log(json_data);
          const url = "http://127.0.0.1:8000/load/commondeletedata/";
          axios
            .post(
              url,
              {
                json_data,
                // 设置上传到后端的数据库和集合名称
                colname: this.$store.state.title_message,
                dbname: this.$store.state.temp_database,
              },
              {
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
              }
            )
            .then((res) => {
              console.log("删除成功");
              //通过flag判断,刷新数据
              if (!this.flag) {
                this.showData();
              } else {
                this.onSearchSubmit();
              }
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },
    // 开始搜索
    onSearchSubmit() {
      if (this.searchCondition.filter_key == "") {
        this.$message.warning("查询条件不能为空！");
        return;
      }
      console.log(this.searchCondition.filter_key);
      let filter_key_data = this.searchCondition.filter_key;
      const url = "http://127.0.0.1:8000/load/commonquerydata/";
      axios
        .post(url, {
          filter_key_data,
          // 设置上传到后端的数据库和集合名称
          colname: this.$store.state.title_message,
          dbname: this.$store.state.temp_database,
        })
        .then((response) => {
          if (response.data) {
            this.tableData = response.data; //返回查询的数据
            console.log(response.data);
            // 总共数据
            var count = Object.keys(response.data).length;
            // console.log(count)
            this.totalCount = count;
            let countarr = [];
            for (let i = 0; i < (count % 10) + 1; i++) {
              const tencount = (i + 1) * 10;
              countarr.push(tencount);
            }
            this.pageSizes = countarr; //有个小意外，这个地方设置了，变不会去了
            this.orgCode = 1;
            // 每页显示的条数
            this.PageSize = 10;
            // 显示第几页
          } else {
            // alert("输入有误或数据不存在");
            this.$message.warning("输入有误或数据不存在");
            return;
          }
          //页面初始化数据需要判断是否检索过
          this.flag = true;
        });
    },

    handleDelete(index, row) {
      console.log(index, row);
    },
    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      // 改变每页显示的条数
      this.PageSize = val;

      this.handleCurrentChange(this.currentPage);
    },
    // 监听 pageSize 改变的事件，显示第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      // 改变默认的页数
      this.currentPage = val;

    },
    //组件自带监控当前页码
    currentChangePage(list) {
      let from = (this.currentPage - 1) * this.pageSize;
      let to = this.currentPage * this.pageSize;
      // this.tableData = [];
      for (; from < to; from++) {
        if (list[from]) {
          this.tableData.push(list[from]);
        }
      }
    },
  },
};
</script>

<style>
/* 全局样式 */
</style>
<style lang="scss" scoped>
/* 本地样式 */
// 设置真个数据内容的大小
.DataShow {
  height: 775px;
}
// 设置搜索框的大小
.data_search {
  height: 45px !important;
}
// 设置表格数据大小，表格+分页
.data_content {
  height: 730px !important;
  overflow: auto;
}
// 设置表格数据大小
.data_table {
  height: 690px !important;
  overflow: auto;
}
// 搜索设置
#search-title {
  padding-top: 2px;
  height: 45px;
  float: right;
}
// 设置搜索关键字段字体
.demo-form-inline ::v-deep .el-form-item__label {
  font-size: 18px !important;
  color: rgb(73, 76, 80);
  font-family: "Arial Narrow";
  font-weight: bold;
}
// 设置表格数据滚动条,这里还是留着比较好
</style>