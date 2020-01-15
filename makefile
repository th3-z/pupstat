all: build

install:
	install pupstat /usr/bin
	install pupstat.py /usr/bin

uninstall:
	rm -f /usr/bin/pupstat
	rm -f /usr/bin/pupstat.py

build: setuid.c
	gcc setuid.c -o pupstat
	chown root:root pupstat
	chmod u=rwx,go=xr,+s pupstat

.PHONY: install uninstall all

