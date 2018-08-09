#include <stdio.h>
#include <stdlib.h>
#define EXIT_SUCCESS 0
// infinitely check for prime numbers in probably the least efficient way :D
int main (void){
    int i,j;
    for (i=2;i>0;i++){
        for (j=2;j<=i;j++){
            if (i % j == 0 && j != i){
                break;
            }
            if (i % j == 0 && j == i){
                printf("%d is prime\n",i);
                break;
            }
        }
    }
return EXIT_SUCCESS;
}
