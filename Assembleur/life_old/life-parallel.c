#include "life.h"
#include <pthread.h>
#include <math.h>


typedef struct s_args{
int threads;
int threads_num;
LifeBoard *state;
LifeBoard *next_state;
int steps;
pthread_barrier_t* barrier;    
} args;

void *simulate_life_parallel_threads(void* thread_arg) {

    args * arg_t;
    arg_t = (args *) thread_arg;
    int threads = arg_t->threads;
    int threads_num = arg_t->threads_num;
    LifeBoard *state = arg_t->state;
    LifeBoard *next_state = arg_t->next_state;
    int steps = arg_t->steps;
    pthread_barrier_t* finished_board = arg_t->barrier;
    printf("threads %d, threads_num %d, state %p, next_state %p, steps %d, barrier %p\n", threads,threads_num, state, next_state, steps, finished_board);
    

  //TODO
}



void simulate_life_parallel(int threads, LifeBoard *state, int steps) {

    args args_array[threads];

    for(int i=0; i < threads; i++){
        args_array[i].threads = threads;
        args_array[i].state = state;
        args_array[i].next_state = next_state;
        args_array[i].steps = steps;
        args_array[i].barrier = &finished_board;
        args_array[i].threads_num = i;
        pthread_create(&life_workers[i], NULL, simulate_life_parallel_threads,(void*) &args_array[i]);
    }
    

  //TODO
}
