package com.example.chris.helloworld;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.io.*;

public class MainActivity4 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
    }

    
    //fbehdbcdhbchd
    // bhdbhfbc
    // ebfhbc
    public static void foo () throws IOException {
    	FileOutputStream fos = new FileOutputStream(new File("whatever.txt"));
    	fos.write(7);   //DOH! What if exception?
    	fos.close();
 }	

 	public static void foo2 () throws IOException {
    	FileOutputStream fos2 = new FileOutputStream(new File("whatever.txt"));
    	fos2.write(7);   //DOH! What if exception?
    	fos2.close();
 }

}
