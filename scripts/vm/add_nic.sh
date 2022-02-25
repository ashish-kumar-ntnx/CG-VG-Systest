for i in {1..100}
do
nic_count=`acli vm.nic_list vm-$i | wc -l`
#echo $nic_count
if [ $nic_count == 1 ]
  then
  echo "#### Adding NIC to vm-$i ####"
  acli vm.nic_create vm-$i network=vlan0
fi

done
