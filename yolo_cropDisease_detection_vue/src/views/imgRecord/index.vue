<template>
	<div class="system-role-container layout-padding">
		<div class="system-role-padding layout-padding-auto layout-padding-view">
			<div class="system-user-search mb15">
				<el-input v-model="state.tableData.param.search1" size="default" placeholder="请输入农作物类型"
					style="max-width: 180px"> </el-input>
				<el-input v-model="state.tableData.param.search2" size="default" placeholder="请输入识别结果"
					style="max-width: 180px; margin-left: 15px">
				</el-input>
				<el-button size="default" type="primary" class="ml10" @click="getTableData()">
					<el-icon>
						<ele-Search />
					</el-icon>
					查询
				</el-button>
			</div>
			<el-table :data="state.tableData.data" style="width: 100%">
				<el-table-column type="expand">
					<template #default="props">
						<div m="4">
							<p style="margin-left: 20px; font-size: 16px; font-weight: 800;">详细识别结果：</p>
							<el-table :data="props.row.family">
								<el-table-column prop="label" label="识别结果" align="center" />
								<el-table-column prop="confidence" label="置信度" show-overflow-tooltip
									align="center"></el-table-column>
								<el-table-column prop="startTime" label="识别时间" align="center" />
							</el-table>
						</div>
					</template>
				</el-table-column>
				<el-table-column prop="num" label="序号" width="80" align="center" />
				<el-table-column prop="inputImg" label="原始图片" width="120" align="center">
					<template #default="scope">
						<img :src="scope.row.inputImg" width="120" height="80" />
					</template>
				</el-table-column>
				<el-table-column prop="outImg" label="预测图片" width="120" align="center">
					<template #default="scope">
						<img :src="scope.row.outImg" width="120" height="80" />
					</template>
				</el-table-column>
				<el-table-column prop="weight" label="识别权重" show-overflow-tooltip align="center"></el-table-column>
				<el-table-column prop="conf" label="最小阈值" show-overflow-tooltip align="center"></el-table-column>
				<el-table-column prop="allTime" label="总用时" show-overflow-tooltip align="center"></el-table-column>
				<el-table-column prop="startTime" label="识别时间" width="200" align="center" />
				<el-table-column prop="username" label="识别用户" show-overflow-tooltip align="center"></el-table-column>
				<el-table-column label="操作" width="80">
					<template #default="scope">
						<el-button size="small" text type="primary" @click="onRowDel(scope.row)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
			<el-pagination @size-change="onHandleSizeChange" @current-change="onHandleCurrentChange" class="mt15"
				:pager-count="5" :page-sizes="[10, 20, 30]" v-model:current-page="state.tableData.param.pageNum"
				background v-model:page-size="state.tableData.param.pageSize"
				layout="total, sizes, prev, pager, next, jumper" :total="state.tableData.total">
			</el-pagination>
		</div>
	</div>
</template>

<script setup lang="ts" name="systemRole">
import { defineAsyncComponent, reactive, onMounted, ref } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import request from '/@/utils/request';
import { useUserInfo } from '/@/stores/userInfo';
import { storeToRefs } from 'pinia';

const stores = useUserInfo();
const { userInfos } = storeToRefs(stores);

const state = reactive({
	tableData: {
		data: [] as any,
		total: 0,
		loading: false,
		param: {
			search: '',
			search1: '',
			search2: '',
			pageNum: 1,
			pageSize: 10,
		},
	},
});

const getTableData = () => {
	state.tableData.loading = true;
	if (userInfos.value.userName != 'admin') {
		state.tableData.param.search = userInfos.value.userName;
	}
	request
		.get('/api/imgRecords', {
			params: state.tableData.param,
		})
		.then((res) => {
			if (res.code == 0) {
				state.tableData.data = [];
				setTimeout(() => {
					state.tableData.loading = false;
				}, 500);
				for (let i = 0; i < res.data.records.length; i++) {
					const confidences = JSON.parse(res.data.records[i].confidence);
					const labels = JSON.parse(res.data.records[i].label);
					const transformedData = transformData(res.data.records[i], confidences, labels);
					transformedData["num"] = i + 1;
					state.tableData.data[i] = transformedData
				}
				state.tableData.total = res.data.total;
			} else {
				ElMessage({
					type: 'error',
					message: res.msg,
				});
			}
		});
};

const transformData = (originalData, confidences, labels) => {
    const family = labels.map((label, index) => ({
        label: label,
        confidence: confidences[index],
        startTime: originalData.startTime
    }));

    const result = {
		id: originalData.id,
        inputImg: originalData.inputImg,
        outImg: originalData.outImg,
        weight: originalData.weight,
        allTime: originalData.allTime,
        conf: originalData.conf,
        startTime: originalData.startTime,
        username: originalData.username,
        family: family
    };

    return result;
}


// 删除
const onRowDel = (row: any) => {
	ElMessageBox.confirm(`此操作将永久删除该信息，是否继续?`, '提示', {
		confirmButtonText: '确认',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(() => {
			console.log(row);
			request.delete('/api/imgRecords/' + row.id).then((res) => {
				if (res.code == 0) {
					console.log(res.data);
					ElMessage({
						type: 'success',
						message: '删除成功！',
					});
				} else {
					ElMessage({
						type: 'error',
						message: res.msg,
					});
				}
			});
			setTimeout(() => {
				getTableData();
			}, 500);
		})
		.catch(() => { });
};
// 分页改变
const onHandleSizeChange = (val: number) => {
	state.tableData.param.pageSize = val;
	getTableData();
};
// 分页改变
const onHandleCurrentChange = (val: number) => {
	state.tableData.param.pageNum = val;
	getTableData();
};

// 页面加载时
onMounted(() => {
	getTableData();
});
</script>

<style scoped lang="scss">
.system-role-container {
	.system-role-padding {
		padding: 15px;

		.el-table {
			flex: 1;
		}
	}
}
</style>
