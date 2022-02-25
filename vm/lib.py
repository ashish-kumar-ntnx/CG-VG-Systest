from tinydb import TinyDB, Query

image_db = TinyDB("../db/image.json")
ctr_db = TinyDB("../db/ctr.json")
cluster_db = TinyDB("../db/cluster.json")
category_db = TinyDB("../db/category.json")
subnet_db = TinyDB("../db/subnet.json")
vm_small_db = TinyDB("../db/vm_small_spec.json")
cg_db = TinyDB("../db/cg.json")

def get_ctr_id(spec):
  q = Query()
  return ctr_db.search((q.name == spec["ctr"]) & (q.cluster_name == spec["cluster"]))[0]["uuid"]

def get_image_id(spec):
  q = Query()
  return image_db.search(q.name == spec["image"])[0]["uuid"]

def get_cluster_id(spec):
  q = Query()
  return cluster_db.search(q.name == spec["cluster"])[0]["uuid"]

def get_subnet_id(spec):
  q = Query()
  return subnet_db.search((q.name == spec["nic"]) & (q.cluster_name == spec["cluster"]))[0]["uuid"]

def get_category_id(spec):
  q = Query()
  return category_db.search((q.cat_key == spec["cat_key"]) & (q.cat_val == spec["cat_val"]))[0]["uuid"]

#def get_cg_id(spec):
#  q = Query()
#  return category_db.search((q.cat_key == spec["cat_key"]) & (q.cat_val == spec["cat_val"]))[0]["uuid"]

class GetIds:
  def __init__(self, spec):
    self.ctr_id = get_ctr_id(spec)
    self.image_id = get_image_id(spec)
    self.cluster_id = get_cluster_id(spec)
    self.subnet_id = get_subnet_id(spec)
    self.category_id = get_category_id(spec)

if __name__=="__main__":
  spec = {"name": "vm-52", "ctr": "cg-vg-ctr-6", "nic": "vlan0", "image": "rhel_73", "disk_size_bytes": 5368709120, "cluster": "PC-A-PE-1", "cat_val": "val-6", "cat_key": "cat-6"}
  print "ctr_id: {0}".format(get_ctr_id(spec))
  print "image_id: {0}".format(get_image_id(spec))
  print "cluster_id: {0}".format(get_cluster_id(spec))
  print "subnet_id: {0}".format(get_subnet_id(spec))
  print "category_id: {0}".format(get_category_id(spec))
  d = GetIds(spec)
  print d.__dict__
