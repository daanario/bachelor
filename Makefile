OPENMP?=-fopenmp
DEBUG?=-g
CC?=gcc
CDFLAGS?=Wextra -Wall -pedantic -std=c99 -fPIC
LDFLAGS?=-lm
LIBFLAGS?=-shared

all: game game.so
	
game: game.o
	$(CC) -o $@ $^ $(LDFLAGS) $(OPENMP)

game.so: game.o
	$(CC) -o $@ $^ $(LDFLAGS) $(OPENMP) $(LIBFLAGS)

%.o: %.c
	$(CC) -c $< $(CFLAGS) $(DEBUG) $(OPENMP)

clean:
	rm -rf game *.o *.dSYN *.pyc *.so

