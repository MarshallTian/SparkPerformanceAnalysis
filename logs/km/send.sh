for slave in `cat slaves`
do
	WORK_DIR=`pwd`
#	ssh $slave "mkdir /home/L/monitor/"
#	scp *.rpm $slave:/home/L/monitor/
	#ssh $slave "cd $WORK_DIR; rpm -ivh sysstat*.rpm"
	str="\`killall free\`"
	str1="\`killall iostat\`"
	echo $str
	echo $str1
	#scp change.sh $slave:$WORK_DIR/ 
	#ssh $slave "cd $WORK_DIR; sh change.sh"
	ssh $slave "killall iostat"
done
