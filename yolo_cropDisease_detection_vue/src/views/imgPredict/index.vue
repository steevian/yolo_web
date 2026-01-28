<template>
	<div class="system-predict-container layout-padding">
		<div class="system-predict-padding layout-padding-auto layout-padding-view">
			<div class="header">
				<div class="weight">
					<el-select v-model="kind" placeholder="请选择作物种类" size="large" style="width: 200px" @change="getData">
						<el-option v-for="item in state.kind_items" :key="item.value" :label="item.label"
							:value="item.value" />
					</el-select>
				</div>
				<div class="weight">
					<el-select v-model="weight" placeholder="请选择模型" size="large" style="margin-left: 20px;width: 200px">
						<el-option v-for="item in state.weight_items" :key="item.value" :label="item.label"
							:value="item.value" />
					</el-select>
				</div>
				<div class="conf" style="margin-left: 20px;display: flex; flex-direction: row;">
					<div
						style="font-size: 14px;margin-right: 20px;display: flex;justify-content: start;align-items: center;color: #909399;">
						设置最小置信度阈值</div>
					<el-slider v-model="conf" :format-tooltip="formatTooltip" style="width: 300px;" />
				</div>
				<div class="button-section" style="margin-left: 20px">
					<el-button type="primary" @click="upData" class="predict-button">开始预测</el-button>
				</div>
			</div>
			<el-card shadow="hover" class="card">
				<el-upload v-model="state.img" ref="uploadFile" class="avatar-uploader"
					action="http://localhost:9999/files/upload" :show-file-list="false"
					:on-success="handleAvatarSuccessone">
					<img v-if="imageUrl" :src="imageUrl" class="avatar" />
					<el-icon v-else class="avatar-uploader-icon">
						<Plus />
					</el-icon>
				</el-upload>
			</el-card>
			<el-card class="result-section" v-if="state.predictionResult.label">
				<div class="bottom">
					<div style="width: 33%">识别结果：{{ state.predictionResult.label }}</div>
					<div style="width: 33%">预测概率：{{ state.predictionResult.confidence }}</div>
					<div style="width: 33%">总时间：{{ state.predictionResult.allTime }}</div>
				</div>
			</el-card>
		</div>
	</div>
</template>

<script setup lang="ts" name="personal">
import { reactive, ref, onMounted } from 'vue';
import type { UploadInstance, UploadProps } from 'element-plus';
import { ElMessage } from 'element-plus';
import request from '/@/utils/request';
import { Plus } from '@element-plus/icons-vue';
import { useUserInfo } from '/@/stores/userInfo';
import { storeToRefs } from 'pinia';
import { formatDate } from '/@/utils/formatTime';

// 初始化变量，修复conf默认值为空的问题
const imageUrl = ref('');
const conf = ref(50); // 默认置信度50%
const weight = ref('');
const kind = ref('');
const uploadFile = ref<UploadInstance>();
const stores = useUserInfo();
const { userInfos } = storeToRefs(stores);

const state = reactive({
	weight_items: [] as any,
	kind_items: [
		{
			value: 'corn',
			label: '玉米',
		},
		{
			value: 'rice',
			label: '水稻',
		},
		{
			value: 'strawberry',
			label: '草莓',
		},
		{
			value: 'tomato',
			label: '西红柿',
		},
	],
	img: '',
	predictionResult: {
		label: '',
		confidence: '',
		allTime: '',
	},
	form: {
		username: '',
		inputImg: null as any,
		weight: '',
		conf: null as any,
		kind: '',
		startTime: ''
	},
});

// 格式化滑块提示
const formatTooltip = (val: number) => {
	return val / 100;
};

// 图片上传成功回调
const handleAvatarSuccessone: UploadProps['onSuccess'] = (response, uploadFile) => {
	imageUrl.value = URL.createObjectURL(uploadFile.raw!);
	state.img = response.data;
};

// 获取模型列表 - 修复接口地址 + 解析逻辑
const getData = () => {
	// 增加参数校验：必须选择作物种类才请求
	if (!kind.value) {
		state.weight_items = [];
		ElMessage.warning('请先选择作物种类');
		return;
	}
	
	// 修复1：接口地址改为后端实际地址 /flask/file_names（去掉/api前缀）
	request.get('/flask/file_names')
		.then((res) => {
			try {
				// 修复2：兼容不同的返回格式
				const data = typeof res === 'string' ? JSON.parse(res) : res;
				// 过滤对应作物的模型
				state.weight_items = data.weight_items?.filter(item => item.value.includes(kind.value)) || [];
			} catch (e) {
				console.error('解析模型列表失败:', e);
				ElMessage.error('解析模型列表失败，请检查后端返回格式');
			}
		})
		.catch(error => {
			console.error('获取模型列表失败:', error);
			ElMessage.error('获取模型列表失败，请检查Flask服务是否启动');
		});
};

