import sys
from framework.vm_entity import VM
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
IP = "10.45.72.227"
#IP = TGT_PC_IP

vm_obj = VM(IP)
rpt_obj = RecoveryPoint(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()

#START, END = 1, 101
#vm_prefix = "vm-"

#vm_not_present_list = list()

#for i in range(START, END):
#  vm_name = vm_prefix + str(i)
#  if vm_name in vm_name_uuid_map:
#    print "VM: {0} - {1} already present.".format(vm_name, vm_name_uuid_map[vm_name])
#    continue
#  vm_not_present_list.append(vm_name)
#
#print " ".join(vm_not_present_list)

for vm_uuid in ['95c1b94d-6556-48f9-bca1-9c29e54deee5', 'cf89c31e-6374-4370-88cd-3c98c5fd4671', 'a666d6b9-44d3-42c8-8a9b-bd08ae8afb03', '6cb8055a-55a5-41ce-b421-a6b4446d6514', 'c12d3c07-a3d9-449e-9e55-c96cb92ec915', '9e4cbf53-0fea-433d-8f77-35be698e0813', 'e84261e3-7177-40de-aaef-e7179872d51b', 'c18e2791-86b4-41fd-b8bc-30d3c36b702d', '7ae2e839-87d3-41c9-9713-69c948b082be', 'e7c01c5b-e168-4d4d-80b1-35fd0ec7d924', '1a501ac5-4315-4978-bcc6-70836a363b68', '5542a513-385c-43b3-8536-eeb483e48fe8', '2f8f8a7b-53d4-43d6-97b9-fbbedc5f37b7', 'cc744c1c-48db-403a-8b48-cefa76f51e3a', '892b612b-c8e6-4872-be4b-730071b9cca8', 'cbf8e087-ced9-457a-8dfd-85eaa6348b74', '4884eca2-6cc9-45bc-946f-d302752a9239', 'b92ce643-7b5a-4f5f-a487-9b4736fcebb2', '18ca1087-3d36-4cb0-b85f-97fe1a4038d7', '3d23b8ee-ae73-4e1a-af6a-d9752c5a9ace', 'e1b17e46-af7c-4049-93a4-51fd810acb11', 'a954db1c-04d6-4cf1-b4f7-c021600dc15a', '1df54e2b-869e-491b-b9c3-c0563517c2ea', 'eb9ea90d-7cfe-4d68-9b6e-8ef181b27fce', '102b1d75-923f-49d2-981d-1c72a6991a69', '187391fd-8b99-4470-b09e-101d3013b656', '10e5613b-d62e-4581-9b65-34339f2d4a10', 'b52a1ddf-f695-487c-8860-06e3b8ad85dc', '556986dd-69a2-4240-9600-3c5840d9f49d', 'acc3f888-4342-4f85-9b25-911c0557860f', '3cc39faa-6061-433f-92de-10c3c8f57444', '335531ac-0624-439f-a907-c68bb85ef098', 'c1bd2167-cee9-471b-a7a5-97d4217fb692', 'a2ec4b99-e25d-4e1a-8814-36261cd9d0ed', 'd560addd-7df3-41c3-8df7-0da1782dbbdb', '18865a4c-d1a4-4860-9082-77001fb31081', '69f28b75-b708-47e1-bbca-796feda3769a', '71234afc-99db-49ba-bf23-3fd7439351e6', '70a6dc62-aa29-4e07-99e5-075e97159969', '964abf0d-82e5-40ae-a886-7a2364b7f1ae', '900dc50e-f8da-47e4-b14b-2e6e45818732', 'd73bf51e-d8d4-4194-94fb-afa56f910508', '084a669a-e5a1-4006-b843-b6e7a15b0640', '3131988f-1814-4144-b426-c292dcbc297c', '3306be6e-1a87-428d-ac3c-37aa8ac7b49b', '73c76761-1e4f-4cff-95d2-e70a5c1b5442', '133de6fd-c4dd-4ff7-a574-d35a1ac34938', 'deadec1b-08a8-4a51-b876-e4304ff92226', 'dec10927-373d-40fc-af50-c9459569dd7b', 'ab61511c-c0fe-4580-a4aa-864ac0c6c3c6', '48f96ff1-5981-4d50-8373-78d333038185', '718eb46f-c740-4ceb-9d77-1d1e8fb4c46c', 'eb9f4546-5f45-4c8a-b2dd-003c7f3ad06f', 'ff6ded3f-6bbe-4c94-875d-33dd77ff476d', '9bfd7077-0a74-43ca-84f6-92d1fa49d489', 'bc851177-c306-4d1f-af43-d616f727f41f', 'aa362763-9728-4bd8-8257-5640c3ece0f6', '5db2896a-975f-4993-9ce4-3a8df1716fcf', '7ba19542-2096-410b-b6ea-98a513b02644', 'f9bd4fbb-223c-48ab-a6ba-c9f722bd69f9', '25c9834b-9a65-4656-b5e8-3c7e140201c1', '8f11a276-6586-4659-8265-3d0ae3d9714a', '128c1acf-654a-4536-8edf-c89e95865426', 'ffc0cd1e-dc88-4376-9822-320d0aaa9a40', 'd99c9f84-e41f-4b5c-aa7b-45a2f2fb8c3c', 'a74b5c02-bdad-4010-9116-84326a5ea928', '00ece9eb-abec-4256-afe8-9bb2e8008381', '3e98b0c7-ebaa-4231-b6f4-62616dc87c61', '50dc7d4a-5dbb-4117-89e0-4cb1eb061d02', '16cbb6b5-8b2f-4835-a03d-1e0e4b6b57dd', 'c429594c-2882-40a1-95d7-6c8fc87bb9cf', 'ccee526f-2902-40bd-af91-deac33a7bd65', '583c963c-0dc0-4b34-adc5-305c00affa98', 'c381382d-66ae-454a-ab0c-fd4679b5fd0a', '9bd7ce45-a98f-4f43-b07d-4b4dd2567ed1', '40d1a77f-8538-4aa1-90b2-7bd83a057e03', '75a1f615-a33b-466a-a578-8b8cafd57ccb', '929679e8-b090-4f66-95db-bf985a9b83ba', '26e6483d-ebb4-4504-bf79-f0d7f8c7b4a8', '6bd21eef-40d1-4fd4-b191-85afa21e33f3', 'bbe21eea-82a3-4871-b9bc-2d8d644a848e', '79a274ca-7e62-47af-9241-1db52bafd196', '08b8844a-c4d9-4e63-86a3-7e70efacb07f', '9122f627-c430-4948-9333-8a6effb1bcad', '01401044-8e89-4c47-b786-b70953172187', '610b689d-09fe-4124-8d9b-c0deae206c1f', 'ebdd3f56-c9eb-4ec7-ac04-4929d559fe9d', 'e4a33a4c-b630-449f-9f39-33068894da32', '82d5e37f-3bdb-43e3-9172-4df03c0efc35', '18805baf-e3ee-4c40-af58-726f8e1af01d', 'a746d617-70a5-4514-b025-799d63990402', '72d6e437-fba6-40d2-83e9-da204e683d4b', '4bc15fad-ee81-4b52-b228-cfe08af9f707', '5be8a723-9520-4da6-a9c0-aa085174d41e', '9b9b32ba-9f45-4d83-9051-f5ebde3acc73', '02c7c920-9720-4bb5-8363-7d6834e0dd58', '90c59ee5-8a01-45c3-a01c-5637832bf4b3', 'e1089ba1-79b2-424f-908c-517da8e06ba7', '6b582c79-134d-450b-b386-bb7de9559624', '5be33baf-4ddd-4b21-9697-a58786611e1c']:


  filter_criteria = {
    "entity_type":"recovery_point",
    "group_member_sort_attribute": "_created_timestamp_usecs_",
    "group_member_sort_order": "DESCENDING",
    "group_member_attributes": 
    [
      {
        "attribute": "_created_timestamp_usecs_"
      }
    ],
    "filter_criteria":"vm_live_entity_uuid_list=={0}".format(vm_uuid)
  }
  #print filter_criteria
  out = rpt_obj.get_groups_response(filter_criteria)
  rpt_uuid_list = list()
  if out["filtered_group_count"] > 0:
    rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
    print "\nFound RecoveryPoints on Source: {0}".format(IP)
  print "\nLatest Recovery Point: {0}".format(rpt_uuid_list[0])
  src_rpt_obj = rpt_obj.get(rpt_uuid_list[0], get_vm_vg_details=False)
  print "Restoring Recovery Point"
  src_rpt_obj.restore_rec_point() 
