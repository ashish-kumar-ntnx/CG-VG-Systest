from tinydb import TinyDB, Query
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass

AUTH = ("admin", "Nutanix.123")
PC_IP = "10.45.72.242"
VG_DB = TinyDB("../db/vg.json")
CAT_DB = TinyDB("../db/category.json")

url = "https://{0}:9440/api/storage/v4.0.a1/config/volume-groups".format(PC_IP)


vg_num_a = 1
vg_num_b = 1

vg_category_list = list()

for i in range(1, 21):
  tmp = dict()
  cat_key = "cat-" + str(i)
  cat_val = "val-" + str(i)
  q = Query()
  cat_uuid = CAT_DB.search(q.cat_key == cat_key)[0]["uuid"]
  tmp["cat_key"] = cat_key
  tmp["cat_val"] = cat_val
  tmp["cat_uuid"] = cat_uuid
  tmp["vg_list"] = list()
  if i <= 10:
    vg_prefix = "vg-a-"
    for _ in range(10):
      vg_name_1 = vg_prefix + str(vg_num_a)
      vg_name_2 = vg_prefix + str(vg_num_a + 100)
      vg_num_a += 1
      q = Query()
      vg_uuid_1 = VG_DB.search(q.name == vg_name_1)[0]["uuid"]
      vg_uuid_2 = VG_DB.search(q.name == vg_name_2)[0]["uuid"]
      tmp["vg_list"].append({vg_name_1: vg_uuid_1})
      tmp["vg_list"].append({vg_name_2: vg_uuid_2})
  else:
    vg_prefix = "vg-b-"
    for _ in range(10):
      vg_name_1 = vg_prefix + str(vg_num_b)
      vg_name_2 = vg_prefix + str(vg_num_b + 100)
      vg_num_b += 1
      q = Query()
      vg_uuid_1 = VG_DB.search(q.name == vg_name_1)[0]["uuid"]
      vg_uuid_2 = VG_DB.search(q.name == vg_name_2)[0]["uuid"]
      tmp["vg_list"].append({vg_name_1: vg_uuid_1})
      tmp["vg_list"].append({vg_name_2: vg_uuid_2})
  vg_category_list.append(tmp)

for i in vg_category_list:
  failed_category_apply = list()
  cat_key = i["cat_key"]
  cat_val = i["cat_val"]
  cat_uuid = i["cat_uuid"]
  for j in i["vg_list"]:
    vg_name = j.keys()[0]
    vg_uuid = j.values()[0]
    url = "https://{0}:9440/api//storage/v4.0.a1/config/volume-groups/{1}/category-associations".format(PC_IP, vg_uuid)
    r = requests.get(url, auth=AUTH, verify=False)
    out = r.json()
    cat_already_applied =False
    if out["$dataItemDiscriminator"] != "EMPTY_LIST":
      for k in out["data"]:
        if k["extId"] == cat_uuid:
          cat_already_applied = True
          print "Category: ({0}: {1})({2}) to VG: {3}({4}) already applied to VG.".format(cat_key, cat_val, cat_uuid, vg_name, vg_uuid)

    if not cat_already_applied:
      print "Adding category: ({0}: {1})({2}) to VG: {3}({4})".format(cat_key, cat_val, cat_uuid, vg_name, vg_uuid)
      url = "https://{0}:9440/api//storage/v4.0.a1/config/volume-groups/{1}/$actions/associate-category".format(PC_IP, vg_uuid)
      spec = {"categories": [{"entityType": "CATEGORY","extId":"{0}".format(cat_uuid)}]}
      r = requests.post(url, auth=AUTH, json=spec, verify=False)
      url = "https://{0}:9440/api//storage/v4.0.a1/config/volume-groups/{1}/category-associations".format(PC_IP, vg_uuid)
      r = requests.get(url, auth=AUTH, verify=False)
      out = r.json()
      cat_already_applied =False
      if out["$dataItemDiscriminator"] != "EMPTY_LIST":
        for k in out["data"]:
          if k["extId"] == cat_uuid:
            cat_already_applied = True
            print "Category: ({0}: {1})({2}) successfully applied to VG: {3}({4}).".format(cat_key, cat_val, cat_uuid, vg_name, vg_uuid)
      if not cat_already_applied:
        failed_category_apply.append({"cat_key": cat_key, "cat_val": cat_val, "cat_uuid": cat_uuid, "vg_name": vg_name, "vg_uuid": vg_uuid}) 
    print "\n"
print failed_category_apply
