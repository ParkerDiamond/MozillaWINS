OBJS = turbo_test.o
CC = /usr/bin/g++
DEBUG = -g
CFLAGS = -c
LFLAGS = -litpp

turbo_test: $(OBJS)
	$(CC) -o turbo_test $(OBJS) $(LFLAGS)

turbo_test.o: turbo_test.cpp
	$(CC) $(CFLAGS) turbo_test.cpp

