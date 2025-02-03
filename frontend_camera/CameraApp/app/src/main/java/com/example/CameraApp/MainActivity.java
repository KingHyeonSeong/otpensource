package com.example.CameraApp;

import static java.security.AccessController.getContext;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ColorMatrix;
import android.graphics.ColorMatrixColorFilter;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.hardware.camera2.CameraAccessException;
import android.media.ExifInterface;
import android.media.Image;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.annotation.ColorInt;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

/*
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.segmentation.Segmentation;
import com.google.mlkit.vision.segmentation.SegmentationMask;
import com.google.mlkit.vision.segmentation.Segmenter;
import com.google.mlkit.vision.segmentation.selfie.SelfieSegmenterOptions;
import com.google.mlkit.vision.segmentation.subject.SubjectSegmenterOptions;
import android.graphics.PorterDuff;
import android.graphics.PorterDuffXfermode;
*/

import org.json.JSONException;
import org.json.JSONObject;

import java.nio.ByteBuffer;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Callback;



public class MainActivity extends AppCompatActivity {

    private static final int REQUEST_CAMERA_PERMISSION = 200;
    private static final int PICK_IMAGE_REQUEST = 1;
    private static final String TAG = "MAINACTIVITY";
    private static final int REQUEST_IMAGE_CAPTURE = 672;
    private static final int SHOW_RESULT_POPUP = 300;
    private static final float contrast = 1.5f, brightness = -50.0f;
    private static final int fixedWidth = 1080;
    private int UploadCnt = 0;

    private Context mContext;
    private Bitmap fixedBitmap;
    private Button btnUpload, btnCapture;
    private TextView statusTextView;
    private List<Uri> imageUris = new ArrayList<>();
    private String CapturePath;
    private Uri CapturedUrl;
    private String imageFileName;
    private EditText ServerText;
    private String Strprt1, Strprt2;
    private int Toastidx = 0;

