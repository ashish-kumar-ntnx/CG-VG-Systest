import time
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass

RETRY_COUNT = 10
AUTH = ("admin", "Nutanix.123")
ok_status_codes = [200, 201, 202, 203, 204]

def send_request(method, cluster_ip, url, json=None, auth=AUTH, verify=False, check_task=False, debug=False, etag=None):
  url = "https://{0}:9440/{1}".format(cluster_ip, url)
  if debug:
    print "Method: {0}\nURL: {1}\nPayload: {2}\n\n".format(method, url, json)
  if method == "GET":
    retry_count = RETRY_COUNT
    while retry_count:
      r = requests.get(url, auth=auth, verify=verify)
      if r.status_code not in ok_status_codes:
        time.sleep(0.1)
        retry_count -= 1
        print "retrying {0} on URL: {1}, remaining retries: {2}".format(method, url, retry_count)
      else:
        break
  elif method in ["POST", "PUT", "PATCH"]:
    retry_count = RETRY_COUNT
    while retry_count:
      if not etag:
        r = requests.request(method, url, json=json, auth=auth, verify=verify)
      else:
        r = requests.request(method, url, json=json, auth=auth, verify=verify, headers={"If-Match": etag})
 
      if debug:
        print r.text
      if r.status_code not in ok_status_codes:
        time.sleep(0.1)
        retry_count -= 1
        print "retrying {0} on URL: {1}, remaining retries: {2}".format(method, url, retry_count)
      else:
        break
  elif method == "DELETE":
    retry_count = RETRY_COUNT
    while retry_count:
      r = requests.delete(url, auth=auth, verify=verify)
      if r.status_code not in ok_status_codes:
        time.sleep(0.1)
        retry_count -= 1
        print "retrying {0} on URL: {1}, remaining retries: {2}".format(method, url, retry_count)
      else:
        break
  return r
