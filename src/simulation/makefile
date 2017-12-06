OBJS = SimpleTurbo.o Transcoder.o
CC = /usr/bin/g++
DEBUG = -g
CFLAGS = -c -Ofast
LFLAGS = -litpp

SimpleTurbo: $(OBJS)
	$(CC) -o SimpleTurbo $(OBJS) $(LFLAGS)

SimpleTurbo.o: SimpleTurbo.cpp Transcoder.h
	$(CC) $(CFLAGS) SimpleTurbo.cpp

Transcoder.o: Transcoder.cpp
	$(CC) $(CFLAGS) Transcoder.cpp

clean:
	rm -f $(OBJS) client.o server.o client server SimpleTurbo
