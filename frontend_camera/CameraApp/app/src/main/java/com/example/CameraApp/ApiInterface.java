package com.example.CameraApp;

import org.json.JSONObject;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public interface ApiInterface {
    @Headers("Content-Type: application/json") // JSON 헤더 추가
    @POST("check_similarity")
    Call<Data> postData(@Body Data data);
}

