for i in `cat $1`; do
	echo $i;
	rm -f $i
done
	 
