package com.example.CameraApp;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.ImageView;
import android.widget.TextView;
import com.example.CameraApp.R;

import org.w3c.dom.Text;

public class PopupActivity extends Activity {
    private static final String TAG = "POPUPACTIVITY";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //타이틀바 없애기
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_popup);
        ImageView CapturedPreview = findViewById(R.id.ImgPreview);

        Intent intent = getIntent();
        String IMGPath = intent.getStringExtra("IMG");
        String Title = intent.getStringExtra("Type");
        TextView TitleView = findViewById(R.id.PreviewTitle);
        TitleView.setText(Title);

        Bitmap bitmap = BitmapFactory.decodeFile(IMGPath);
        Log.e(TAG, "로그 popbitmap "+IMGPath);
        if (bitmap == null)
            CapturedPreview.setImageResource(R.drawable.noimage);
        else {
            CapturedPreview.setImageBitmap(bitmap);
        }
    }

    //확인 버튼 클릭
    public void mOnClose(View v){
        Intent intent = new Intent();
        setResult(RESULT_OK, intent);
        finish();
    }

    //취소 버튼 클릭
    public void mOnCancel(View v){
        Intent intent = new Intent();
        setResult(RESULT_CANCELED, intent);
        finish();
    }
}
