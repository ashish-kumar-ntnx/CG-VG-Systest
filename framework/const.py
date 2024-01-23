from config import *
V4_API_VERSION = "v4.0.a2"
if BUILD == "master":
  CAT_API_VERSION = "v4.0.b1"
  #VG_API_VERSION = "v4.0.a3"
  #VG_ETAG_REQUIRED = True
  VG_API_VERSION = "v4.0.b1"
  #VG_API_VERSION = "v4.0.a2"
  VG_ETAG_REQUIRED = False
  CG_API_VERSION = V4_API_VERSION
else:
  CAT_API_VERSION = "v4.0.a1"
  #CAT_API_VERSION = "v2.1.a1"
  VG_API_VERSION = "v4.0.a1"
  VG_ETAG_REQUIRED = False
  CG_API_VERSION = "v4.0.a1"

def get_ntnx_req_id():
  import uuid
  return str(uuid.uuid4())
