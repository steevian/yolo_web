package com.example.Kcsj.controller;

import com.alibaba.fastjson.JSONObject;
import com.example.Kcsj.common.Result;
import com.example.Kcsj.entity.ImgRecords;
import com.example.Kcsj.mapper.ImgRecordsMapper;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;
import java.math.BigDecimal;
import java.util.Date;

@RestController
@RequestMapping("/flask")
public class PredictionController {
    @Resource
    ImgRecordsMapper imgRecordsMapper;

    private final RestTemplate restTemplate = new RestTemplate();

    // 定义接收的参数类
    public static class PredictRequest {
        private String startTime;
        private String weight;
        private String username;
        private String inputImg;
        private String kind;
        private String conf;

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getStartTime() {
            return startTime;
        }

        public void setStartTime(String startTime) {
            this.startTime = startTime;
        }

        public String getWeight() {
            return weight;
        }

        public void setWeight(String weight) {
            this.weight = weight;
        }

        public String getInputImg() {
            return inputImg;
        }

        public void setInputImg(String inputImg) {
            this.inputImg = inputImg;
        }

        public String getConf() {
            return conf;
        }

        public void setConf(String conf) {
            this.conf = conf;
        }

        public String getKind() {
            return kind;
        }

        public void setKind(String kind) {
            this.kind = kind;
        }
    }

    @PostMapping("/predict")
    public Result<?> predict(@RequestBody PredictRequest request) {
        if (request == null || request.getInputImg() == null || request.getInputImg().isEmpty()) {
            return Result.error("-1", "未提供图片链接");
        } else if (request.getWeight() == null || request.getWeight().isEmpty()) {
            return Result.error("-1", "未提供权重");
        }

        try {
            // 创建请求体
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<PredictRequest> requestEntity = new HttpEntity<>(request, headers);

            // 调用 Flask API
            String response = restTemplate.postForObject("http://localhost:5000/predictImg", requestEntity, String.class);
            System.out.println("Received response: " + response);
            JSONObject responses = JSONObject.parseObject(response);
            
            if(responses.get("status").equals(400)){
                return Result.error("-1", "Error: " + responses.get("message"));
            } else {
                ImgRecords imgRecords = new ImgRecords();
                imgRecords.setWeight(request.getWeight());
                
                // 修复1：处理 conf 空值 + 转换为 BigDecimal
                String confStr = request.getConf() == null || request.getConf().isEmpty() ? "0.0" : request.getConf();
                imgRecords.setConf(new BigDecimal(confStr));
                
                imgRecords.setKind(request.getKind());
                imgRecords.setInputImg(request.getInputImg());
                imgRecords.setUsername(request.getUsername());
                imgRecords.setStartTime(request.getStartTime());
                
                // 修复2：纠正字段名拼写错误（lable → label）
                imgRecords.setLabel(String.valueOf(responses.get("label")));
                
                // 修复3：处理 confidence 空值 + 转换为 BigDecimal
                String confidenceStr = responses.getString("confidence");
                if (confidenceStr == null || confidenceStr.isEmpty() || "".equals(confidenceStr)) {
                    confidenceStr = "0.0";
                }
                imgRecords.setConfidence(new BigDecimal(confidenceStr));
                
                // 修复4：处理 allTime 空值 + 转换为 BigDecimal
                String allTimeStr = responses.getString("allTime");
                if (allTimeStr == null || allTimeStr.isEmpty()) {
                    allTimeStr = "0.0";
                }
                imgRecords.setAllTime(new BigDecimal(allTimeStr));
                
                imgRecords.setOutImg(String.valueOf(responses.get("outImg")));
                
                // 插入到数据库
                imgRecordsMapper.insert(imgRecords); 
                return Result.success(response);
            }
        } catch (Exception e) {
            e.printStackTrace(); // 打印详细异常，方便排查
            return Result.error("-1", "Error: " + e.getMessage());
        }
    }

    @GetMapping("/file_names")
    public Result<?> getFileNames() {
        try {
            // 调用 Flask API
            String response = restTemplate.getForObject("http://127.0.0.1:5000/file_names", String.class);
            return Result.success(response);
        } catch (Exception e) {
            return Result.error("-1", "Error: " + e.getMessage());
        }
    }
}