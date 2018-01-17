package com.AndroidTechies.gamer.randomexcessvariable.honest_methods;

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


public class frag1_honest extends Fragment implements AdapterView.OnItemClickListener{
    ListView list_honest;
    honest_method communicator;

    String[]honestchapters={"What’s wrong today?","A good or a bad teacher", "How to study?","Be practical","Who to talk to?","Learn to express","Have a plan","Conclusion"};
    int[]hon_images={R.drawable.whatswrong,R.drawable.goodteacher,R.drawable.howtostudy,R.drawable.bepractical,R.drawable.whotoalkto,R.drawable.learntoexpress,R.drawable.haveaplan,R.drawable.conclusion};
    String[]quote={"What is the problem? ","Excuse me professsor, I have a doubt","That is a good question","Apply the things you study","Share your problems with someone","Stop shying and start talking","Even a backup plan","Something worth reading"};

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.activity_frag1_honest, container, false);
        list_honest=(ListView)view.findViewById(R.id.list_honest);

        View honestlist = view.findViewById(R.id.lin_honestlist);
        Drawable background = honestlist.getBackground();
        background.setAlpha(100);

        Honest_customAdapter adapter=new Honest_customAdapter(getActivity(),honestchapters,quote,hon_images);
        list_honest.setAdapter(adapter);
        list_honest.setOnItemClickListener(this);
        return view;
    }

    public void setCommunicator(honest_method communicator){
        this.communicator= communicator;
    }

    /**
     * Callback method to be invoked when an item in this AdapterView has
     * been clicked.
     * <p/>
     * Implementers can call getItemAtPosition(position) if they need
     * to access the data associated with the selected item.
     *
     * @param parent   The AdapterView where the click happened.
     * @param view     The view within the AdapterView that was clicked (this
     *                 will be a view provided by the adapter)
     * @param i        The position of the view in the adapter.
     * @param id       The row id of the item that was clicked*/
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int i, long id) {
        communicator.respond(i);
    }
    public interface communicator{
        public void respond(int index);
    }

}