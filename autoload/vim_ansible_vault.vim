" Declare a function that can autoload this file 
fu! vim_ansible_vault#load() 
endfu

let repo_root = expand("<sfile>:p:h:h")
execute 'py3file ' . repo_root . '/lib/main.py'

command! -nargs=0 AnsibleVaultEncrypt py3 encrypt()
command! -nargs=0 AnsibleVaultDecrypt py3 decrypt()
