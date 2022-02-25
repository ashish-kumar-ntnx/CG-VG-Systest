from config import SETUP_TYPE
from vm_entity import VM
from mh_vm_entity import MhVM

class BaseVM(object):
  if SETUP_TYPE == "AHV":
    return VM
  elif SETUP_TYPE == "ESX":
    return MhVM
