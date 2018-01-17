package com.repmax.devlanding.onerepmaxcalculator.Main;

import android.content.Context;
import android.support.annotation.NonNull;

import com.repmax.devlanding.onerepmaxcalculator.calculator.OneRepMaxTemplate;

/**
 * Created by ted on 11/20/16.
 */

public class MainPresenter implements MainActivityMvp.presenter{
    private int[] data;
    private RecyclerViewAdapter adapter;

    private final MainActivityMvp.view view;
    private final Context context;
    private int reps;
    private int weight;

    public MainPresenter(MainActivityMvp.view view, Context context){
        this.view = view;
        this.context = context;
    }
    @Override
    public void createListOfMaxs(){
        weight = 200;
        reps = 5;
        data = OneRepMaxTemplate.get10RepMaxs(weight, reps);
        adapter = new RecyclerViewAdapter(context, data);
        view.showListOfMaxs(adapter);

    }

    @Override
    public void updateWeight(@NonNull int weight) {
        this.weight = weight;
    }

    public void updateList() {
        data = OneRepMaxTemplate.get10RepMaxs(weight, reps);
        adapter.updateList(data);
    }

    public void updateReps(@NonNull int reps) {
        this.reps = reps;
    }
}
