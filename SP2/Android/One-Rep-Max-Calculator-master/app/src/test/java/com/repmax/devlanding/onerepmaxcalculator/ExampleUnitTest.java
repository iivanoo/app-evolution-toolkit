package com.repmax.devlanding.onerepmaxcalculator;

import com.repmax.devlanding.onerepmaxcalculator.calculator.OneRepMaxTemplate;
import com.repmax.devlanding.onerepmaxcalculator.calculator.PercentRepMax;

import junit.framework.Assert;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * To work on unit tests, switch the Test Artifact in the Build Variants view.
 */
public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() throws Exception {
        assertEquals(4, 2 + 2);
    }

    @Test
    public void repTest(){
        OneRepMaxTemplate oneRep = new PercentRepMax();
        int[] rep = oneRep.determineRepMaxes(45, 10);
        Assert.assertEquals(49,  rep[5]);
    }

}