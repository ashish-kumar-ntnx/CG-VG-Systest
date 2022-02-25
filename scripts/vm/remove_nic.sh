for i in {1..100}
do
echo "Removing nic from vm-$i"
for j in `acli vm.nic_get vm-$i | grep mac_addr | awk '{print $2}' | xargs`
  do
  echo "deleting nic with mac_addr $j"
  acli vm.nic_delete vm-$i $j
  done
done
