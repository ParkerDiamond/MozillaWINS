OBJS = SimpleTurbo.o Transcoder.o
CC = /usr/bin/g++
DEBUG = -g
CFLAGS = -c -Ofast -fPIC
LFLAGS = -litpp

SimpleTurbo: $(OBJS)
	$(CC) -fPIC -shared -o libsimpleturbo.so $(OBJS) $(LFLAGS)

SimpleTurbo.o: SimpleTurbo.cpp Transcoder.h
	$(CC) $(CFLAGS) SimpleTurbo.cpp

Transcoder.o: Transcoder.cpp
	$(CC) $(CFLAGS) Transcoder.cpp

clean:
	rm -f $(OBJS) SimpleTurbo
