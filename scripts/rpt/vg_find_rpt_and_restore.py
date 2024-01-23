import sys
from framework.vm_entity import VM
from framework.lib import *
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
#IP = TGT_PC_IP

vg_name = sys.argv[1]
source_cluster_uuid = "0005dab7-18a3-8a23-7e83-0cc47a9b0a8c"

spec = {"entity_type":"volume_group_recovery_point","group_member_sort_attribute":"creation_time_usecs","group_member_sort_order":"ASCENDING","group_member_attributes":[{"attribute": "top_level_recovery_point_uuid"}, {"attribute":"source_cluster_uuid"},{"attribute":"creation_time_usecs"}],"filter_criteria":"source_cluster_uuid=={0};volume_group_name==.*{1}.*".format(source_cluster_uuid ,vg_name)}

print spec

url = "api/nutanix/v3/groups"

r = send_request("POST", IP, url, json=spec)
out = r.json()

if out["filtered_entity_count"] == 0:
  print "No recovery point found for VG: {0} on cluster: {1}".format(vg_name, source_cluster_uuid)
else:
  rpt_uuid = out["group_results"][0]["entity_results"][0]["data"][0]["values"][0]["values"][0]
  url = "api/dataprotection/v4.0.a2/config/recovery-points/{0}/volume-group-recovery-points".format(rpt_uuid)
  r = send_request("GET", IP, url)
  out = r.json()
  vg_rpt_uuid = out["data"][0]["extId"]
  print "For VG: {0} on cluster: {1} vg_rpt: {2}, top_level_rpt: {3}".format(vg_name, source_cluster_uuid, vg_rpt_uuid, rpt_uuid)


url = "api/dataprotection/v4.0.a2/config/recovery-points/{0}/volume-group-recovery-points/{1}/$actions/restore".format(rpt_uuid, vg_rpt_uuid)
#url = "api/dataprotection/v4.0.a2/config/recovery-points/{0}/$actions/restore".format(rpt_uuid)

print "Restoring VG: {0}".format(vg_name)
r = send_request("POST", IP, url, json={})
print r.status_code

