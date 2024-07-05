import subprocess
import datetime
import sys

# Define global variables
vault_token = None
leader_pod = None

def login():
    global vault_token
    # Define the command
    command = f"oc exec -ti vault-0 -- vault login {vault_token}"

    # Execute the command
    execute_command(command, "Login command executed successfully!")

def peers():
    # Define the command
    command = "oc exec -ti vault-0 -- vault operator raft list-peers"

    # Execute the command
    execute_command(command, "List peers command executed successfully!")

def login_leader():
    global vault_token, leader_pod
    # Define the command
    command = f"oc exec -ti {leader_pod} -- vault login {vault_token}"

    # Execute the command
    execute_command(command, "Login leader command executed successfully!")

def backup():
    global leader_pod
    # Get the current date for the snapshot filename
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # Define the command
    command = f'oc exec -ti {leader_pod} -- vault operator raft snapshot save /tmp/vaultsnapshot-{current_date}.snap'

    # Execute the command
    execute_command(command, f"Backup command executed successfully! Snapshot saved as /tmp/vaultsnapshot-{current_date}.snap")

def copy():
    # Get the current date for the snapshot filename
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # Define the command
    command = f'oc cp vault/vault-0:/tmp/vaultsnapshot-{current_date}.snap ~/vaultsnapshot-{current_date}.snap'

    # Execute the command
    execute_command(command, f"Copy command executed successfully! Snapshot copied as ~/vaultsnapshot-{current_date}.snap")

def execute_command(command, success_message):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Filter out specific messages from stdout
        filtered_output = result.stdout.replace("tar: removing leading '/' from member names", "").strip()

        # Print filtered output if any
        if filtered_output:
            print("Output:\n", filtered_output)

        # Print success message
        print(success_message)
        
        # Print stderr if there's an error message
        if result.stderr:
            print("Error Output:\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print("Return code:", e.returncode)
        print("Error message:\n", e.stderr)
        sys.exit(1)  # Exit the script with a non-zero status code upon error

def main():
    global vault_token
    # Prompt the user to enter the Vault token
    vault_token = input("Please enter the Vault token: ")
    login()

def leader():
    global leader_pod
    # Prompt the user to enter the Vault Leader Pod name
    leader_pod = input("Please enter the Leader Vault Pod (Hint: vault-0): ")
    login_leader()
    backup()
    copy()

if __name__ == "__main__":
    try:
        main()
        peers()
        leader()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(0)  # Exit gracefully on user interrupt
