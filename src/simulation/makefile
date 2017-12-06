OBJS = SimpleTurbo.o Transcoder.o
CC = /usr/bin/g++
DEBUG = -g
CFLAGS = -c -Ofast
LFLAGS = -litpp

SimpleTurbo: $(OBJS)
	$(CC) -o SimpleTurbo $(OBJS) $(LFLAGS)

SimpleTurbo.o: SimpleTurbo.cpp Transcoder.h
	$(CC) $(CFLAGS) SimpleTurbo.cpp

client: $(OBJS)
	$(CC) -o client client.o $(OBJS) $(LFLAGS)

client.o: client.cpp Transcoder.h
	$(CC) $(CFLAGS) client.cpp

server: $(OBJS)
	$(CC) -o server server.o $(OBJS) $(LFLAGS)

server.o: server.cpp Transcoder.h
	$(CC) $(CFLAGS) server.cpp

Transcoder.o: Transcoder.cpp
	$(CC) $(CFLAGS) Transcoder.cpp

clean:
	rm -f $(OBJS) client.o server.o client server SimpleTurbo