// 开始预测 - 核心修复：适配后端返回格式 + 容错处理
const upData = () => {
	// 完善参数校验
	if (!kind.value) return ElMessage.warning('请选择作物种类');
	if (!weight.value) return ElMessage.warning('请选择模型');
	if (!state.img) return ElMessage.warning('请上传检测图片');
	
	// 组装请求参数
	state.form.weight = weight.value;
	state.form.conf = (conf.value / 100).toString(); // 转为字符串，适配后端接收格式
	state.form.username = userInfos.value.userName || 'admin'; // 兜底默认值
	state.form.inputImg = state.img;
	state.form.kind = kind.value;
	state.form.startTime = formatDate(new Date(), 'YYYY-mm-dd HH:MM:SS');
	
	console.log('预测请求参数:', state.form);
	
	// 修复1：接口地址改为 /flask/predict（去掉/api前缀）
	request.post('/flask/predict', state.form)
		.then((res) => {
			try {
				// 修复2：统一解析逻辑，兼容多层嵌套的JSON字符串
				let result = res;
				// 如果返回的是封装后的结果，取data字段；否则直接用res
				if (res.data) {
					result = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
				}
				
				// 修复3：判断后端返回的状态码（Flask返回的是status字段）
				if (result.status === 200) {
					// 处理识别结果：兼容字符串/数组格式
					let label = result.label || '未识别到病害';
					if (Array.isArray(label)) {
						label = label.join('、'); // 数组转字符串，方便展示
					}
					
					// 处理置信度：确保是数值格式
					const confidence = result.confidence || 0;
					const allTime = result.allTime || 0;
					
					// 更新页面展示结果
					state.predictionResult = {
						label: label,
						confidence: `${(confidence * 100).toFixed(2)}%`, // 转为百分比展示
						allTime: `${allTime.toFixed(2)}秒` // 格式化耗时
					};
					
					// 覆盖原图片（预测结果图）
					if (result.outImg) {
						imageUrl.value = result.outImg;
					}
					
					ElMessage.success('预测成功！');
				} else {
					// 后端返回业务错误
					ElMessage.error(result.message || '预测失败，请重试');
				}
			} catch (error) {
				console.error('解析检测结果失败:', error);
				ElMessage.error('解析检测结果失败，请检查后端返回格式');
			}
		})
		.catch(error => {
			// 捕获网络/接口错误
			console.error('预测接口请求失败:', error);
			ElMessage.error('接口调用失败，请检查SpringBoot和Flask服务是否都已启动');
		});
};

// 页面挂载时初始化
onMounted(() => {
	// 可选：默认加载玉米模型
	kind.value = 'corn';
	getData();
});
</script>

<style scoped lang="scss">
.system-predict-container {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;

	.system-predict-padding {
		padding: 15px;

		.el-table {
			flex: 1;
		}
	}
}

.header {
	width: 100%;
	height: 5%;
	display: flex;
	justify-content: start;
	align-items: center;
	font-size: 20px;
}

.card {
	width: 100%;
	height: 95%;
	border-radius: 10px;
	margin-top: 15px;
	display: flex;
	justify-content: center;
	align-items: center;
}

.avatar-uploader .avatar {
	width: 100%;
	height: 600px;
	display: block;
	object-fit: contain; // 修复图片拉伸问题
}

.el-icon.avatar-uploader-icon {
	font-size: 28px;
	color: #8c939d;
	width: 100%;
	height: 600px;
	text-align: center;
	line-height: 600px; // 修复图标垂直居中
}

.button-section {
	display: flex;
	justify-content: center;
}

.predict-button {
	width: 100%;
	/* 按钮宽度填满 */
}

.result-section {
	width: 100%;
	margin-top: 15px;
	text-align: center;
	display: flex;
	/* 添加 display: flex; */
	flex-direction: column;
	border-radius: 6px;
	padding: 20px 0; // 增加内边距
}

.bottom {
	width: 100%;
	font-size: 18px;
	display: flex;
	/* 添加 display: flex; */
	flex-direction: row;
	justify-content: center;
	align-items: center;
	gap: 20px; // 增加间距
}
</style>