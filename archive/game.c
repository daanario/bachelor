#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <omp.h>
#include <time.h>

typedef void (*print_callback)(const char*);

void print_cb_f(print_callback callback, double item) {
     if (callback != NULL) {
            char buffer[100];
            sprintf(buffer, "item: %f array: ", item);
            callback(buffer);
    }
}

void print_cb_str(print_callback callback, char* str) {
     if (callback != NULL) {
            char buffer[100];
            sprintf(buffer, str);
            callback(buffer);
    }
}

int find_index_cb(double* arr, double item, size_t size, print_callback callback) {
    // print array
    /*
    for (int j = 0; j < size; j++) {
        print_cb_f(callback, arr[j]);
    }
    */
    for (int i = 0; i < size; i++) {
        if (fabs(arr[i] - item) < 0.000001) {
            return i;
        }
    }
    return -1;
}

int find_index(double* arr, double item, size_t size) {
    for (int i = 0; i < size; i++) {
        if (fabs(arr[i] - item) < 0.000001) {
            return i;
        }
    }
    return -1;
}

double max_value(double* arr, size_t size) {
    double max_so_far = arr[0];
    for (int i = 0; i < size; i++) {
        if (arr[i] > max_so_far) {max_so_far = arr[i];}
    }
    return max_so_far;
}

double get_random() {
    return (double)rand() / (double)((unsigned)RAND_MAX + 1);
}

double demand(double p1, double p2) {
    if (p1 < p2) {
            return 1.0 - p1;
    } else if (fabs(p1 - p2) < 0.00001) {
            return 0.5 * (1.0 - p1);
    } else if (p1 > p2) {
            return 0;
    }
}

double profit(double p1, double p2) {
    return p1 * demand(p1, p2);
}

typedef struct Qlearner2D Qlearner2D;
typedef struct Game2D Game2D;

struct Qlearner2D {
    int k, T;
    double* qtable;
    double* prices;
    double* ps;
    double* profits;
    double alpha, delta;
    int t;
    double theta, epsilon;
};

struct Game2D {
    int k, T, N;
};

Qlearner2D* Qlearner2D_construct(int k, int T) {
    Qlearner2D* q = malloc(sizeof(*q));
    if (q == NULL) {
        //print_cb_str(cb, "Error instantiating Qlearner2D!");
        printf("Error initializing Qlearner2D object!");
    }

    q->k = k;
    q->T = T; // Total no. periods
    q->qtable = (double *)malloc(k * k * sizeof(double)); // Q table is a k X k matrix
    
    q->prices = (double *)malloc((k + 1) * sizeof(double));
    for (int i = 0; i < k+1; i++) {q->prices[i] = (float)i / k;}
    q->profits = (double *)malloc(T * sizeof(double));
    // Initialize zero matrix
    for (int i = 0; i < k; i++) {
        for(int j = 0; j < k; j++){
            q->qtable[i * k + j] = 0.0;
        }
    }
    q->ps = malloc(T * sizeof(double)); //price history array
    for (int i = 0; i < T; i++) {q->ps[i] = NAN;}
    q->alpha = 0.3;
    q->delta = 0.95;
    q->t = 0; // current period
    q->theta = -powf((1.0/1000000.0), 1.0 / (float)T) + 1;
    q->epsilon = powf((1 - q->theta), q->t);
    
    return q;
}

void Qlearner2D_update(Qlearner2D* q, int t, double s, double s_next) {
    double p = q->ps[t];
    if (isnan(p)) {printf("ERROR: p is NaN!\n");}
    int k = q->k;
    size_t size = sizeof(q->qtable);
    int m = find_index(q->prices, p, size);
    int n = find_index(q->prices, s, size);
    double prev_est = q->qtable[m * k + n];
    
    int r = find_index(q->prices, s_next, k);

    // construct temporary array of possible Q-values (constrained by the state)
    double* choices = malloc((q->k) * sizeof(double));
    for (int j = 0; j < k; j++) {
        choices[j] = q->qtable[r * k + j];
    }
    double maxedQ = max_value(choices, q->k);
    double new_est = profit(p, s) + q->delta * profit(p, s_next) + powf(q->delta, 2.0) * maxedQ;
    q->qtable[m * k + n] = (1.0 - q->alpha) * prev_est + q->alpha * new_est;
}

void Qlearner2D_setprice(Qlearner2D* q, double s) {
    if (q->epsilon >= get_random()) {
        q->ps[q->t] = q->prices[rand()%q->k]; // choose random element from prices
    }
    else {
        // first find maxedQ given our state
        int r = find_index(q->prices, s, q->k);
        double* choices = malloc((q->k) * sizeof(double));
        for (int j = 0; j < q->k; j++) {
            choices[j] = q->qtable[r * q->k + j];
        }
        double maxedQ = max_value(choices, q->k);
        q->ps[q->t] = q->prices[find_index(choices, maxedQ, q->k)];
    }

}

Qlearner2D* Qlearner2D_destruct(Qlearner2D* q) {
    free(q);
    return NULL;
}

Game2D* Game2D_construct(int k, int T, int N) {
    Game2D* g = malloc(sizeof(*g));
    if (g == NULL) {
        //print_cb_str(cb, "Error instantiating Qlearner2D!");
        printf("Error initializing Game2D object!");
    }
    g->k = k;
    g->T = T;
    g->N = N;

    return g;
}

Game2D* Game2D_destruct(Game2D* g) {
    free(g);
    return NULL;
}

void print_matrix(double* mat, int k) {
    for (int i=0; i < k; i++) {
        printf("[");
        for(int j=0; j < k; j++){
            printf("%f ", mat[i * k + j]);
        }
        printf("]\n");
    }
}

int main(int argc, char** argv) {
    srand(time(NULL)); // randomize seed
    Qlearner2D* q = Qlearner2D_construct(6, 100);
    Game2D* g = Game2D_construct(6, 100, 1);
    Qlearner2D_destruct(q);
    Game2D_destruct(g);
    return 0;
}
