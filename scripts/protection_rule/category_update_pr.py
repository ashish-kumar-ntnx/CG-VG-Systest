import sys
from framework.protection_rule_entity import ProtectionRule
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
IP = SRC_PC_IP
pr = ProtectionRule(IP)
"""
pr_category_list = [
  {
    "pr_name": "pr-1-a1-to-b1",
    "cat_list": [
      {"cat-1": "val-1"},
      {"cat-2": "val-2"},
      {"cat-3": "val-3"},
      {"cat-4": "val-4"},
      {"cat-5": "val-5"}
    ]
  },
  {
    "pr_name": "pr-2-a1-to-b1",
    "cat_list": [
      {"cat-6": "val-6"},
      {"cat-7": "val-7"},
      {"cat-8": "val-8"},
      {"cat-9": "val-9"},
      {"cat-10": "val-10"}
    ]
  },
  {
    "pr_name": "pr-3-a2-to-b2",
    "cat_list": [
      {"cat-11": "val-11"},
      {"cat-12": "val-12"},
      {"cat-13": "val-13"},
      {"cat-14": "val-14"},
      {"cat-15": "val-15"}
    ]
  },
  {
    "pr_name": "pr-4-a2-to-b2",
    "cat_list": [
      {"cat-16": "val-16"}, 
      {"cat-17": "val-17"}, 
      {"cat-18": "val-18"}, 
      {"cat-19": "val-19"},
      {"cat-20": "val-20"}
    ]
  }
]
exclude_pr_list = ["pr-3-a2-to-b2", "pr-4-a2-to-b2"]
"""
#cat_prefix = "self-az-cat-"
cat_prefix = "cat-"

pr_category_list = [
  {
    "pr_name": "pr-1",
    "cat_list": [
      {"{0}1".format(cat_prefix): "val-1"}
    ]
  },
  {
    "pr_name": "pr-2",
    "cat_list": [
      {"{0}2".format(cat_prefix): "val-2"}
    ]
  },
  {
    "pr_name": "pr-3",
    "cat_list": [
      {"{0}3".format(cat_prefix): "val-3"}
    ]
  },
  {
    "pr_name": "pr-4",
    "cat_list": [
      {"{0}4".format(cat_prefix): "val-4"}
    ]
  },
  {
    "pr_name": "pr-5",
    "cat_list": [
      {"{0}5".format(cat_prefix): "val-5"}
    ]
  },
  {
    "pr_name": "pr-6",
    "cat_list": [
      {"{0}6".format(cat_prefix): "val-6"}
    ]
  },
  {
    "pr_name": "pr-7",
    "cat_list": [
      {"{0}7".format(cat_prefix): "val-7"}
    ]
  },
  {
    "pr_name": "pr-8",
    "cat_list": [
      {"{0}8".format(cat_prefix): "val-8"}
    ]
  },
  {
    "pr_name": "pr-9",
    "cat_list": [
      {"{0}9".format(cat_prefix): "val-9"}
    ]
  },
  {
    "pr_name": "pr-10",
    "cat_list": [
      {"{0}10".format(cat_prefix): "val-10"}
    ]
  }
]
exclude_pr_list = []


if len(sys.argv) != 2:
  print "\n\tUsage: category_update_pr.py <remove/add>\n"
  sys.exit(1)
op = sys.argv[1]
for i in pr_category_list:
  pr_name = i["pr_name"]
  if pr_name in exclude_pr_list:
    continue
  cat_list = i["cat_list"]
  pr_obj = pr.get(pr_name=pr_name)
  spec = pr_obj.spec
  #print spec["spec"]["resources"]["category_filter"]
  spec.pop("status")
  if op == "remove":
    print "Removing categories from PR: {0} - {1}".format(pr_name, pr_obj.uuid)
    spec["spec"]["resources"]["category_filter"]["params"] = {}
  if op == "add":
    category_param = dict()
    for cat in cat_list:
      category_param[cat.keys()[0]] = cat.values()
    print "Adding categories to PR: {0} - {1}".format(pr_name, pr_obj.uuid)
    spec["spec"]["resources"]["category_filter"]["params"] = category_param
  pr_obj.update(spec)
