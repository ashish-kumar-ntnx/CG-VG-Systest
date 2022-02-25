
class VG(object):
  def __init__(self, uuid=None):
    self.uuid = uuid

  def create(self, vg_name, cluster_name):
    pass

  def remove(self):
    pass

  def list_all(self):
    pass

  def get(self):
    pass

  # Disk ops
  def add_disk(self, disk_size, ctr_uuid):
    pass

  def remove_disk(self, disk_index):
    pass

  def update_disk(self):
    pass

  def get_disks(self):
    pass

  # Category ops
  def add_category(self, cat_key, cat_val):
    pass

  def remove_category(self, cat_key, cat_val):
    pass

  def get_categories(self):
    pass

  # Iscsi ops
  def get_iscsi_attachments(self):
    pass

  def attach_iscsi(self):
    pass

  def detach_iscsi(self):
    pass

  # Hypervisor attachement ops
  def get_hyp_attachments(self):
    pass

  def attach_vm(self):
    pass

  def detach_vm(self):
    pass

  # Migrate ops
  def migrate(self):
    pass


  
