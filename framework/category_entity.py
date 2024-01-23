from lib import *
from framework.const import V4_API_VERSION, CAT_API_VERSION

class Category(object):
  def __init__(self, pc_ip, uuid=None, cat_key=None, cat_val=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.cat_key = cat_key
    self.cat_val = cat_val

  def create(self, cat_key, cat_val, description=None):
    url = "api/prism/{0}/config/categories".format(CAT_API_VERSION)
    cat_key_dict = dict()
    cat_key_dict["key"] = cat_key
    cat_key_dict["value"] = cat_val
    if description:
      cat_key_dict["description"] = cat_key
    #print url, cat_key_dict
    r = send_request("POST", self.pc_ip, url, json=cat_key_dict)
    #print r.status_code, r.text
    out = r.json()
    print out
    #parentExtId = out["data"]["extId"]
    #cat_val_dict = {"parentExtId": parentExtId, "name": cat_val}
    #r = send_request("POST", self.pc_ip, url, json=cat_val_dict)
    #print r.status_code, r.text
    #out = r.json()
    #out = r.json()
    extId = out["data"]["extId"]
    c = Category(self.pc_ip, uuid=extId, cat_key=cat_key, cat_val=cat_val)
    return c

  def add_value(self):
    pass

  def get(self, cat_key=None, cat_val=None, cat_uuid=None):
    if cat_uuid:
      url = "api/prism/{0}/config/categories/{1}".format(CAT_API_VERSION, cat_uuid)
      r = send_request("GET", self.pc_ip, url)
      out = r.json()
      if out["$dataItemDiscriminator"] == "EMPTY_LIST":
        print "category: {0} not found".format(cat_uuid)
        return
      fq_name = out["data"]["fqName"]
      fq_name = fq_name.split("/")
      cat_key = fq_name[0]
      cat_val = fq_name[1]
    else:
      #url = "api/prism/{0}/config/categories?type=USER,SYSTEM,INTERNAL&fqName={1}/{2}".format(CAT_API_VERSION, cat_key, cat_val)
      #r = send_request("GET", self.pc_ip, url)
      #out = r.json()
      ##print out
      #if out["$dataItemDiscriminator"] == "EMPTY_LIST":
      #  print "Category not found."
      #  return
      #for i in out["data"]:
      #  if i["fqName"] == "{0}/{1}".format(cat_key, cat_val):
      #    cat_uuid = i["extId"]
      #url = "api/prism/{0}/config/categories?$page=0&$filter=(fqName eq '{1}/{2}')".format(CAT_API_VERSION, cat_key, cat_val)
      url = "api/prism/{0}/config/categories?$filter=(key eq '{1}') and (value eq '{2}')".format(CAT_API_VERSION, cat_key, cat_val)
      r = send_request("GET", self.pc_ip, url)
      out = r.json()
      #print out
      #if out["$dataItemDiscriminator"] == "EMPTY_LIST":
      if out["metadata"]["totalAvailableResults"] == 0:
        print "Category not found."
        return
      cat_uuid = out["data"][0]["extId"]
    c = Category(self.pc_ip, uuid=cat_uuid, cat_key=cat_key, cat_val=cat_val)
    return c

  def get_key_uuid_map(self):
    cat_key_uuid_map = dict()
    category_list = self.list_all()
    for i in category_list:
      cat_key_uuid_map[i["cat_key"]] =  i["uuid"]
    return cat_key_uuid_map

  def remove(self):
    pass

  def list_all(self):
    category_list = list()
    url = "api/prism/{0}/config/categories?type=USER,SYSTEM,INTERNAL".format(CAT_API_VERSION)
    r = send_request("GET", self.pc_ip, url)
    out = r.json()
    print "---- 1 ----"
    print out
    for i in out["data"]:
      cat_key = i["key"]
      #cat_key = i["name"]
      #url = "api/prism/{0}/config/categories/{1}?$view=SUMMARY".format(CAT_API_VERSION, i["extId"])
      url = "api/prism/{0}/config/categories?parentExtId={1}".format(CAT_API_VERSION, i["extId"])
      r = send_request("GET", self.pc_ip, url)
      out = r.json()
      print "---- 2 ----"
      print out
      if out["metadata"]["totalAvailableResults"] == 0:
        continue
      for i in out["data"]:
        print "---- 3 ----"
        print i
        #cat_val = i["name"]
        cat_val = i["value"]
        uuid = i["extId"]
        category_list.append({"cat_key": cat_key, "cat_val": cat_val, "uuid": uuid})
    return category_list

  def get_value(self):
    pass

  def get_entities(self):
    vm_list, vg_list = list(), list()
    url = "api/prism/{1}/config/categories/{1}/entityReferences".format(CAT_API_VERSION, self.uuid)    
    r = send_request("GET", self.pc_ip, url)
    out = r.json()
    #print out
    for i in out["data"]:
      if i["entityType"] == "VM":
        for j in i["entityReferences"]:
          vm_list.append(j["entityId"])
      if i["entityType"] == "VOLUMEGROUP":
        for j in i["entityReferences"]:
          vg_list.append(j["entityId"])
    return vm_list, vg_list