    private SharedPreferences preferences;
    private SharedPreferences.Editor editor;
    public String ServerAddr = "", PrevAddr = "";
    //Segmenter segmenter;
    ApiInterface api;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        mContext = this;
        btnCapture = findViewById(R.id.CaptureButton);
        btnUpload = findViewById(R.id.UploadButton);
        statusTextView = findViewById(R.id.StatusText);
        ServerText = findViewById(R.id.ServerAddr);

        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{
                    android.Manifest.permission.CAMERA,
                    android.Manifest.permission.READ_MEDIA_IMAGES,
            }, REQUEST_CAMERA_PERMISSION);
        }

        File dir = new File(Environment.getExternalStorageDirectory()+"/DCIM/CameraAPP");
        if (!dir.exists()) {
            Log.e(TAG, "mkdir MainDir");
            dir.mkdirs();
        }

        //segmenterCreate();
        preferences = getSharedPreferences("Server_Address", MODE_PRIVATE);
        editor = preferences.edit();
        ServerAddr = preferences.getString("Server_Address","");
        PrevAddr = ServerAddr;
        ServerText.setText(ServerAddr);

        btnCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                UpdateServerAddr();
                openCaptureCamera();
            }
        });

        btnUpload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                UpdateServerAddr();
                openImageChooser();
            }
        });
    }
    /*
    public void segmenterCreate() {
        SelfieSegmenterOptions options =
                new SelfieSegmenterOptions.Builder()
                        .setDetectorMode(SelfieSegmenterOptions.SINGLE_IMAGE_MODE)
                        .enableRawSizeMask()
                        .build();
        segmenter = Segmentation.getClient(options);
    }
    */

    private void openCaptureCamera() {
        Log.d(TAG, "로그 openCaptureCamera");
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(intent.resolveActivity(getPackageManager()) != null) {
            File CapturedImage = null;
            try {
                CapturedImage = createImageFile();
            }
            catch (IOException e) {}
            if(CapturedImage != null) {
                CapturedUrl = FileProvider.getUriForFile(getApplicationContext(), getPackageName(),CapturedImage);
                Log.d(TAG, "로그 Path "+CapturedUrl);;
                intent.putExtra(MediaStore.EXTRA_OUTPUT,CapturedUrl);
                startActivityForResult(intent,REQUEST_IMAGE_CAPTURE);
            }
        }
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        imageFileName = "CameraAPP_" + timeStamp;

        File storageDir = new File(Environment.getExternalStorageDirectory().getPath() + "/DCIM/CameraAPP");
        Log.d(TAG, "로그 경로 "+Environment.getExternalStorageDirectory().getPath());
        File image = File.createTempFile(
                imageFileName,
                ".jpg",
                storageDir
        );
        CapturePath = image.getAbsolutePath();
        return image;
    }

    private void openImageChooser() {
        Log.d(TAG, "로그 openImageChooser");
        imageUris.clear();
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT); // ACTION_PICK 으로 바꾸면 기존 APP에서 Uri만 복사됨 (실제 파일명 얻기 가능)
        intent.setType("image/*");
        //intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        startActivityForResult(Intent.createChooser(intent, "Select Pictures"), PICK_IMAGE_REQUEST);
        Toast.makeText(this,"Select Images",Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d(TAG, "로그 onActivityResult");
        if (requestCode == PICK_IMAGE_REQUEST && resultCode == Activity.RESULT_OK) {
            if (data != null) {
                if (data.getClipData() != null) {
                    Uri imageUri = data.getClipData().getItemAt(0).getUri();
                    Log.d(TAG, "로그 Select : " + imageUri);
                    try {
                        InputStream is = getContentResolver().openInputStream(imageUri);
                        Bitmap bitmap = BitmapFactory.decodeStream(is);
                        Log.d(TAG, "로그 Select : " + bitmap);

                        int exifDegree = 0, origWidth = bitmap.getWidth(), origHeight = bitmap.getHeight();
                        if (origWidth > origHeight)
                            exifDegree = 90;
                        bitmap = rotate(bitmap, exifDegree);

                        int newWidth = fixedWidth;
                        int newHeight = (newWidth * bitmap.getHeight())/bitmap.getWidth();
                        bitmap = Bitmap.createScaledBitmap(bitmap, newWidth, newHeight, true);

                        fixedBitmap = changeBitmapContrastBrightness(bitmap,contrast,brightness);

                        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
                        String FixedCapturePath = Environment.getExternalStorageDirectory()+"/DCIM/CameraAPP/CameraAPP_"+timeStamp+".jpg";
                        final File file = new File(FixedCapturePath);
                        FileOutputStream output = null;
                        byte[] bytes = bitmapToByteArray(fixedBitmap);
                        try{
                            Log.d(TAG, "로그 " + file.getAbsolutePath());
                            output = new FileOutputStream(file);
                            output.write(bytes);
                            output.close();
                            ToastFullPath(file.getAbsolutePath());

                            Intent intent = new Intent(MainActivity.this, PopupActivity.class);
                            intent.putExtra("IMG",FixedCapturePath);
                            intent.putExtra("Type","Selected Image");
                            startActivityForResult(intent, SHOW_RESULT_POPUP);
                        }
                        catch (Exception e) {
                            Log.e(TAG, "로그 save error "+e);
                            throw new RuntimeException(e);
                        }
                    }
                    catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
            else
            {
                Log.e(TAG, "로그 No Select");
                Toast.makeText(this,"Selected No Image",Toast.LENGTH_SHORT).show();
            }
        }
        else if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
            Bitmap bitmap = BitmapFactory.decodeFile(CapturePath);

            ExifInterface exif = null;
            try {
                exif = new ExifInterface(CapturePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
            int exifOrientation, exifDegree;
            if (exif != null) {
                exifOrientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
                exifDegree = exifOrientationToDegress(exifOrientation);
            } else {
                exifDegree = 0;
            }
            bitmap = rotate(bitmap, exifDegree);

            int newWidth = fixedWidth;
            int newHeight = (newWidth * bitmap.getHeight())/bitmap.getWidth();
            bitmap = Bitmap.createScaledBitmap(bitmap, newWidth, newHeight, true);

            fixedBitmap = changeBitmapContrastBrightness(bitmap,contrast,brightness);

            String FixedCapturePath = CapturePath.substring(0,CapturePath.length()-4)+"_fixed.jpg";
            final File file = new File(FixedCapturePath);
            FileOutputStream output = null;
            byte[] bytes = bitmapToByteArray(fixedBitmap);
            try{
                Log.d(TAG, "로그 " + file.getAbsolutePath());
                output = new FileOutputStream(file);
                output.write(bytes);
                output.close();
                ToastFullPath(file.getAbsolutePath());

                fileDelete(CapturePath);
                Intent intent = new Intent(MainActivity.this, PopupActivity.class);
                intent.putExtra("IMG",FixedCapturePath);
                intent.putExtra("Type","Captured Image");
                startActivityForResult(intent, SHOW_RESULT_POPUP);
            }
            catch (Exception e) {
                Log.e(TAG, "로그 save error "+e);
                throw new RuntimeException(e);
            }
        }
        else if (requestCode == SHOW_RESULT_POPUP && resultCode == Activity.RESULT_OK) {
            PostBitmap(fixedBitmap);
        }
    }
    public void ToastFullPath(String Str) {
        Toastidx = 0;
        int idx = Str.lastIndexOf('/');
        Strprt1 = "Saved as "+Str.substring(0,idx+1);
        Strprt2 = Str.substring(idx+1);
        Timer m_timer = new Timer();
        m_timer.schedule( new TimerTask()  { // TimerTask, Timer 매번 생성해야함
            @Override
            public void run()
            {
                if (Toastidx == 0)
                {
                    runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(mContext,Strprt1,Toast.LENGTH_SHORT).show();
                        }
                    });
                    Toastidx++;
                }
                else if (Toastidx == 1)
                {
                    runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(mContext,Strprt2,Toast.LENGTH_SHORT).show();
                        }
                    });
                    m_timer.cancel();
                }
            }
        },0,2500); // 시간 조절 (초기 대기시간, 주기)
    }

    public void UpdateServerAddr() {
        ServerAddr = ServerText.getText().toString();
        if (api == null || !PrevAddr.equals(ServerAddr))
        {
            api = RetrofitClient.getRetrofit(ServerAddr).create(ApiInterface.class);
            editor.clear();
            editor.putString("Server_Address",ServerAddr);
            editor.commit();
            PrevAddr = ServerAddr;
        }
    }

    public void PostBitmap(Bitmap bitmap) {
        String StatusMsg = "Status: Uploading in progress";
        statusTextView.setText(StatusMsg);

        Data data = new Data();
        byte[] bytes = bitmapToByteArray(bitmap);
        String bitmapStr = Base64.encodeToString(bytes,Base64.DEFAULT);
        data.setImage_base64(bitmapStr);

        Log.e(TAG, "로그 PostBitmap");
        api.postData(data).enqueue(new Callback<Data>() {
            @Override
            public void onResponse(Call<Data> call, Response<Data> response) {
                Log.e(TAG, "로그 onResponse " + response);
                if(response.isSuccessful()){
                    UploadCnt++;
                    Log.e(TAG, "로그 isSuccessful " +response.message());
                    String StatusMsg;
                    if (UploadCnt == 1) {
                        StatusMsg = "Status: "+UploadCnt+" Image is uploaded";
                    }
                    else {
                        StatusMsg = "Status: " + UploadCnt + " Images are uploaded";
                    }
                    statusTextView.setText(StatusMsg);
                }
                else {
                    String Msg = "Status: Upload Failed ("+response.message()+")";
                    statusTextView.setText(Msg);
                }
            }

            @Override
            public void onFailure(Call<Data> call, Throwable t) {
                Log.e(TAG, "로그 onFailure");
                String Msg = "Status: Upload Failed";
                statusTextView.setText(Msg);
            }
        });
    }

    public static Bitmap changeBitmapContrastBrightness(Bitmap bmp, float contrast, float brightness)
    {
        ColorMatrix cm = new ColorMatrix(new float[]
                {
                        contrast, 0, 0, 0, brightness,
                        0, contrast, 0, 0, brightness,
                        0, 0, contrast, 0, brightness,
                        0, 0, 0, 1, 0
                });
        Bitmap ret = Bitmap.createBitmap(bmp.getWidth(), bmp.getHeight(), bmp.getConfig());
        Canvas canvas = new Canvas(ret);
        Paint paint = new Paint();
        paint.setColorFilter(new ColorMatrixColorFilter(cm));
        canvas.drawBitmap(bmp, 0, 0, paint);
        return ret;
    }

    /*
    @ColorInt
    private int[] maskColorsFromByteBuffer(ByteBuffer byteBuffer, int maskWidth, int maskHeight) {
        @ColorInt int[] colors = new int[maskWidth * maskHeight];
        for (int i = 0; i < maskWidth * maskHeight; i++) {
            float backgroundLikelihood = 1 - byteBuffer.getFloat();
            if (backgroundLikelihood > 0.9) {
                colors[i] = Color.rgb(51, 112, 69); // 높은 확률의 배경일 경우 녹색으로 설정
            } else if (backgroundLikelihood > 0.2) {
                colors[i] = Color.rgb(51, 112, 69); // 일반적인 배경일 경우 녹색으로 설정
            }
        }
        return colors;
    }
    */

    public boolean fileDelete(String filePath){
        try {
            File file = new File(filePath);
            if(file.exists()){
                file.delete();
                return true;
            }
        }catch (Exception e){
            e.printStackTrace();
        }
        return false;
    }

    private int exifOrientationToDegress(int exifOrientation) {
        if(exifOrientation == ExifInterface.ORIENTATION_ROTATE_90){
            return 90;
        } else if (exifOrientation == ExifInterface.ORIENTATION_ROTATE_180){
            return 180;
        } else if ((exifOrientation == ExifInterface.ORIENTATION_ROTATE_270)) {
            return 270;
        }
        return 0;
    }

    private Bitmap rotate(Bitmap bitmap, int exifDegree) {
        Matrix matrix = new Matrix();
        matrix.postRotate(exifDegree);
        return Bitmap.createBitmap(bitmap,0,0,bitmap.getWidth(),bitmap.getHeight(),matrix,true);
    }

    public Bitmap byteArrayToBitmap( byte[] byteArray ) {
        Bitmap bitmap = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
        return bitmap;
    }

    public byte[] bitmapToByteArray(Bitmap bitmap) {
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
        byte[] byteArray = stream.toByteArray();
        return byteArray;
    }

    @Override
    protected void onResume() {
        Log.e(TAG, "로그 onResume");
        super.onResume();
    }

    @Override
    protected void onPause() {
        Log.e(TAG, "로그 onPause");
        super.onPause();
    }
}


