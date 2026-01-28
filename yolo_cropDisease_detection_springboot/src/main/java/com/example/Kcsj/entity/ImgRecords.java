package com.example.Kcsj.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@TableName("imgrecords")
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ImgRecords {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private String weight;
    private String inputImg;
    private String outImg;
    
    // 核心修改1：数值型字段改为 BigDecimal 类型
    private BigDecimal confidence;
    private BigDecimal allTime;
    private BigDecimal conf;
    
    private String label;
    private String username;
    private String kind;
    private String startTime;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

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

    public String getOutImg() {
        return outImg;
    }

    public void setOutImg(String outImg) {
        this.outImg = outImg;
    }

    // 核心修改2：更新 BigDecimal 类型的 getter/setter
    public BigDecimal getConfidence() {
        return confidence;
    }

    public void setConfidence(BigDecimal confidence) {
        this.confidence = confidence;
    }

    public BigDecimal getAllTime() {
        return allTime;
    }

    public void setAllTime(BigDecimal allTime) {
        this.allTime = allTime;
    }

    public BigDecimal getConf() {
        return conf;
    }

    public void setConf(BigDecimal conf) {
        this.conf = conf;
    }

    // 核心修改3：修复拼写错误（getLable/setLable → getLabel/setLabel）
    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public String getKind() {
        return kind;
    }

    public void setKind(String kind) {
        this.kind = kind;
    }
}