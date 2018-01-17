package com.AndroidTechies.gamer.randomexcessvariable.honest_methods;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.AndroidTechies.gamer.randomexcessvariable.R;

public class Honest_customAdapter extends ArrayAdapter<String> {

    Context cont;
    String[] honestchapters;
    String[] quotes;
    int[] honest_images;
    LayoutInflater inflater;


    public Honest_customAdapter(Context context,  String[] honestchapters, String[] quotes, int[] honest_images) {
        super(context, R.layout.activity_honest_custom_adapter, honestchapters);

        this.cont = context;
        this.honestchapters = honestchapters;
        this.honest_images = honest_images;
        this.quotes=quotes;
    }

    public class ViewHolder {
        TextView honest_title;
        TextView quote;
        ImageView hon_images;

    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        //checks if view is null and if it is, then creates it.
        if (convertView == null) {
            inflater = (LayoutInflater) cont.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.activity_honest_custom_adapter, null);
        }
        //else
        ViewHolder holder = new ViewHolder();
        //initailise views
        holder.honest_title = (TextView) convertView.findViewById(R.id.text_honestlist);
        holder.quote= (TextView) convertView.findViewById(R.id.subtext_honestlist);

        holder.hon_images = (ImageView) convertView.findViewById(R.id.image_honest);

        //assign them data
        holder.honest_title.setText(honestchapters[position]);
        holder.quote.setText(quotes[position]);

        holder.hon_images.setImageResource(honest_images[position]);

        return convertView;
    }
}
