package mduashisharchit.org.mdu;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;

import java.util.Arrays;
import java.util.List;


public class semester extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_semester);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_semester, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            String devPage = "devPage";
            Intent intent = new Intent(this , Syllabus.class).putExtra(Intent.EXTRA_TEXT, devPage );
            startActivity(intent);
            return true;
        }
        if(id == R.id.action_share){
            Intent sendIntent = new Intent();
            sendIntent.setAction(Intent.ACTION_SEND);
            sendIntent.putExtra(Intent.EXTRA_TEXT, "Take a look at \"MDU\" - https://play.google.com/store/apps/details?id=mduashisharchit.org.mdu");
            sendIntent.setType("text/plain");
            startActivity(sendIntent);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {
        private ArrayAdapter<String> semAdapter;

        public PlaceholderFragment() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            Intent intent = getActivity().getIntent();
            View rootView = inflater.inflate(R.layout.fragment_semester, container, false);
            AdView mAdView = (AdView) rootView.findViewById(R.id.adView);
            AdRequest adRequest = new AdRequest.Builder().build();
            mAdView.loadAd(adRequest);

            if (intent != null && intent.hasExtra(Intent.EXTRA_TEXT)) {
                String semStr = intent.getStringExtra(Intent.EXTRA_TEXT);
                switch (semStr) {
                    case "B.techIT": {
                        chooseSemester(rootView , semStr);
                    }
                    break;
                    case "B.techCSE": {
                        chooseSemester(rootView, semStr);
                    }
                    break;
                    case "B.techECE": {

                        chooseSemester(rootView, semStr);
                    }
                    break;
                    case "B.techMECHANICAL": {

                        chooseSemester(rootView, semStr);
                    }
                    break;
                }


            }
            return rootView;
        }
        private void chooseSemester(View rootView, final String semStr) {
            String[] chooseSem = new String[]
                    {
                            "1ST SEMESTER", "2ND SEMESTER", "3RD SEMESTER", "4TH SEMESTER", "5TH SEMESTER", "6TH SEMESTER", "7TH SEMESTER"
                    };

            List liststream = Arrays.asList(chooseSem);
            semAdapter = new ArrayAdapter<String>(
                    getActivity(),
                    R.layout.list_course,
                    R.id.list_course1,
                    liststream
            );
            ListView l = (ListView) rootView.findViewById(R.id.listView3);
            l.setAdapter(semAdapter);
            l.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                    String forecast = semStr + semAdapter.getItem(position);
                    Intent intent = new Intent(getActivity(), Subject.class).putExtra(Intent.EXTRA_TEXT, forecast);
                    startActivity(intent);
                    //Toast.makeText(getActivity(), forecast, Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
}