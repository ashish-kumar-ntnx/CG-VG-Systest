j=0;for i in {1..20}; do for k in {1..3}; do acli vm.update vm-$((j+k)) memory=2G; done; j=$((j+10)); done
