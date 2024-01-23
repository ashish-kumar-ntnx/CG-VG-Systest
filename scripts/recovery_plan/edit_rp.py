from framework.recovery_plan_entity import RecoveryPlan
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
IP = SRC_PC_IP

rp = RecoveryPlan(IP)
data_service_ip_mapping_list = [{"data_service_ip_mapping":[{"recovery_data_service_ip":"10.45.133.142","test_data_service_ip":"10.45.133.142","availability_zone_url":"3e8d35d9-32ea-440b-8f9d-e5844ae98c71","cluster_reference":{"kind":"cluster","uuid":"0005d4e9-5425-61a3-35a5-0cc47a9ba363"}},{"recovery_data_service_ip":"10.53.128.98","test_data_service_ip":"10.53.128.98","availability_zone_url":"b47f5bb9-2a30-4d7a-b96d-a082af811c46","cluster_reference":{"kind":"cluster","uuid":"0005d533-c433-972c-0000-000000011f39"}}]}]

for i in range(1, 11):
  rp_name = "rp-vgs-vms-set-" + str(i)
  rp_obj = rp.get(rp_name=rp_name)
  spec = rp_obj.spec
  spec.pop("status")
  spec["spec"]["resources"]["parameters"]["data_service_ip_mapping_list"] = data_service_ip_mapping_list
  rp_obj.edit(spec=spec)
