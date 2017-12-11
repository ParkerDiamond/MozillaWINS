OBJS = SimpleTurbo.o Transcoder.o
CC = /usr/bin/g++
DEBUG = -g
CFLAGS = -c -Ofast -fPIC -std=c++11
LFLAGS = -litpp

SimpleTurbo: $(OBJS)
	$(CC) -fPIC -shared -o libsimpleturbo.so $(OBJS) $(LFLAGS)

GaussianNoise: GaussianNoise.o
	$(CC) -o GaussianNoise GaussianNoise.o $(LFLAGS)

GaussianNoise.o: GaussianNoise.cpp
	$(CC) $(CFLAGS) GaussianNoise.cpp

SimpleTurbo.o: SimpleTurbo.cpp Transcoder.h
	$(CC) $(CFLAGS) SimpleTurbo.cpp

Transcoder.o: Transcoder.cpp
	$(CC) $(CFLAGS) Transcoder.cpp

all: SimpleTurbo GaussianNoise

clean:
	rm -f $(OBJS) SimpleTurbo
