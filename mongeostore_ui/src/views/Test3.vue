<template>
  <div class="custom-tree-container">
    <div class="block">
      <p>使用 scoped slot</p>
      <el-tree
        :data="data"
        show-checkbox
        node-key="id"
        default-expand-all
        :expand-on-click-node="false"
        @node-click="handleNodeClick"
      >
        <span
          class="custom-tree-node"
          slot-scope="{ node, data }"
          @mouseenter="mouseenter(data)"
          @mouseleave="mouseleave(data)"
        >
          <span>{{ node.label }}</span>
          <span>
            <el-button
              type="text"
              size="mini"
              v-show="data.del"
              v-if="data.isEdit"
              @click="() => append(data)"
            >
              <i class="el-icon-plus"></i>
            </el-button>
            <el-button
              type="text"
              size="mini"
              v-show="data.del"
              v-else-if="!data.isEdit"
              @click="() => remove(node, data)"
            >
              <i class="el-icon-delete"></i>
            </el-button>
            <el-button
              size="mini"
              type="text"
              v-show="data.del"
              @click="() => rename(node, data)"
            >
              <i class="el-icon-edit-outline"></i>
            </el-button>
          </span>
        </span>
      </el-tree>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
let id = 1000;

export default {
  name: "Test3",
  data() {
    const data = [
      {
        id: 1,
        label: "一级 1",
        children: [
          {
            id: 4,
            label: "二级 1-1",
            children: [
              {
                id: 9,
                label: "三级 1-1-1",
              },
              {
                id: 10,
                label: "三级 1-1-2",
              },
            ],
          },
        ],
      },
      {
        id: 2,
        label: "一级 2",
        children: [
          {
            id: 5,
            label: "二级 2-1",
          },
          {
            id: 6,
            label: "二级 2-2",
          },
        ],
      },
      {
        id: 3,
        label: "一级 3",
        children: [
          {
            id: 7,
            label: "二级 3-1",
          },
          {
            id: 8,
            label: "二级 3-2",
          },
        ],
      },
    ];
    return {
      data: JSON.parse(JSON.stringify(data)),
      // data: JSON.parse(JSON.stringify(data)),
    };
  },
  created() {
    this.showDataBase();
  },

  methods: {
    // 读取数据库信息，返回前端页面展示
    showDataBase() {
      let url = "http://127.0.0.1:8000/load/showdatabase/";
      var temp_list = [];
      axios
        .get(url, {})
        .then((res) => {
          this.data = res.data;
        })
        .catch();
    },

    append(data) {
      let collections = [];
      for (let i = 0; i < data.children.length; i++) {
        const col_data = data.children[i];
        const collection = col_data["label"];
        // console.log(collection);
        collections.push(collection);
      }

      let temp = new Set(collections);
      this.$prompt("请输入中文名称", "添加数据（请勿重名）", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[\u4e00-\u9fa5]{1,}$/, //匹配全中文
        inputErrorMessage: "请输入中文", //不符合正则匹配的提示语句
      })
        .then(({ value }) => {
          //判断是否存在
          if (!temp.has(value)) {
            // 后端数据添加
            const newChild = {
              id: id++,
              label: value,
              isEdit: false,
              _database: data.label,
            };
            data.children.push(newChild);
            console.log(data);
            let url = "http://127.0.0.1:8000/load/addcollection/";
            axios
              .post(url, { newChild })
              .then((res) => {
                this.$message({
                  type: "success",
                  message: "添加成功",
                });
              })
              .catch(() => {
                this.$message({
                  type: "info",
                  message: "添加失败",
                });
              });
          } else {
            this.$message({
              type: "info",
              message: "已存在，请重新输入！",
            });
          }
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消添加",
          });
        });
    },

    rename(node, data) {
      let url = "http://127.0.0.1:8000/load/editdatabasename/";
      this.$prompt("请输入新的名称", "重命名", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[\u4e00-\u9fa5]{1,}$/, //匹配全中文
        inputErrorMessage: "请输入中文", //不符合正则匹配的提示语句
      })
        .then(({ value }) => {
          //可以在这里发请求，http是我模拟的一个虚假的封装好的axios请求,()可写请求参数
          axios
            .post(url, { value, data })
            .then((data) => {
              this.$message({
                type: "success",
                message: "修改成功",
              });
              //请求成功需局部刷新该节点，调用方法,把节点信息node传入
              this.showDataBase();
            })
            //请求失败
            .catch(() => {
              this.$message({
                type: "info",
                message: "修改失败",
              });
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消修改",
          });
        });
    },

    remove(node, data) {
      this.$confirm("永久删除，是否继续？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          // 前端页面删除
          const parent = node.parent;
          const children = parent.data.children || parent.data;
          const index = children.findIndex((d) => d.id === data.id);
          children.splice(index, 1);
          // 后端数据删除
          let url = "http://127.0.0.1:8000/load/deletecollection/";
          axios
            .post(url, { data })
            .then((res) => {
              this.$message({
                type: "success",
                message: "删除成功",
              });
            })
            .catch(() => {
              //请求失败
              this.$message({
                type: "info",
                message: "删除失败",
              });
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },
    mouseenter(data) {
      this.$set(data, "del", true);
    },
    mouseleave(data) {
      this.$set(data, "del", false);
    },
    handleNodeClick(data) {
      console.log(data);
    },
  },
};
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>