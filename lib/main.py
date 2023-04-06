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
    return "./"



def list_vault_identities():
    config_file = find_ansible_config_file()
    if not config_file:
        return None
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

    current_buffer = vim.current.buffer.name

    ansible_dir = os.path.dirname(find_ansible_config_file())
    if ansible_dir != '.':
        vault_ids = list_vault_identities()
        vault_ids_str = ", ".join(vault_ids)
        vault_id = vim.eval(f'input("Enter the vault-id ({vault_ids_str})> ")')
        if vault_id not in vault_ids:
            print(f"{vault_id} is not in {vault_ids}")
            return
        cmd = f"ansible-vault encrypt --encrypt-vault-id {vault_id} {current_buffer}"
    else:
        current_buffer = '\n'.join(vim.current.buffer[:])
        cmd = f"echo '{current_buffer}' | ansible-vault encrypt --output=-"
    result = subprocess.run(
        cmd, shell=True, cwd=ansible_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(result.stderr)
        return
    vim.current.buffer[:] = result.stdout.splitlines()


def decrypt():
    if not is_encrypted():
        print("File is already decrypted")
        return

    ansible_dir = os.path.dirname(find_ansible_config_file())
    current_buffer = '\n'.join(vim.current.buffer[:])
    #current_buffer = vim.current.buffer.name
    cmd = f"echo '{current_buffer}' | ansible-vault decrypt --output=-"
    result = subprocess.run(
        cmd, shell=True, cwd=ansible_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f'echoerr "{result.stderr}"')
        return
    vim.current.buffer[:] = result.stdout.splitlines()


def is_encrypted():
    for row in vim.current.buffer[:]:
        if "$ANSIBLE_VAULT" in row:
            return True
    return False