/* 누끼따는 코드 (미사용)
            InputImage mlImage = InputImage.fromBitmap(bitmap, 0);
            Bitmap finalBitmap = bitmap;
            segmenter.process(mlImage)
                    .addOnSuccessListener(new OnSuccessListener<SegmentationMask>() {
                        @Override
                        public void onSuccess(@NonNull SegmentationMask segmentationMask) {
                            // Segmentation 성공 시 호출되는 메서드

                            // SegmentationMask에서 ByteBuffer, 가로 및 세로 크기를 가져옵니다.
                            ByteBuffer mask = segmentationMask.getBuffer();
                            int maskWidth = segmentationMask.getWidth();
                            int maskHeight = segmentationMask.getHeight();

                            // ByteBuffer에서 색상 배열을 가져옵니다.
                            int[] arr = maskColorsFromByteBuffer(mask, maskWidth, maskHeight);

                            // 새로운 비트맵 객체를 생성합니다.
                            Bitmap segmentedBitmap = Bitmap.createBitmap(newWidth, newHeight, Bitmap.Config.ARGB_8888);
                            Bitmap maskBitmap = Bitmap.createBitmap(arr, maskWidth, maskHeight, Bitmap.Config.ARGB_8888);

                            // Canvas를 사용하여 이미지를 그립니다.
                            Canvas canvas = new Canvas(segmentedBitmap);
                            Paint paint = new Paint();
                            canvas.drawBitmap(finalBitmap, 0, 0, paint);

                            // Xfermode를 설정하여 마스크를 적용합니다.
                            paint.setXfermode(new PorterDuffXfermode(PorterDuff.Mode.SRC_ATOP));

                            // 비트맵 크기를 조정하고 이동시켜서 블렌딩합니다.
                            Matrix matrixz = new Matrix();
                            matrixz.setScale((float) finalBitmap.getWidth() / maskBitmap.getWidth(), (float) finalBitmap.getHeight() / maskBitmap.getHeight());
                            matrixz.postTranslate(0, 0);
                            canvas.drawBitmap(maskBitmap, matrixz, paint);

                            fixedBitmap = segmentedBitmap;

                            String FixedCapturePath = CapturePath.substring(0,CapturePath.length()-4)+"_fixed.jpg";
                            final File file = new File(FixedCapturePath);
                            FileOutputStream output = null;
                            byte[] bytes = bitmapToByteArray(fixedBitmap);
                            try{
                                Log.d(TAG, "로그 " + file.getAbsolutePath());
                                output = new FileOutputStream(file);
                                output.write(bytes);
                                output.close();
                            }
                            catch (Exception e) {
                                Log.e(TAG, "로그 save error "+e);
                                throw new RuntimeException(e);
                            }
                            fileDelete(CapturePath);
                            Intent intent = new Intent(MainActivity.this, PopupActivity.class);
                            intent.putExtra("IMG",FixedCapturePath);
                            intent.putExtra("Type","Captured Image");
                            startActivityForResult(intent, SHOW_RESULT_POPUP);
                        }
                    });
            */



