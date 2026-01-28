import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/files")
public class FileController {
    // 图片上传路径（请自行修改为你的实际路径）
    private static final String UPLOAD_PATH = "uploads/";

    @PostMapping("/upload")
    public ResponseEntity<Map<String, Object>> upload(@RequestParam("file") MultipartFile file) {
        Map<String, Object> result = new HashMap<>();
        try {
            // 创建上传目录
            File dir = new File(UPLOAD_PATH);
            if (!dir.exists()) dir.mkdirs();
            
            // 生成唯一文件名
            String originalFilename = file.getOriginalFilename();
            String suffix = originalFilename.substring(originalFilename.lastIndexOf("."));
            String fileName = UUID.randomUUID().toString() + suffix;
            
            // 保存文件
            File destFile = new File(UPLOAD_PATH + fileName);
            file.transferTo(destFile);
            
            // 返回文件路径
            result.put("code", 0);
            result.put("msg", "上传成功");
            result.put("data", UPLOAD_PATH + fileName);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            result.put("code", -1);
            result.put("msg", "上传失败：" + e.getMessage());
            return ResponseEntity.status(500).body(result);
        }
    }
}