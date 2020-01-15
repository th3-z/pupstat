#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>

/*
 * Runs pupstat.py as root, allows regular users to run it
 */

int main(int argc, char *argv[]) {
    setreuid(geteuid(), geteuid());
    setregid(getegid(), getegid());
    
    return system("/usr/bin/python3 ./pupstat.py");
}

