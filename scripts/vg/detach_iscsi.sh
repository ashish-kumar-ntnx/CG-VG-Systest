for i in {1..200}; do iqn=`acli vg.get vg-a-$i |grep external_initiator_name | awk '{print $2}' |xargs`; echo "Detaching iqn from vg-a-$i" ;acli vg.detach_external vg-a-$i initiator_name=$iqn; done
