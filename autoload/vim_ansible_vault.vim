" Declare a function that can autoload this file 
fu! vim_ansible_vault#load() 
endfu

let repo_root = expand("<sfile>:p:h:h")
execute 'pyfile ' . repo_root . '/lib/main.py'

command! -nargs=0 AnsibleVaultEncrypt py encrypt()
command! -nargs=0 AnsibleVaultDecrypt py decrypt()
