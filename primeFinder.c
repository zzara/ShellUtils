#include <stdio.h>
#include <stdlib.h>
#define EXIT_SUCCESS 0
// infinitely check for prime numbers in probably the least efficient way :D
int main (void){
    int i,j;
    for (i=1;i<20;i++){
        // error checking -- fails if the starting number is not greater than or equal to 1
        if (i >=1 ){
            if (i == 1){
                printf("1 is not a prime number\n");
                break;
            }
            for (j=2;j<=i;j++){
                // if the target number is divisible by any other number pther than itself, break the loop and continue to check the next target number
                if (i % j == 0 && j != i){
                    break;
                }
                // if the target number is only divisible by itself, print the result
                if (i % j == 0 && j == i){
                    printf("%d is prime\n",i);
                    break;
                }
            }
        }
        else{
            printf("'i' is not greater than or equal to 1. Fix your starting number and run this program again.\n");
        }
    }
return EXIT_SUCCESS;
}
