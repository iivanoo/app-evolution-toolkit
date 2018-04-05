package com.example.chris.infertestappandroid;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.io.*;

public class MainActivity2 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }


    // more dummy text

    public static void foo3 () throws IOException {
        FileOutputStream fos3 = new FileOutputStream(new File("whatever.txt"));
        fos3.write(10);   //DOH! What if exception?
        fos3.close();
    }

    //some dummy text

    public static void foo2 () throws IOException {
        FileOutputStream fos2 = new FileOutputStream(new File("whatever.txt"));
        fos2.write(7);   //DOH! What if exception?
        fos2.close();
    }

    public static void foo () throws IOException {
    	FileOutputStream fos = new FileOutputStream(new File("whatever.txt"));
    	fos.write(7);   //DOH! What if exception?
    	fos.close();
	}
}
