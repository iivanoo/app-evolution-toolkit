package com.AndroidTechies.gamer.randomexcessvariable.cheats;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.AndroidTechies.gamer.randomexcessvariable.R;

public class custom_adapterCheats extends ArrayAdapter<String> {

    Context cont;
    String[] chapters;
    String[] tagline;
    int[] images;
    LayoutInflater inflator;


    public custom_adapterCheats(Context context, String[] chapters, int[] images, String[] tagline) {
        super(context, R.layout.activity_custom_adapter_cheats, chapters);

        this.cont = context;
        this.chapters = chapters;
        this.images = images;
        this.tagline=tagline;
    }

    public class ViewHolder {
        TextView names;
        TextView tagline;
        ImageView images;

    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        //checks if view is null and if it is, then creates it.
        if (convertView == null) {
            inflator = (LayoutInflater) cont.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflator.inflate(R.layout.activity_custom_adapter_cheats, null);
        }
        //else
        ViewHolder holder = new ViewHolder();
        //initailise views
        holder.names = (TextView) convertView.findViewById(R.id.text_chapters);
        holder.tagline= (TextView) convertView.findViewById(R.id.subtext_chapters);

        holder.images = (ImageView) convertView.findViewById(R.id.image_cheats);

        //assign them data
        holder.names.setText(chapters[position]);
        holder.tagline.setText(tagline[position]);

        holder.images.setImageResource(images[position]);

        return convertView;
    }
}
