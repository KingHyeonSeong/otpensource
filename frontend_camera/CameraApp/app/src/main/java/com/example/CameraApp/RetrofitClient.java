package com.example.CameraApp;

import android.util.Log;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private static Retrofit retrofit;
    private static final String TAG = "RetrofitClient";

    public static Retrofit getRetrofit(String ServerAddr){
        if(retrofit==null){
            Retrofit.Builder builder = new Retrofit.Builder();
            builder.baseUrl("https://"+ServerAddr+".ngrok-free.app/");
            builder.addConverterFactory(GsonConverterFactory.create());
            Log.e(TAG, "로그 getRetrofit "+"https://"+ServerAddr+".ngrok-free.app/");
            retrofit = builder.build();
        }
        return retrofit;
    }
}