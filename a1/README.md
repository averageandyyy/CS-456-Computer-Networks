# Machines tested on
- `ubuntu2404-002` or equivalently `ubuntu2404-002.student.cs.uwaterloo.ca`
- `ubuntu2404-004` or equivalently `ubuntu2404-004.student.cs.uwaterloo.ca`

# How to run
- After unzipping this submission with `unzip a1_21232618.zip`, cd into the newly created `a1` directory. Do this for separate
  instances of the terminal on two machines, such as the ones suggested above.
- On one machine/terminal (i.e. `ubuntu2404-002`), run the server via `bash server.sh storage`. Within the `a1/storage` folder, there
  sits two files of `hello_world.txt` and `goodbye_world.txt` for testing. At this point, we should see `SERVER_PORT=<some value>` as
  requested.
- On the other machine/terminal (i.e. `ubuntu2404-004`), first `rm` the `received_*` files via `rm received_*`. Then,  run the client
  via `bash client.sh ubuntu2404-002.student.cs.uwaterloo.ca SERVER_PORT ACTV hello_world.txt`, where `SERVER_PORT` was the output from
  the server program. You should see `R_PORT` being printed. We can check the received file in `received_hello_world.txt`!
- We can repeat this with `PASV` and `goodbye_world.txt` via `bash client.sh ubuntu2404-002.student.cs.uwaterloo.ca SERVER_PORT PASV
  goodbye_world.txt`. Observe `R_PORT` from the server and `received_goodbye_world.txt` on the client machine.
- To test the assignment on a single machine, pick either one to `ssh` into and repeat the above steps of `unzip`ing, `cd`ing and
  `rm`ing test files. Using `tmux` for instance, create two terminal instances. On one instance, run the server as above. On the other
  run the client with the preferred mode and file to receive, only changing the server address to `localhost` instead, since the server
  is running locally as well.
