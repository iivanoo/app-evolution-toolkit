package com.AndroidTechies.gamer.randomexcessvariable.cheats;

import android.app.Fragment;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;

import com.AndroidTechies.gamer.randomexcessvariable.R;

public class frag1 extends Fragment implements AdapterView.OnItemClickListener {
    ListView list;
    listofcheats communicator;

    String[]chapters={"The Specks Case","Disposable cheating", "The clocked friendship", "The creative artist", "Love your shoes", "The shoulder tapping", "The warrior technique", "The distracting escapade (difficult)", "The Pepsi saves the day", "The desperate maneuver", "The last resort suggested", "Some helpful tips"};
    int[]images={R.drawable.speckscase,R.drawable.disposablecheating,R.drawable.clockedfriendship,R.drawable.creativeartist,R.drawable.loveyourshoes,R.drawable.shouldertapping,R.drawable.warrior,R.drawable.thedistractingescapade,R.drawable.papsisaves,R.drawable.desperatemanuver,R.drawable.lastresort,R.drawable.helpfultips};
    String[]tagline={"The curious case of spectacles","No one will know","How much do you trust your friend?","Let's be creative","As long as you need them","Tap, tap, tap","Spartans never surrender","Look who's there.","Quench your thirst, cheat first","Will you try this?","The devil awaits to hug you","Crack the cracker using the cracks"};

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.activity_frag1, container, false);

        View cheatsintroimage = view.findViewById(R.id.rel_fragcheat);
        Drawable background = cheatsintroimage.getBackground();
        background.setAlpha(100);


        list = (ListView) view.findViewById(R.id.listView);
        custom_adapterCheats adapter=new custom_adapterCheats(getActivity(),chapters,images,tagline);
        list.setAdapter(adapter);
        list.setOnItemClickListener(this);
        return view;
    }


    public void setCommunicator(listofcheats communicator) {
        this.communicator = communicator;
    }

    /**
     * Callback method to be invoked when an item in this AdapterView has
     * been clicked.
     * <p>
     * Implementers can call getItemAtPosition(position) if they need
     * to access the data associated with the selected item.
     *
     * @param parent The AdapterView where the click happened.
     * @param view   The view within the AdapterView that was clicked (this
     *               will be a view provided by the adapter)
     * @param i      The position of the view in the adapter.
     * @param id     The row id of the item that was clicked
     */
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int i, long id) {
        communicator.respond(i);
    }

    public interface communicator {
        public void respond(int index);
    }
}
