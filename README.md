***Vault Secrets-Backup***

**Pre-requisites:**
1. Vault cluster should be up and running
2. Vault should be using integrated storage(Raft)
3. Needed vault root token (or) any other equivalent token with required permissions
4. OC command line utility

**Working:**

`
git clone https://github.com/Gokul-C/Tools-Automation.git
` 

`
cd Tools-Automation/vault
`

`
python3 backup-secrets.py
`
