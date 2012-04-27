#include <stdio.h>
#include <math.h>

int main(int argc, char ** argv)
{
    if (argc > 1) {
        int i = atoi(argv[1]);
        printf("«%s» → %d\n", argv[1], i);
        i = round(2.35);
    }
}
