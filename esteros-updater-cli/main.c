#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    // check if sudo
    if (geteuid() != 0) {
        fprintf(stderr, "This program must be run as the root user or with sudo.\n");
        return 1;
    }
    // script url location
    char scriptUrl[] = "https://raw.githubusercontent.com/ruanyf/simple-bash-scripts/master/scripts/hello-world.sh";
    
    // script file location
    char scriptFilename[] = "temp_script.sh";

    // curl download
    char downloadCommand[256];
    sprintf(downloadCommand, "curl -s -o %s %s", scriptFilename, scriptUrl);

    // executable
    char makeExecutableCommand[256];
    sprintf(makeExecutableCommand, "chmod +x %s", scriptFilename);

    // execute
    char executeCommand[256];
    sprintf(executeCommand, "./%s", scriptFilename);

    // dl
    if (system(downloadCommand) == -1) {
        fprintf(stderr, "Error downloading the update.\n");
        return 1;
    }

    // mkex
    if (system(makeExecutableCommand) == -1 && system(executeCommand) == -1) {
        fprintf(stderr, "Error while updating.\n");
        return 1;
    }

    // ex
    if (system(executeCommand) == -1) {
        fprintf(stderr, "Error while updating.\n");
        return 1;
    }

    // cleanup
    remove(scriptFilename);

    return 0;
}

