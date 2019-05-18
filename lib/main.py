import os
import subprocess
import configparser
import re

def find_ansible_config_file():
    cfg_files = []
    for root, _, files in os.walk(".", topdown=False):
        for f in files:
            if f == "ansible.cfg":
                full_path = os.path.join(root, f)
                distance = len(full_path.split('/'))
                cfg_files.append({'path': full_path, 'distance': distance})
    if cfg_files:
        cfg_files.sort(key=lambda v: v["distance"])
        return cfg_files[0]['path']



def list_vault_identities():
    config_file = find_ansible_config_file()
    config = configparser.ConfigParser()
    config.read(config_file)
    identity_list_line = config["defaults"]["vault_identity_list"]
    # Extract possible options
    #  vault_identity_list = dev@./.dev_vault , test@./.test_vault
    vault_ids = re.findall("(\w+)@", identity_list_line)
    return vault_ids


def encrypt():
    if is_encrypted():
        print("File is already encrypted")
        return

    ansible_dir = os.path.dirname(find_ansible_config_file())
    current_buffer = vim.current.buffer.name

    vault_ids = list_vault_identities()
    vault_ids_str = ", ".join(vault_ids)
    vault_id = vim.eval(f'input("Enter the vault-id ({vault_ids_str})> ")')
    if vault_id not in vault_ids:
        print(f"{vault_id} is not in {vault_ids}")
        return

    current_buffer = vim.current.buffer.name
    cmd = f"ansible-vault encrypt --encrypt-vault-id {vault_id} {current_buffer}"
    result = subprocess.run(
        cmd, shell=True, cwd=ansible_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(result.stderr)
        return


def decrypt():
    if not is_encrypted():
        print("File is already decrypted")
        return

    ansible_dir = os.path.dirname(find_ansible_config_file())
    current_buffer = vim.current.buffer.name
    cmd = f"ansible-vault decrypt {current_buffer}"
    result = subprocess.run(
        cmd, shell=True, cwd=ansible_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f'echoerr "{result.stderr}"')
        return


def is_encrypted():
    return "$ANSIBLE_VAULT" in vim.current.buffer[0]
