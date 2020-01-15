all: build

install:
	install -o root -g root -m u=rwx,go=xr,+s pupstat /usr/bin
	install -o root -g root pupstat.py /usr/bin

uninstall:
	rm -f /usr/bin/pupstat
	rm -f /usr/bin/pupstat.py

build: setuid.c
	gcc setuid.c -o pupstat

clean:
	rm -f pupstat

.PHONY: install uninstall all clean

