package com.AndroidTechies.gamer.randomexcessvariable.cheats;

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
public class frag2 extends Fragment{
    TextView text;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.activity_frag2, container, false);

        View cheatscontentimage = view.findViewById(R.id.lin_cheatcontent);
        Drawable background = cheatscontentimage.getBackground();
        background.setAlpha(100);
        text= (TextView) view.findViewById(R.id.text_frag2);
        return view;
    }
    public void changeData(int index)
    {
        String[]description=getResources().getStringArray(R.array.description);
        text.setText(description[index]);
    }
}
