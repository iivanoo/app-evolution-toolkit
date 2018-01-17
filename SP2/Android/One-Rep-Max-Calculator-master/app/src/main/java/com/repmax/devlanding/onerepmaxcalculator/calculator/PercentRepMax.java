package com.repmax.devlanding.onerepmaxcalculator.calculator;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by ted on 10/7/16.
 */
public class PercentRepMax extends OneRepMaxTemplate{
    @Override
    public HashMap<Integer, Integer> calculateSpecialOneToTenRepMax() {
        HashMap<Integer, Integer> repPercentagesToMax = new HashMap<>();
        int[] repMaxes = calculateOneToTenRepMax();
        for(int i = 0; i< repMaxes.length; i++){
            int percentage  =calculatePercentOfOneRepMax(i+1);
            repPercentagesToMax.put(repMaxes[i], percentage);
        }
        return repPercentagesToMax;



    }

    public int calculatePercentOfOneRepMax(int reps){
        int percentage;
        switch(reps){
            case 1:
                percentage = 100;
                break;
            case 2:
                percentage = 95;
                break;
            case 3:
                percentage = 93;
                break;
            case 4:
                percentage = 90;
                break;
            case 5:
                percentage = 87;
                break;
            case 6:
                percentage = 85;
                break;
            case 7:
                percentage = 83;
                break;
            case 8:
                percentage = 80;
                break;
            case 9:
                percentage = 77;
                break;
            case 10:
                percentage = 75;
                break;
            default:
                percentage = 0;
                break;
        }
        return percentage;
    }
}
