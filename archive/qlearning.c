#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <omp.h>


int index(float* arr, float item, size_t size) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == item) {
            return i;
        }
    }
}

int main(int argc, char** argv) {
    return 0;
}
