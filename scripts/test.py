from framework.vm_entity import VM
v = VM("10.45.72.242")
v1 = v.get(vm_name="vm-24", cluster_name="PC-A-PE-1")
print v1.cluster_name
