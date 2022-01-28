import socket

from twitter.connection.twitter_get_connection import send_tweets

if __name__ == "__main__":
    new_skt = socket.socket()  # initiate a socket object
    host = "127.0.0.1"  # local machine address
    port = 5007  # specific port for your service.
    new_skt.bind((host, port))  # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)  # waiting for client connection.
    c, addr = new_skt.accept()  # Establish connection with client. it returns first a socket object,c, and the address bound to the socket

    print("Received request from: " + str(addr))
    # and after accepting the connection, we can send the tweets through the socket
    send_tweets(c)