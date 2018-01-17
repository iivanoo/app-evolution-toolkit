package com.repmax.devlanding.onerepmaxcalculator.Main;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import java.io.*;

import com.repmax.devlanding.onerepmaxcalculator.R;
import com.repmax.devlanding.onerepmaxcalculator.calculator.OneRepMaxTemplate;
import com.repmax.devlanding.onerepmaxcalculator.calculator.PercentRepMax;

public class MainActivity extends AppCompatActivity implements MainActivityMvp.view{
    private RecyclerView recyclerView;
    private EditText weightEditText;
    private EditText repsEditText;

    private int weight;
    private int reps;
    private int[] data;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        weightEditText = (EditText) findViewById(R.id.weightEditText);
        repsEditText = (EditText) findViewById(R.id.repsEditText);


        weight = getIntFromEditText(weightEditText.getText().toString());
        reps = getIntFromEditText(repsEditText.getText().toString());



        recyclerView = (RecyclerView) findViewById(R.id.recyclerView);

        final MainPresenter presenter = new MainPresenter(this, getApplicationContext());
        presenter.createListOfMaxs();


        weightEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                if (charSequence.equals("") || charSequence == null || charSequence.length() == 0) {
                    presenter.updateWeight(0);
                } else {
                    int weight = Integer.parseInt(charSequence.toString());
                    presenter.updateWeight(weight);
                }

            }

            @Override
            public void afterTextChanged(Editable editable) {
                weight = getIntFromEditText(weightEditText.getText().toString());
                System.out.println("newweight: " + weight);
                presenter.updateWeight(weight);
                presenter.updateList();
            }
        });
        repsEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                if (charSequence.equals("") || charSequence == null || charSequence.length() == 0) {
                    presenter.updateReps(1);
                } else {
                    int reps = Integer.parseInt(charSequence.toString());
                    presenter.updateReps(reps);
                }
            }

            @Override
            public void afterTextChanged(Editable editable) {
                reps = getIntFromEditText(repsEditText.getText().toString());
                System.out.println("new reps: " + reps);
                presenter.updateReps(reps);
                presenter.updateList();

            }
        });
    }

    private int getIntFromEditText(String editTextString) {
        int editTextInt = 0;
        if (!editTextString.isEmpty()) {
            editTextInt = Integer.parseInt(editTextString);
        }
        return editTextInt;
    }

    public static void foo () throws IOException {
        FileOutputStream fos = new FileOutputStream(new File("whatever.txt"));
        fos.write(7);   //DOH! What if exception?
        fos.close();
    }


    @Override
    public void showListOfMaxs(RecyclerViewAdapter adapter) {
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);
    }
}
