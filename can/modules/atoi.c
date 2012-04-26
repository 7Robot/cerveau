#include <stdio.h>

int main(int argc, char ** argv)
{
    if (argc > 1) {
        int i = atoi(argv[1]);
        printf("«%s» → %d\n", argv[1], i);
    }
}
