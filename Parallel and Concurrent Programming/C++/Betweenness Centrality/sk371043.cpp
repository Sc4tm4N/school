#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include <stack>
#include <queue>
#include <climits>
#include <atomic>
#include <thread>


unsigned _maxThreads;
std::vector<std::vector<int>> nodes;
int _maximumId, _minimumId;
unsigned _difference;
std::atomic<unsigned> actualToDo{0};
std::atomic<double>* BC;


void addTo(unsigned index, double howMuch) {
    auto current = BC[index].load();
  
    while (!BC[index].compare_exchange_weak(current, current + howMuch));
}


int giveIndex(int nameOfNode) {
    if (nameOfNode < 0) {
        return -nameOfNode;
    } else {
        return _difference + nameOfNode;
    }
}


void calculateBCFor(unsigned size) {
    unsigned current = actualToDo.fetch_add(1, std::memory_order_relaxed);
    
    std::vector<int> P[size];
    std::vector<int> sigma(size, 0);
    std::vector<double> delta(size, 0);
    std::vector<int> d(size, -1);
    
    while (current < size) {
        if (nodes[current].size() != 0) {
            std::stack<int> S;
            std::queue<int> Q;
    
            for (unsigned i = 0; i < size; i++) {
                P[i].resize(0);
            }
            
            std::fill(sigma.begin(), sigma.end(), 0);
            std::fill(delta.begin(), delta.end(), 0);
            std::fill(d.begin(), d.end(), -1);

            sigma[current] = 1;
            d[current] = 0;
            
            if (current < _difference) {
                Q.push(-current);
            } else {
                Q.push(current - _difference);
            }

            while (!Q.empty()) {
                int newFromQueue = Q.front();
                int v = giveIndex(newFromQueue);
                Q.pop();
                S.push(newFromQueue);

                for (const int& currentNode : nodes[v]) {
                    int w = giveIndex(currentNode);
                    
                    if (d[w] < 0) {
                        Q.push(currentNode);
                        d[w] = d[v] + 1;
                    }
                    if (d[w] == d[v] + 1) {
                        P[w].push_back(newFromQueue);
                        sigma[w] += sigma[v];
                    }
                }
            }    

            while (!S.empty()) {
                int newFromStack = S.top();
                int w = giveIndex(newFromStack);
                S.pop();
            
                for (const int& g : P[w]) {
                    int inIndex = giveIndex(g);
                    double c = ((double)sigma[inIndex] / (double)sigma[w]) * (1.0 + delta[w]);
                    delta[inIndex] += c;
                }

                if (current < _difference) {
                    if (newFromStack != -((int)current)) {
                        addTo(w, delta[w]);
                    }
                } else {
                    if (newFromStack != (int)(current - _difference)) {
                        addTo(w, delta[w]);
                    }
                }
            }
        }

        current = actualToDo.fetch_add(1, std::memory_order_relaxed);
    }
}


void printSortedBetweenesses(char* nameOfFile, unsigned size) {
    FILE* output;
    output = fopen(nameOfFile, "w");
    bool begin = true;
    
    for (unsigned i = 0; i < size; i++) {
        if (nodes[i].size() != 0) {
            if (!begin) {
                fputc('\n', output);
                    
                if (i < _difference) {
                    fprintf(output, "%d %f", -i, BC[i].load());
                } else {
                    fprintf(output, "%d %f", i - _difference, BC[i].load());
                }
            } else {
                begin = false;
                
                if (i < _difference) {
                    fprintf(output, "%d %f", -i, BC[i].load());
                } else {
                    fprintf(output, "%d %f", i - _difference, BC[i].load());
                }
            }
        }
    }
    fclose(output);
}


void readData(char *nameOfFile) {
    _maximumId = INT_MIN;
    _minimumId = INT_MAX;

    std::vector<std::vector<int>> positiveNodes;
    std::vector<std::vector<int>> negativeNodes;
    
    std::ifstream file;
    file.open(nameOfFile);

    int first, second;

    while (file >> first >> second) {
       _maximumId = std::max(std::max(_maximumId, first), second);
       _minimumId = std::min(std::min(_minimumId, first), second);

       if (first < 0) {
            for (int i = negativeNodes.size(); i <= -first; i++) {
                std::vector<int> someNewVector;
                negativeNodes.push_back(someNewVector);
            }
            negativeNodes[-first].push_back(second);
       } else {
            for (int i = positiveNodes.size(); i <= first; i++) {
                std::vector<int> someNewVector;
                positiveNodes.push_back(someNewVector);
            }
            positiveNodes[first].push_back(second);
       }
    }
    
    file.close();
    
    for (int i = negativeNodes.size(); i <= -_minimumId; i++) {
        std::vector<int> someNewVector;
        negativeNodes.push_back(someNewVector);
    }

    for (int i = positiveNodes.size(); i <= _maximumId; i++) {
        std::vector<int> someNewVector;
        positiveNodes.push_back(someNewVector);
    }
    
    _difference = negativeNodes.size();
    
    nodes.insert(nodes.end(), negativeNodes.begin(), negativeNodes.end());
    nodes.insert(nodes.end(), positiveNodes.begin(), positiveNodes.end());
    
}


int main(int argc, char* argv[]) {
    unsigned size;

    _maxThreads = atoi(argv[1]);
    
    readData(argv[2]);
    size = nodes.size();

    BC = new std::atomic<double>[size];

    std::thread threads[_maxThreads];
    
    for (unsigned i = 0; i < _maxThreads; i++) {
        threads[i] = std::thread{[size]{calculateBCFor(size);}};
    }

    for (unsigned i = 0; i < _maxThreads; i++) {
        threads[i].join();
    }

    printSortedBetweenesses(argv[3], size);

    delete BC;
    
    return 0;
}
