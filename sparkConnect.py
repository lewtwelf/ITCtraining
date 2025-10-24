import paramiko
from paramiko import SSHClient
import warnings
import time
import select

warnings.filterwarnings("ignore", category=DeprecationWarning)

local_file = "sparkJob.py"  # your Spark job file
remote_file = "/tmp/temp_spark_job.py"

# read the local Spark job
with open(local_file, "r") as f:
    code_text = f.read()

# connect to remote server
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("18.134.163.221", username="Consultants", password="WelcomeItc@2022")

# upload job file to the cluster
sftp = ssh.open_sftp()
sftp.put(local_file, remote_file)
sftp.close()

print("+++++++++++++++++++++++ Job uploaded. Running spark-submit...\n")

# run spark job in client mode (so stdout comes back to us)
stdin, stdout, stderr = ssh.exec_command(
    f"spark-submit --master local[*] {remote_file}"
)

# stream stdout and stderr in real time
while not stdout.channel.exit_status_ready():
    rl, _, _ = select.select([stdout.channel, stderr.channel], [], [], 1)
    for c in rl:
        if c == stdout.channel and c.recv_ready():
            print(c.recv(1024).decode(), end="")
        if c == stderr.channel and c.recv_stderr_ready():
            print(c.recv_stderr(1024).decode(), end="")

# print any remaining output after job finishes
print(stdout.read().decode(), end="")
print(stderr.read().decode(), end="")

# clean up remote job file
ssh.exec_command(f"rm -f {remote_file}")
ssh.close()

print("\n +++++++++++++++++++++++ Done.")
