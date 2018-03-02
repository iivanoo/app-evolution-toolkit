package com.repmax.devlanding.onerepmaxcalculator.calculator;

import java.util.HashMap;
import java.util.List;

/**
 * Created by ted on 10/7/16.
 */
public abstract class OneRepMaxTemplate {

    int weight;
    int repsPerformed;
    public final int[] determineRepMaxes(int weight, int repsPerformed){
        this.weight = weight;
        this.repsPerformed = repsPerformed;
        int[] oneToTenRepMaxs = calculateOneToTenRepMax();
        return oneToTenRepMaxs;

    }

    public double calculateOneRepMax(){
        return weight/(1.0278-(.0278*repsPerformed));
    }

    public int[] calculateOneToTenRepMax(){
        int[] oneToTenRepMaxs = new int[15];
        oneToTenRepMaxs[0] = (int) calculateOneRepMax();

        double oneRepMax = oneToTenRepMaxs[0];
        double coefficient = 1.07;

        for(int i = 1; i < oneToTenRepMaxs.length;i++){
            oneToTenRepMaxs[i] = (int) (oneRepMax / coefficient);

            if(i == 1){
                coefficient += .05;
            }else{
                coefficient += .03;
            }

        }
        return oneToTenRepMaxs;
    }
    public static int[] get10RepMaxs(int weight, int reps) {
        OneRepMaxTemplate oneRepMaxTemplate = new PercentRepMax();
        int[] data = oneRepMaxTemplate.determineRepMaxes(weight, reps);

        return data;
    }

    public abstract HashMap<Integer, Integer> calculateSpecialOneToTenRepMax();


}
