# vim-ansible-vault

[![asciicast](https://asciinema.org/a/2slyQm1cV0xDlpKsiDyQ5Z4LQ.png)](https://asciinema.org/a/2slyQm1cV0xDlpKsiDyQ5Z4LQ?autplay=1&size=medium)

Vim helpers to encrypt / decrypt Ansible vaults. May use vault-ids that are read
from your ansible.cfg. In case ansible.cfg won't found in the way from your
current filesystem position, try to use ansible-vault encrypt/decrypt with
current shell settings.

- `:AnsibleVaultEncrypt` - to encrypt vault files
- `:AnsibleVaultDecrypt` - to decrypt vault files

So, you can map these to your leader call, adding next lines to your vim/nvim
config:

```bash
   let mapleader = ","
   nmap <Leader>d :AnsibleVaultDecrypt<cr>
   nmap <Leader>e :AnsibleVaultEncrypt<cr>
```
