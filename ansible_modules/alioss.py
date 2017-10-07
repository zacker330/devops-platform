#!/usr/bin/python


DOCUMENTATION = '''
---
module: alioss
short_description: upload and download aliyun oss object
'''

EXAMPLES = '''
- name: upload
  alioss:
    access_key_id: "{{ access_key_id }}"
    access_key_secure: "{{ access_key_secure }}"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "upload"
    path: "./upload.yml"
    object_name:  "tmp/upload.yml"
  register: result
- name: download
  alioss:
    access_key_id: "{{ access_key_id }}"
    access_key_secure: "{{ access_key_secure }}"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "download"
    path: "/tmp/download.yml"
    object_name:  "tmp/upload.yml"
  register: result
'''


from ansible.module_utils.basic import *
import oss2
import os,sys


def get_state(b_path):
    ''' Find out current state '''
    if os.path.islink(b_path):
        return 'link'
    elif os.path.isdir(b_path):
        return 'directory'
    elif os.stat(b_path).st_nlink > 1:
        return 'hard'
    else:
        # could be many other things, but defaulting to file
        return 'file'


def recursive_set_attributes(module, b_path, follow, file_args):
    changed = False
    if get_state(b_path) == 'file':
        tmp_file_args = file_args.copy()
        tmp_file_args['path'] = to_native(b_path, errors='surrogate_or_strict')
        changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
    elif  get_state(b_path) == 'directory':
        for b_root, b_dirs, b_files in os.walk(b_path):
            for b_fsobj in b_dirs + b_files:
                b_fsname = os.path.join(b_root, b_fsobj)
                if not os.path.islink(b_fsname):
                    tmp_file_args = file_args.copy()
                    tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                    changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
                else:
                    tmp_file_args = file_args.copy()
                    tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                    changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
                    if follow:
                        b_fsname = os.path.join(b_root, os.readlink(b_fsname))
                        if os.path.isdir(b_fsname):
                            changed |= recursive_set_attributes(module, b_fsname, follow, file_args)
                        tmp_file_args = file_args.copy()
                        tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                        changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
    return changed

def alioss_upload(module, data):

    try:
        oss_key = data['access_key_id']
        oss_AccessKeySecret = data['access_key_secure']
        endpoint = data['endpoint']
        path = data['path']
        bucket = data['bucket']
        object_name = data['object_name']

        auth = oss2.Auth(oss_key,oss_AccessKeySecret)
        bucket = oss2.Bucket(auth, endpoint, bucket)
        fp = open(path, 'r')
        bucket.put_object(object_name, fp)

    except BaseException as e:
        return False, {'response': e}
    else:
        return True, {"response": "upload success"}


def alioss_download(module, data):
    changed = False
    try:
        oss_key = data['access_key_id']
        oss_AccessKeySecret = data['access_key_secure']
        endpoint = data['endpoint']
        bucket = data['bucket']
        path = data['path']
        object_name = data['object_name']
        # follow = True
        # follow = data['follow']
        ## get files
        file_args = module.load_file_common_arguments(data)

        ## if path exists don't continue
        exists = os.path.exists(path)
        if exists:
            changed = False
        else:
            ### download
            auth = oss2.Auth(oss_key,oss_AccessKeySecret)
            bucket = oss2.Bucket(auth, endpoint, bucket)
            f = open(path,"w")
            f.write(bucket.get_object(object_name).read())
            f.close()
            changed = True

        changed = recursive_set_attributes(
                module,
                to_bytes(file_args['path'],
                    errors='surrogate_or_strict'),
                True,
                file_args)
        return changed, {"response": "success"}
    except BaseException as e:
        # return False, {'response': e}
        module.fail_json(msg= e)
    else:
        return changed, {"response": "download success"}



def main():
    fields = {
            "access_key_id": {"required": True, "type": "str"},
            "access_key_secure": {"required": True, "type": "str" },
            "endpoint": {"required": True, "type": "str"},
            "bucket": {"required": True, "type": "str"},
            "target": {
                "default": "upload",
                "choices": ['upload', 'download'],
                "type": 'str'
            },
            "path": {"required": True, "type": "str"},
            "object_name":  {"required": True, "type": "str"}
    }
    choice_map = {
          "upload": alioss_upload,
          "download": alioss_download,
    }


    module = AnsibleModule(
        argument_spec=fields,
        add_file_common_args=True
    )
    has_changed, result = choice_map.get(module.params['target'])(module, module.params)
    module.exit_json(changed=has_changed, meta=result)
    # auth = oss2.Auth(oss_key,oss_AccessKeySecret)
    # bucket = oss2.Bucket(auth, endpoint, 'cibuckets')
    #
    #
    # f = open(pacakge_write_to,"w")
    #
    # f.write(bucket.get_object(package_path).read())
    #
    # f.close()


if __name__ == '__main__':
    main()
