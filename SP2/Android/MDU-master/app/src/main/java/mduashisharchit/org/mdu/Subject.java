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
import android.widget.Toast;

import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.AdView;

import java.util.Arrays;
import java.util.List;


public class Subject extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_subject);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_subject, menu);
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
        ArrayAdapter<String> subAdapter;
        private static final String LOGTAG = "";
        public PlaceholderFragment() {
        }
        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {

            Intent intent = getActivity().getIntent();
            Bundle extras = intent.getExtras();
            View rootView = inflater.inflate(R.layout.fragment_subject, container, false);
            AdView mAdView = (AdView) rootView.findViewById(R.id.adView);
            AdRequest adRequest = new AdRequest.Builder().build();
            mAdView.loadAd(adRequest);

            if (intent != null && intent.hasExtra(Intent.EXTRA_TEXT)) {
                String subjectStr = intent.getStringExtra(Intent.EXTRA_TEXT);

                switch (subjectStr) {
                        case "B.techIT7TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "DATA WAREHOUSE AND DATA MINING", "SOFTWARE PROJECT MANAGEMENT",
                                            "WEB ENGINEERING", "SYSTEM AND NETWORK  ADMINISTRATION",
                                            "ADVANCED JAVA", "REAL TIME SYSTEM", "DISTRIBUTED OPERATING SYSTEM", "NETWORK SECURITY",
                                            "ADVANCED DBMS", "COMPUTER SOFTWARE TESTING", "HIGH SPEED NETWORKS"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techIT6TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "INTELLIGENT SYSTEMS", "OPERATIONS RESEARCH",
                                            "NETWORK PROGRAMMING", "PRINCIPLE OF SOFTWARE ENGINEERING",
                                            "WIRELESS COMMUNICATION", "WEB DEVELOPMENT"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techIT5TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "RAPID APPLICATION DEVELOPMENT", "SPSA", "COMPUTER NETWORKS", "COMPUTER GRAPHICS",
                                            "MICPROCESSOR AND INTERFACING", "PRINCIPLES OF OPERATING SYSTEM"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;

                        case "B.techIT4TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "MULTIMEDIA TECHNOLOGIES", "INTERNET FUNDAMENTALS", "DATABASE MANAGEMENT SYSTEM",
                                            "COMPUTER ARCHITECTURE AND ORGANISATION", "OBJECT ORIENTED PROGRAMMING", "MATHS3"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;

                        case "B.techIT3RD SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "DIGITAL ELECTRONICS", "FUNDAMENTALS OF MANAGEMENT", "DISCRETE STRUCTURES",
                                            "DATA STRUCTURES", "ENGINEERING ECONOMICS", "DIGITAL AND ANALOG COMMUNICATION"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);

                        }
                        break;
                        case "B.techIT2ND SEMESTER": {
                            String[] chooseSub = new String[]
                                    {"BASICS OF ELECTRONICS", "FUNDAMENTAL OF COMPUTER PROGRAMMING",
                                            "BASICS OF MECHANICAL ENGINEERING", "COMMUNICATION SKILLS",
                                            "MATHEMATICS2", "PHYSICS2"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techIT1ST SEMESTER": {
                            String[] chooseSub = new String[]{
                                    "ESSENTIAL OF COMMUNICATION",
                                    "MATHEMATICS1", "PHYSICS1", "ENGINEERING CHEMISTRY", "ELECTRICAL TECHNOLOGY", "ENGINEERING DRAWING", "WORKSHOP TECHNOLOGY"
                            };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;


                        case "B.techCSE7TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "ADVANCED COMPUTER ARCHITECTURE", "SOFTWARE PROJECT MANAGEMENT",
                                            "NEURAL NETWORKS", "COMPILER DESIGN",
                                            "ADVANCED JAVA", "REAL TIME SYSTEM", "DISTRIBUTED OPERATING SYSTEM", "NETWORK SECURITY",
                                            "ADVANCED DBMS", "COMPUTER SOFTWARE TESTING", "HIGH SPEED NETWORKS"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE6TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "ADA", "DIGITAL SYSTEM", "COMPUTER NETWORKS", "INTELLIGENT SYSTEMS", "PRINCIPLE OF SOFTWARE ENGINEERING", "SPSA"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE5TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "COMPUTER GRAPHICS", "THEORY OF AUTOMATA COMPUTATION", "MULTIMEDIA TECHNOLOGIES",
                                            "MICPROCESSOR AND INTERFACING", "WEB DEVELOPMENT", "PRINCIPLES OF OPERATING SYSTEM"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE4TH SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "OBJECT ORIENTED PROGRAMMING", "DATABASE MANAGEMENT SYSTEM", "INTERNET FUNDAMENTALS",
                                            "COMPUTER ARCHITECTURE AND ORGANISATION", "PROGRAMMING LANGUAGES", "FUNDAMENTALS OF MANAGEMENT"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE3RD SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "DIGITAL ELECTRONICS", "FUNDAMENTALS OF MANAGEMENT", "DISCRETE STRUCTURES",
                                            "DATA STRUCTURES", "ENGINEERING ECONOMICS", "DIGITAL AND ANALOG COMMUNICATION"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE2ND SEMESTER": {
                            String[] chooseSub = new String[]
                                    {
                                            "COMMUNICATION SKILLS", "MATHEMATICS2", "PHYSICS2", "BASICS OF ELECTRONICS", "BASICS OF MECHANICAL ENGINEERING",
                                            "FUNDAMENTAL OF COMPUTER PROGRAMMING"
                                    };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;
                        case "B.techCSE1ST SEMESTER": {
                            String[] chooseSub = new String[]{"ESSENTIAL OF COMMUNICATION",
                                    "ELECTRICAL TECHNOLOGY", "MATHEMATICS1", "PHYSICS1" , "ENGINEERING CHEMISTRY", "ENGINEERING DRAWING", "WORKSHOP TECHNOLOGY"
                            };
                            chooseSubj(chooseSub, rootView, subjectStr);
                        }
                        break;







                    case "B.techECE7TH SEMESTER": {
                        String[] chooseSub = new String[]
                                {
                                        "DATA COMMUNICATION","ADVANCED CONTROL SYSTEMS","OPTICAL COMMUNICATION SYSTEMS","DIGITAL SIGNAL PROCESSING",
                                        "FUZZZY CONTROL SYSTEM","GENETIC ALGORITHMS AND APPLICATIONS","IMAGE PROCESSING",
                                        "POWER ELECTRONICS","RADAR AND SONAR ENGINEERING ","MOBILE COMMUNICATION",
                                        "SATELLITE COMMUNICATION ENGINEERING","WIRELESS SENSOR NETWORKS","WIRELESS COMMUNICATION"
                                };

                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE6TH SEMESTER": {
                        String[] chooseSub = new String[]
                                {
                                        "MICROWAVE AND RADAR ENGINEERING","CONTROL SYSTEMS ENGINEERING","COMPUTER NETWORKS",
                                        "DIGITAL SYSTEM DESIGN","MICROCONTROLLER AND EMBEDDED SYSTEM","VLSI DESIGN"
                                };

                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE5TH SEMESTER": {
                        String[] chooseSub = new String[]
                                {
                                       "COMMUNICATION ENGINEERING","ELECTRONIC MEASUREMENT AND INSTRUMENTATION","ANALOG ELECTRONIC CIRCUITS"
                                        ,"ANTENNA AND WAVE PROPAGATION AND TV ENGINEERING","COMPUTER ARCHITECTURE AND ORGANISATION","MICROPROCESSORS AND INTERFACING",

                                };

                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE4TH SEMESTER": {
                        String[] chooseSub = new String[]
                                {
                                        "ENGINEERING ECONOMICS","SIGNALS AND SYSTEM","ANALOG ELECTRONICS",
                                        "DIGITAL ELECTRONICS","COMMUNICATION SYSTEM","ELECTROMAGNETIC FIELD THEORY"
                                };

                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE3RD SEMESTER": {
                        String[] chooseSub = new String[]
                                {
                                        "FUNDAMENTALS OF MANAGEMENT", "MATHEMATICS3","DATA STRUCTURES","ELECTRONIC DEVICES AND CIRCUITS",
                                        "NETWORK THEORY","ELECTROMECHANICAL ENERGY CONVERSION"
                                };
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE2ND SEMESTER": {
                        String[] chooseSub = new String[]{"ESSENTIAL OF COMMUNICATION",
                                "ELECTRICAL TECHNOLOGY", "MATHEMATICS2", "PHYSICS2" , "ENGINEERING CHEMISTRY", "ENGINEERING DRAWING", "WORKSHOP TECHNOLOGY"
                        };
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techECE1ST SEMESTER": {
                        String[] chooseSub = new String[]{"COMMUNICATION SKILLS", "MATHEMATICS1", "PHYSICS1", "BASICS OF ELECTRONICS", "BASICS OF MECHANICAL ENGINEERING",
                                "FUNDAMENTAL OF COMPUTER PROGRAMMING"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;







                    case "B.techMECHANICAL7TH SEMESTER": {
                        String[] chooseSub = new String[]{"STRENGTH OF MATERIAL2","REFRIGERATION AND AIR CONDITIONING","OPERTAION RESEARCH",
                        "POWER PLANT ENGINEERING","MECHANICAL VIBRATION","QUALITY ENGINEERING","FINITE ELEMENT METHODS",
                        "ENERGY MANAGEMENT PRINCIPLES","ENGINEERING DESIGN","COMPUTER INTEGRATED MANUFACTURING","MANUFACTURING MANAGEMENT",
                        "RELIABILITY ENGINEERING","SOLAR ENERGY ENGINEERING","VALUE ENGINEERING"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL6TH SEMESTER": {
                        String[] chooseSub = new String[]{"AUTOMOBILE ENGINEERING", "MECHANICAL MACHINE DESIGN2", "HEAT TRANSFER",
                                "AUTOMATIC CONTROL", "MEASUREMENT AND INSTRUMENTATION",
                                "INDUSTRIAL ENGINEERING"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL5TH SEMESTER": {
                        String[] chooseSub = new String[]{"DYNAMICS OF MACHINE","MECHANICAL MACHINE DESIGN1", "FLUID MACHINE",
                                "INTERNAL COMBUSTION ENGINES AND GAS TURBINES", "MANUFACTURING TECHNOLOGY2",
                                "APPLIED NUMERICAL TECHNIQUE AND COMPUTING"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL4TH SEMESTER": {
                        String[] chooseSub = new String[]{"ENGINEERING ECONOMICS", "MANUFACTURING TECHNOLOGY1", "KINEMATICS OF MACHINE", "STRENGTH OF MATERIALS1",
                                "FLUID MECHANICS",
                                "STEAM AND POWER GENERATION"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL3RD SEMESTER": {
                        String[] chooseSub = new String[]{"FUNDAMENTALS OF MANAGEMENT", "MATHEMATICS3","THERMODYNAMICS","COMPUTER AIDED DESIGN",
                        "ENGINEERING MECHANICS","MATERIAL SCIENCE"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL2ND SEMESTER": {
                        String[] chooseSub = new String[]{"ESSENTIAL OF COMMUNICATION",
                                "ELECTRICAL TECHNOLOGY", "MATHEMATICS2", "PHYSICS2" , "ENGINEERING CHEMISTRY", "ENGINEERING DRAWING", "WORKSHOP TECHNOLOGY"
                        };
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;
                    case "B.techMECHANICAL1ST SEMESTER": {
                        String[] chooseSub = new String[]{"COMMUNICATION SKILLS", "MATHEMATICS1", "PHYSICS1", "BASICS OF ELECTRONICS", "BASICS OF MECHANICAL ENGINEERING",
                                "FUNDAMENTAL OF COMPUTER PROGRAMMING"};
                        chooseSubj(chooseSub, rootView, subjectStr);
                    }
                    break;

                        default:

                            Toast.makeText(getActivity(), "error", Toast.LENGTH_SHORT).show();


                            break;
                    }
                }
            return rootView;
            }


        private void chooseSubj(String[] streams, View rootView, final String subjectStr) {
            List listsub = Arrays.asList(streams);
            subAdapter = new ArrayAdapter<String>(
                    getActivity(),
                    R.layout.list_course,
                    R.id.list_course1,
                    listsub
            );
            ListView l = (ListView) rootView.findViewById(R.id.listView4);
            l.setAdapter(subAdapter);
            l.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                    String forecast3 = subjectStr + subAdapter.getItem(position);

                    Intent intent = new Intent(getActivity(), Syllabus.class).putExtra(Intent.EXTRA_TEXT, forecast3);
                    startActivity(intent);

                }
            });
        }
    }
}