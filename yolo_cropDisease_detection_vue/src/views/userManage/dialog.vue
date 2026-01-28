<template>
	<div class="system-role-dialog-container">
		<el-dialog :title="state.dialog.title" v-model="state.dialog.isShowDialog" width="800px" class="dia">
			<div class="imgs">
				<el-upload
					v-model="state.form.avatar"
					ref="uploadFile"
					class="avatar-uploader"
					action="http://localhost:9999/files/upload"
					:show-file-list="false"
					:on-success="handleAvatarSuccessone"
				>
					<img v-if="imageUrl" :src="imageUrl" class="avatar" />
					<el-icon v-if="!imageUrl"><Plus /></el-icon>
				</el-upload>
			</div>
			<el-form ref="roleDialogFormRef" :model="state.form" size="default" label-width="100px">
				<el-row :gutter="35">
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="账号" style="color: #000">
							<el-input v-model="state.form.username" placeholder="请输入账号" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="密码">
							<el-input v-model="state.form.password" placeholder="请输入密码" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="姓名" style="color: #000">
							<el-input v-model="state.form.name" placeholder="请输入姓名" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="性别">
							<el-input v-model="state.form.sex" placeholder="请输入性别" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="Email">
							<el-input v-model="state.form.email" placeholder="请输入Email" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="手机号码">
							<el-input v-model="state.form.tel" placeholder="请输入手机号码" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
						<el-form-item label="角色">
							<el-select v-model="state.form.role" value-key="id" placeholder="请选择注册角色" style="width: 100%">
								<el-option v-for="item in option" :key="item.id" :label="item.label" :value="item.role" />
							</el-select>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel" size="default">取 消</el-button>
					<el-button type="primary" @click="onSubmit" size="default">{{ state.dialog.submitTxt }}</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="systemRoleDialog">
import { nextTick, computed, reactive, ref } from 'vue';
import type { UploadInstance, UploadProps } from 'element-plus';
import { ElMessage } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import request from '/@/utils/request';

// 定义子组件向父组件传值/事件
const emit = defineEmits(['refresh']);

const imageUrl = ref('');
const uploadFile = ref<UploadInstance>();

const handleAvatarSuccessone: UploadProps['onSuccess'] = (response, uploadFile) => {
	console.log(response);
	imageUrl.value = URL.createObjectURL(uploadFile.raw!);
	state.form.avatar = response.data;
};

const option = [
	{ id: 1, label: '管理员', role: 'admin' },
	{ id: 2, label: '普通用户', role: 'common' },
];

// 定义变量内容
const roleDialogFormRef = ref();
const state = reactive({
	form: {} as any,
	menuData: [] as TreeType[],
	menuProps: {
		children: 'children',
		label: 'label',
	},
	dialog: {
		isShowDialog: false,
		type: '',
		title: '',
		submitTxt: '',
	},
});

// 打开弹窗
const openDialog = (type: string, row: RowRoleType) => {
	if (type === 'edit') {
		state.form = row;
		state.dialog.title = '修改信息';
		state.dialog.submitTxt = '修 改';
		imageUrl.value = state.form.avatar;
	} else {
		state.dialog.title = '新增信息';
		state.dialog.submitTxt = '新 增';
		// 清空表单，此项需加表单验证才能使用
		nextTick(() => {
			uploadFile.value!.clearFiles(); //该方法就是清理上传列表
			imageUrl.value = '';
		});
	}
	state.dialog.isShowDialog = true;
};
// 关闭弹窗
const closeDialog = () => {
	state.dialog.isShowDialog = false;
};
// 取消
const onCancel = () => {
	closeDialog();
};
// 提交
const onSubmit = () => {
	if (state.form['role'] == '管理员') {
		state.form['role'] = 'admin';
	} else if (state.form['role'] == '普通用户') {
		state.form['role'] = 'common';
	} else if (state.form['role'] == '其他用户') {
		state.form['role'] = 'others';
	}
	if (state.dialog.title == '修改信息') {
		request.post('/api/user/update', state.form).then((res) => {
			if (res.code == 0) {
				ElMessage.success('修改成功！');
				setTimeout(() => {
					closeDialog();
					emit('refresh');
				}, 500);
			} else {
				ElMessage({
					type: 'error',
					message: res.msg,
				});
			}
		});
	} else {
		request.post('/api/user/', state.form).then((res) => {
			if (res.code == 0) {
				ElMessage.success('添加成功！');
			} else {
				ElMessage({
					type: 'error',
					message: res.msg,
				});
			}
			setTimeout(() => {
				closeDialog();
				emit('refresh');
			}, 500);
		});
	}
};

// 暴露变量
defineExpose({
	openDialog,
});
</script>

<style scoped lang="scss">
:deep(.dia) {
	width: 800px;
	height: 650px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.el-form {
	width: 80%;
	margin-left: 10%;
}

.imgs {
	font-size: 28px;
	color: hsl(215, 8%, 58%);
	width: 120px;
	height: 120px;
	display: flex;
	justify-content: center;
	align-items: center;
	border: 1px dashed #d9d9d9;
	border-radius: 6px;
	cursor: pointer;
	margin-left: 320px;
	margin-bottom: 20px;
}

.avatar-uploader .el-upload:hover {
	border-color: #409eff;
}
.avatar {
	width: 120px;
	height: 120px;
	display: block;
}
</style>
