package com.AndroidTechies.gamer.randomexcessvariable.honest_methods;

import android.app.Fragment;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.AndroidTechies.gamer.randomexcessvariable.R;

/**
 * Created by gamer on 4/10/2016.
 */
public class frag2_honest extends Fragment{
    TextView text_honst;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.activity_frag2_honest, container, false);

        View honestcontent = view.findViewById(R.id.lin_honestcontent);
        Drawable background = honestcontent.getBackground();
        background.setAlpha(100);

        text_honst= (TextView) view.findViewById(R.id.text_honest);
        return view;
    }
    public void changeData(int index)
    {
        String[]description=getResources().getStringArray(R.array.honest_description);
        text_honst.setText(description[index]);
    }
}
