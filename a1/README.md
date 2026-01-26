# Machines tested on
- `ubuntu2404-102` or equivalently `linux.cs.uwaterloo.ca`
- `ubuntu2404-004` or equivalently `ubuntu2404-004.students.cs.uwaterloo.ca`

# How to run
- Run the server first via `bash server.sh <storage_directory>`. For example, assuming you have `cd`ed into this assignment directory you can run `bash server.sh storage`. Within `storage` sits `hello_world.txt` and `goodbye_world.txt` for testing. The server address is specified to be `0.0.0.0` and port `1025`. The port number was chosen arbitrarily and the address was chosen to allow connections from any IP address.
- On a separate terminal/machine and in the same assignment directory, run the client via `bash client.sh <server_ip> <server_port> "<command>" "<filename>"`. For example, `bash client.sh 129.97.167.161 1025 ACTV hello_world.txt` for `ACTV` mode and `PASV` instead for `PASV` mode. You should expect to see `received_hello_world.txt` appear in your current working directory after a successful transfer. Note that the server IP should be replaced with the actual server's IP address, which can be obtained by running `ifconfig` on the server machine.