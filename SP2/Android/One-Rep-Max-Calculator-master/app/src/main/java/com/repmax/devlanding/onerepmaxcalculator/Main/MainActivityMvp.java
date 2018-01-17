package com.repmax.devlanding.onerepmaxcalculator.Main;

/**
 * Created by ted on 11/20/16.
 */

public class MainActivityMvp {
    interface view{

        void showListOfMaxs(RecyclerViewAdapter adapter);
    }
    interface presenter{

        void createListOfMaxs();

        void updateWeight(int weight);
    }
}