"""
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

for vg_uuid in ['8de65b96-3eed-47e0-a708-c4d2913a74dd', '84be13fc-8560-4c31-8c1a-0f5e553927a0', '7ff7b1d8-2837-40cb-a5be-4ac0e6e62e1f', '191b9b31-c3b5-40b1-b94d-788da91cca3e', '43704abb-77c1-437f-af0d-b250eac25718', '61660342-8316-48f5-bdf0-ea9afeb99452', 'd874e1b5-d5b1-458d-bde2-c74963901624', '952b8265-3ece-4395-aeb4-60d432327267', '4b136fe2-130f-4e61-bce6-f35a87d920f3', '36a0e80b-0bcc-4525-9b0c-6a7945c3f424', '2da49aee-1056-4ca9-9a8f-a3c4df957cf3', 'e5339a30-3265-4e63-b357-a5e2f8c6ec47', 'd0d26965-0e16-493f-8b4c-be44db4a1251', '23d46d5a-5c7d-4300-b287-4857c5ea4047', '4c18ebb9-8841-4983-89b5-2bb9809dc8e1', 'c04e4881-783d-4c14-a6e0-98b75b853a92', '48eaae74-2dff-4986-8d29-c73884f42adf', '1f846389-dcd8-4a51-a006-0d79e0ca2d5b', 'fd09b520-f1f8-4626-bb13-7a1021718ab6', 'd9f9ec0d-4124-4483-9e33-92651c894463', '9dae9cf6-2142-44cd-8526-71918d908b73', '1ab48fbd-9e36-4163-af58-81ae03effe6e', 'f8fd13ec-b327-45a2-b5ce-443cc24b6dbe', '630b8b3d-ec00-49ea-9b9f-30c99830ce40', 'bbb20db7-49d2-4286-9428-23e32892599a', '97b44046-5e6f-4d81-bdf5-08a5c2a11f55', '37fbf907-5c18-4138-8bb3-dfbbbb3af64f', 'bf5e8ed1-33ed-4761-81ca-735c3c7d960c', '0791f423-ce31-4a2c-b81e-9f6d9061eb0f', '19f4253e-cf65-4744-997a-ae0dc6ef0fce', '4a6f54a3-dd26-4211-9a7a-236d4ad92703', 'c050d323-be77-46c0-be4c-1dad4ec97c93', '3f572b22-0f3f-4da4-8f1a-a52aa5b2f2b5', '8a77bbdb-6138-4391-802c-982ea057c61e', '32f07941-4660-4658-aa59-af5abea7b911', '62dc0060-7942-49dd-86be-55b313ef5ccb', 'd7ea67d3-d62d-451d-a4d5-6f1ac7a9fba3', '7e50ac36-384d-4a13-bfb1-967d6f5e2406', '4c4f9eb3-003e-4f72-abf4-07e4d2e8c1b3', '94766aed-4e96-4f8b-a0cf-8fd3d15e665e', 'fc06b78a-a35f-429e-aff5-316fee38552d', '90ee80dd-5002-4d8a-aaea-fa986573d870', '73f513e8-46d4-4b33-8ad9-b289bcabc0d8', '54cffb29-54fc-4166-ac15-b65bc93d605f', 'ce356b4a-287e-454c-8849-a18ba8de1676', '0bea64b6-bf92-4490-904b-74df6c7530e8', 'f5859e0b-ec40-47c1-b2d0-e000aeb13ab1', 'e9ac00b8-4871-4c7e-8f72-80efdc1736c9', 'aa98bb90-8ae7-48f3-a9dc-8bc1c93ef3fd', '0f2a4d91-3e0c-4e5e-822c-74c3e1fa71e0', 'ca69da06-ee00-4e20-bfa1-500c267901e4', 'fabde005-78ce-4521-97dd-539316d5608e', '7a245e3c-fc55-4f0f-a613-82104cb860aa', '293ce97f-c87a-4c9b-aa57-06b85c4235c4', '7ed1ec18-379c-4f91-bbae-b5c908926c8c', '81c02dd7-75e0-45ed-8620-af4ae617a876', '0e6bed5c-b231-4fdf-8c9e-1534b93e534d', '98883900-fe49-49b4-a71c-9fc08837faaf', '4c7f7881-6f44-41e5-9d7b-97a4b8ad9ccd', '96caa4ea-9027-42da-8a5d-5ada4545ec87', '2b78477e-21df-41b2-8bce-3dabdf1c723f', '690a2eaa-8bba-4464-a6e6-6c5d19b94219', '90598dce-ecb2-44ae-b31f-a65962510703', '0a766f63-34ff-47c9-9f38-7fef067cb46a', 'd2126dc0-32a0-4703-a834-100389e357d7', '7b36bb54-4dc9-4403-a4b2-64e98d4a560d', 'fbc2ac24-31c9-4885-9653-d4ccca759d82', '89c7a3fc-724e-4393-9ac1-a48bfa8d6b5f', '315a7d00-3652-4376-8d69-9fa19e144aec', '6f29aeab-3aa9-4dc9-aea0-65bdf2e0b04d', '1c375b98-3671-44e5-b07f-911e5d5e329f', '74836e10-ca9a-453c-9730-3875867e231e', '8677543d-e498-49f7-8bfd-8429427e2df7', 'fe7e6160-a280-453b-a5b3-7059990ab828', '1c743eea-c564-4dc2-bd54-7faee21d30a9', 'c5191f5c-b095-45f0-98ea-f78c656b01ce', 'cab1d343-0f52-4f9e-bbad-18bc06376c46', '33456242-b9cb-4605-a9a8-b943d72620af', '53606bd8-ee67-46a4-b8ce-40a144c21d03', 'd6cabc68-51a8-468b-b6d2-bafc4e8dfbdd', 'd3b12307-cf9d-4e15-a92b-dd9a00bfc383', '032960ba-909e-447e-8116-bdcfbefb8b29', 'bc9a5e7e-d5bc-4acf-bd78-390c19282c1f', 'c2d851d1-0aed-4d2d-b919-3823c1370e34', 'a1d2ab69-03e0-4c55-8349-6eeb817b3af1', 'e726711e-57cc-460b-a119-61dcec447571', '37f112fb-87ca-47d7-b62c-9142662049f7', '72f90ff1-5e3a-4dfc-acef-e597947242af', 'bf503d12-10b4-4fe2-a1d7-67f8e92c0b14', '94f1fd3f-5523-4147-b74d-db6efbcdeebe', 'a1981909-b36b-4afa-9eb9-9ccdce8b96d3', '6088970f-c688-4ce6-8cde-752b3e3f3e1b', 'e1c98c65-a61c-4212-a6e2-55e29b212290', '0c8429a4-571a-41c4-90d4-16533cef5d6e', '34b6f49a-4402-4756-9aed-4886aa5b8c44', '0fc67d68-45de-4297-aea7-a9f270949d52', '8752c17d-2418-4f16-a6d6-0289de58d911', 'a530e780-b881-41b6-9ccc-01c9bd325ff2', 'cd51b4cd-5a56-463c-adbb-db1ea1e8fcd7', 'e130fa02-3482-48b8-9194-37da089c3737', '4acd1304-84b8-4d0e-8a16-8482ecfd1be8', '2c335d80-53a3-4807-af4a-58f12d3f39a5', 'ec4018d7-066e-4de8-9742-9b08feee96e9', '1c92c9da-a3dc-4646-b8b5-9b0304ac6330', '301330bc-99ab-44f3-a419-b5eedc165630', '8d68d367-072d-41b5-a311-b54c1413cff5', '3b4d005c-ae5d-4856-9a90-982e5c697f16', 'ad6498bb-ad02-4280-bd62-f80a63f1c9d6', '39aa896e-6d36-4de5-a37b-cbcd79d813fc', 'e636bbef-e041-465b-8b35-7725db27d688', '5bdf2b2c-ad59-4883-b22a-3d387cf7c340', '4d0d6c86-5f04-48f7-a762-dfc96d07df08', '95cfff2d-9bce-422e-984b-3544b160940f', 'a30fd1ad-f7d5-4dbc-b254-e9f9056d42c8', '0dfc1b7e-0ed3-491c-819e-79d4c18663a3', '1f455803-1597-4ce3-bf5a-25a7d9b651f9', 'cfce19a5-8b0e-401d-b789-a6bbe9942383', '9a70c13a-4f55-495e-8b7b-703c778ccd05', 'a9ed97cf-08ba-436f-af6a-1ac1be05b8bf', 'bfea9b8c-2351-4e11-a272-68434695e1a6', 'd9d7b2de-85f4-42de-9fec-0e7bf5bffeca', '435f07f8-38a1-4a94-86b6-42e72c2e92db', 'f5d3dda8-7151-452f-8aa9-a4590c0bc712', '5d6fea3e-5a54-49a8-9375-b5f768fb3651', '3aa116c8-3753-4c09-94b6-33e787a0efbf', '55faa2ff-219b-40b3-82d2-24428e2662e9', 'd8b5052f-d866-4bdf-8cfa-121ad27fda51', '6f2b3397-185b-49ea-8917-f0752fced3c2', '2afef1cb-6950-4b95-b73c-a795b7c5511d', 'a2726abe-69cc-4252-acf4-024c2781ffed', 'b8631110-a46e-47eb-8eb1-f2342bb50ab7', '0c7ecc05-96f0-4a0e-91e2-9e71a3abb506', '285d7636-a645-4f56-819d-cf2c32d5ecc8', '93c2b017-25f2-41cd-b179-63c9f94fe04a', '8fe7fdcb-73bc-436f-86a9-9180d3aff0ab', '46e28f4f-261d-4c8f-913d-e1a7695f02a4', '49319728-5062-40a9-8734-81f561dc4f12', '573f90af-eff2-4c0b-8f2c-37ebb4e7d8be', '1db486d3-27b2-40c8-a6b8-c9e544f9ea21', 'b5ff6576-4efe-4247-b1dc-86ebf1e16658', '370c174d-ef04-4690-afe3-e4561b57fdbf', 'b4b88b9b-1581-45da-b112-25432d07d83b', 'aef70c8f-68e9-4cc0-8f49-83418d431b31', '381331ae-80c5-4379-8149-4fa9fb9fbb30', 'e2bf3652-72fb-4e82-9dec-3076c91b8975', 'c1583a8e-9bf4-4b01-9687-28cdaa7b0cb2', 'baf81867-a5de-4805-959d-050346226f27', '359f41e8-78f6-4310-85b4-a2966a2ef252', '86334a70-f528-497c-b9d4-74d9f0b664be', 'f1a07b1e-339c-44a5-a03e-4fbde22cc9f0', '541c934f-3eec-4104-8eff-ab85bbc68481', '41eb72f9-b558-4cd9-8a5f-4e99504ba095', '210a3d83-b993-4614-b9cd-55ffa46470dd', 'f68548a9-4702-4e55-9fb2-13468ae075bf', 'cad969ea-d4c6-480c-b7e1-9af11198bf4f', '83551478-6d9b-4ec8-8a36-afa54f881e0f', '3583f67d-f87a-41ea-8b61-38b500f17337', 'a900d6cd-1adb-4fc2-8694-162b22e46851', 'a4376e8d-2626-4b27-920d-591a1050d77f', '7abcb440-e2af-4243-b019-c0a96f67022d', 'bb7a7af8-19b9-4e81-b0d5-3c9c083f981e', '4f861fe5-77d3-4ca7-b4af-8b22679d6e42', '02a2ba26-16bd-47a7-be48-57507c381bb1', 'ce27ca60-8d9f-4dc4-99a4-b8a44bb74d49', '38aef045-b9ae-44dd-8eb9-f6a3f7252963', '453bc3cb-204b-4681-9493-59f9114d8a6a', '2fe42e87-8880-4c3d-abd9-d5389faecd87', 'bb2f1167-0de8-4826-acc5-fe612263f49d', 'e4b937a4-8690-4535-9947-0b46be8eff58', 'f4285018-4a60-4fb6-9212-bf5008004b02', '5751d9df-1534-41b6-8deb-088099e00eaf', '0291d345-b2d6-4496-9d04-8931bf0ab96e', '78b66c80-e18e-471c-bc4d-28d978a845b0', 'db0f0fa8-e937-4cbf-93e1-15d253271483', '0dcba787-daa3-4d04-b4a1-7f97f9da5fde', 'b3ee5751-fc2a-43eb-9c72-9758253161a2', '08b31f31-2d93-43a4-a070-87be474c5ac0', '68774b3d-5636-4353-aa4d-ab7e61752c01', '955f0102-96dd-4e33-aa59-a1e1a7f52ed2', '58393f19-be1c-4949-8e22-5b31329079d3', '592426c9-0c3d-41b5-b5a5-d148b735f3a0', '8da9fc28-1b07-4656-86c6-e58178652561', 'aa986a14-3d5c-4e40-bd05-9de1c04f6138', '06f26c0d-830d-46f3-9465-3dc636c71b06', '6e604b4a-14dc-4c71-8816-83acdb25d535', '9c1e3bdc-54bb-4ee7-83d9-a6f6e9ffbacf', 'ebe69a9b-1ed4-4e3c-a22c-c62e2c975be4', 'cd07f4cf-b084-4dea-abc7-c0cfa0a6e55b', 'feffe4f2-7950-40a6-8435-64953ffe29de', '5a7b7028-501e-4571-8a42-a249418c9116', '7eb471b5-e32a-49c2-a84b-351671e60934', '0d885420-10a9-4cce-9d98-923d1dc351a0', 'bf3d73be-bd59-40a5-becd-25c463d4812a', '18c3af6a-8691-45b3-b38b-9c60fa3a9e7f', '4b106a78-1246-4ad9-8174-3fcb9c4fd687', 'cdba2a8e-9ae4-4984-8fa4-fa68e7e8b2f1', 'd641c38d-8804-454d-95b2-f95d5492409f', 'b0176610-26ae-4135-9ea3-deef257771f0', '14eae3b6-2391-4b72-841b-454cf04efa08', 'd899d12d-d639-433c-9039-0e153846f48a']:


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
    "filter_criteria":"disk_group_live_entity_uuid_list=={0}".format(vg_uuid)
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
"""
