#include <iostream>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
#include <omp.h>
#include <algorithm>
#include <random>
using namespace std;
int* generateData(int numberOfElements,int range_of_numbers);
void startTimer();
double stopTimer();
void print_vector(std::vector<int> const &input)
{
    for (auto const& i: input) {
        std::cout << i << " ";
    }
}
double timer;
int main(int argc, const char * argv[]) {
    if (argc != 6) {
        std::cout<< argc<< "Please provide arguments [number_of_points number_of_buckets range_of_numbers number_of_threads is_scalable]" << std::endl;
        return -1;
    }
    
    int number_of_points = atoi(argv[1]);
    int number_of_buckets = atoi(argv[2]);
    int range_of_numbers = atoi(argv[3]);
    int number_of_threads = atoi(argv[4]);
    int initial_number_of_points = number_of_points;
    if(string(argv[5])=="scalable") {
        number_of_points = number_of_points * number_of_threads;
    }
    int* elements = generateData(number_of_points, range_of_numbers);
    omp_set_num_threads(number_of_threads);
    vector<int>* buckets[number_of_buckets];
    for(int i=0; i<number_of_buckets; i++) {
        buckets[i] = new vector<int>();
    }
    startTimer();
    #pragma omp parallel
    {
        for(int bucket_index=omp_get_thread_num();
            bucket_index<number_of_buckets;
            bucket_index+=number_of_threads){
            vector<int>* worker_bucket = buckets[bucket_index];
            int start_index = bucket_index * number_of_points/number_of_buckets;
            int lower_bound,upper_bound;
            int single_bucket_range = range_of_numbers/number_of_buckets;
            lower_bound = bucket_index * single_bucket_range;
            upper_bound = lower_bound + single_bucket_range;
            int i = start_index;
            
            do {
                int elem = elements[i];
                if(elem>=lower_bound && elem<upper_bound){
                    worker_bucket->push_back(elem);
                }
                
                i++;
                i%=number_of_points;
            } while (i!=start_index);
            
            sort(worker_bucket->begin(), worker_bucket->end());
        }
        
    }
    double exec_time = stopTimer();
    cout<<exec_time<<","<<initial_number_of_points<<","<<number_of_buckets<<","<<range_of_numbers<<","<<number_of_threads<<endl;
        delete[] elements;
    

    return 0;
}

int* generateData(int numberOfElements,int range_of_numbers){
    int* elements = new int[numberOfElements];
    std::random_device rand_dev;
    std::mt19937 generator(rand_dev());
    std::uniform_int_distribution<int>  distr(0, range_of_numbers);
    #pragma omp parallel for
    for(int i=0;i<numberOfElements;i++){
        elements[i] = distr(generator);
    }
    return elements;
}

void startTimer(){
    timer = omp_get_wtime();
}

double stopTimer(){
    return omp_get_wtime() - timer;
}
