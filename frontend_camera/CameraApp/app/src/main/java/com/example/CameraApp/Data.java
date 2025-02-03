package com.example.CameraApp;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import org.json.JSONObject;

public class Data {
    @Expose
    @SerializedName("image_base64") private String image_base64;

    public String getImage_base64() {
        return image_base64;
    }
    public void setImage_base64(String image_base64) {
        this.image_base64 = image_base64;
    }
}