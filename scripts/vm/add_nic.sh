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

# remove _clone suffix from vm name
#for i in `acli vm.list |grep clone | awk '{print $1}' | xargs`; do acli vm.update $i name=${i/_clone/}; done

#for i in `acli vm.list | grep vdi | awk '{print $1}' |xargs`
#do
#nic_count=`acli vm.nic_list $i | wc -l`
##echo $nic_count
#if [ $nic_count == 1 ]
#  then
#  echo "#### Adding NIC to $i ####"
#  acli vm.nic_create $i network=vlan0
#fi
#
#done


#for i in `acli vg.list |grep vdi | awk '{print $2}' | xargs`; do iqn=`acli vg.get $i |grep external_initiator_name | awk '{print $2}' |xargs`; echo "Detaching iqn from $i" ;acli vg.detach_external $i initiator_name=$iqn; done
