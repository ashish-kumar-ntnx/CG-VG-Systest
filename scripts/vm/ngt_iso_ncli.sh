for i in {1..100}; do id=`ncli vm list name=vm-$i |grep "Id                        :" |awk '{print $3}'`; echo "Mounting NGT Iso on vm-$i"; ncli ngt mount vm-id=$id; done

#for i in $(eval echo "{$1..$2}")
#do
#        id=`ncli vm list name=vm-$i |grep "Id                        :" |awk '{print $3}'`
#        echo "Mounting NGT Iso on vm-$i"
#        ncli ngt mount vm-id=$id
#done
