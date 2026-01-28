import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/flask")
public class FlaskController {
    // Flask模型服务地址
    private static final String FLASK_BASE_URL = "http://127.0.0.1:5000";
    private final RestTemplate restTemplate = new RestTemplate();

    // 1. 获取模型列表接口
    @GetMapping("/file_names")
    public ResponseEntity<Map<String, Object>> getFileNames() {
        Map<String, Object> result = new HashMap<>();
        try {
            // 转发请求到Flask服务
            String flaskResponse = restTemplate.getForObject(FLASK_BASE_URL + "/file_names", String.class);
            result.put("code", 0);
            result.put("msg", "success");
            result.put("data", flaskResponse);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            result.put("code", -1);
            result.put("msg", "获取模型列表失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(result);
        }
    }

    // 2. 图像检测预测接口
    @PostMapping("/predict")
    public ResponseEntity<Map<String, Object>> predict(@RequestBody Map<String, Object> params) {
        Map<String, Object> result = new HashMap<>();
        try {
            // 转发请求到Flask服务
            String flaskResponse = restTemplate.postForObject(FLASK_BASE_URL + "/predict", params, String.class);
            result.put("code", 0);
            result.put("msg", "success");
            result.put("data", flaskResponse);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            result.put("code", -1);
            result.put("msg", "预测失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(result);
        }
    }
}