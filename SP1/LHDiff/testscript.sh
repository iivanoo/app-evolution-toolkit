#!/bin/bash
outaddress='./result.csv'
inputaddress='./test.csv'
OLDFILE='./old'
num2=1
while IFS=, read col1 col2 col3 col4 col5 col6 col7 col8
do
     echo "$col1"    #repo name column
     echo "$col2"    #commit id
     echo "$col6"    #filename
     echo "$col7"    #line number
     num=$(($col7+$num2))
     echo "$num"
     pushd "./$col1"
     git reset --hard $col2    # reset the repository at each commit
     popd
     NEWFILE=./$col1/$col6    # copy the address of new file (lhdiff parameter)
     abc=$(java -jar ./lhdiff.jar -ob $OLDFILE $NEWFILE | sed -n "$num"p | tr -d ,)    #running the lhdiff tool and extracting the performance issue line as output.
     if [ $? -eq 0 ]; then
     	#abc=$(cat $tool_output | sed -n "$num"p | tr -d ,)
     	echo "$col1,$col2,$col3,$col5,$col6,$col7,$abc" >> $outaddress    #saving the output in a csv file
     	echo "$abc"
     	#rm $OLDFILE
     	#rm $out/"old"
     	#mv $NEWFILE $out/"old"
     	#OLDFILE=$out/"old"
     else
     	echo "$col1,$col2,$col3,$col5,$col6,$col7,DeletedOrMoved" >> $outaddress
     	#mv $NEWFILE $out/"old"
     	#OLDFILE=$out/"old"
     fi
     
	#if [ -f "$FILE" ]
	#then
	#	echo "yes"
	#else
	#	echo "no"
	#fi
done < "$inputaddress"