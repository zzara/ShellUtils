#include <stdio.h>
#include <stdlib.h>

int max(int a, int b) {
    if (a < b)
        return b;
    return a;
}

void squares(int size1, int x_offset, int y_offset, int size2) {
  //compute the max of size1 and (x_offset + size2).  Call this w
  int s = x_offset + size2;
  int w = max(size1,s);
  //compute the max of size1 and (y_offset + size2).  Call this h
  int t = y_offset + size2;
  int h = max(size1,t);
  int x,y;
  //count from 0 to h. Call the number you count with y
  for (y=0;y<h;y++){
    //count from 0 to w. Call the number you count with x
    for (x=0;x<w;x++){
      //check if  EITHER
      //    ((x is between x_offset  and x_offset +size2) AND
      //     y is equal to either y_offset OR y_offset + size2 - 1 )
      //  OR
      //    ((y is between y_offset and y_offset + size2) AND
      //     x is equal to either x_offset OR x_offset + size2 -1)
      // if so, print a *
    if (((((x>=x_offset)&&(x<s))||((x<x_offset)&&(x>=s)))&&((y==y_offset)||(y==t-1)))||((((y>=y_offset)&&(y<t))||((y<y_offset)&&(y>=t)))&&((x==x_offset)||(x==s-1)))){
        printf("*");
    }
      //if not,
      // check if EITHER
      //    x is less than size1 AND (y is either 0 or size1-1)
      // OR
      //    y is less than size1 AND (x is either 0 or size1-1)
      //if so, print a #

      //else print a space
    else{
        if (((x<size1)&&((y==0)||(y==size1-1)))||((y<size1)&&((x==0)||(x==size1-1)))){
            printf("#");
        }
        else{
            printf(" ");
        }
    }
    //when you finish counting x from 0 to w,
    //print a newline
    }
  printf("\n");
  }
}
int main (int argc, char *argv[]){
    char *hh = argv[1];
    int hhi = atoi(hh);
    char *ii = argv[2];
    int iii = atoi(ii);
    char *jj = argv[3];
    int jji = atoi(jj);
    char *kk = argv[4];
    int kki = atoi(kk);
    squares(hhi,iii,jji,kki);
}
