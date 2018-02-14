#include <thread>
#include <iostream>
#include <mutex>
#include <condition_variable>
#include <chrono>


class barrier {
    private :
        unsigned _resistance;
        std::mutex _forLock;
        std::condition_variable _cv;
    public :
        barrier(unsigned resistance) : _resistance(resistance) {}
        
        void reach() {
            std::unique_lock<std::mutex> lock{_forLock};
            
            if (--_resistance == 0) {
                _cv.notify_all();
            } else {
                _cv.wait(lock, [this] { return _resistance == 0; });
            }
        }
};


barrier test(4);


void f() {
    std::cout << "f() starts" << std::endl;
    std::cout << "thread waits on barrier" << std::endl;
    test.reach();
    std::cout << "barrier breached" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::cout << "f() completes" << std::endl;
}


int main() {
    std::thread t1{f};
    std::thread t2{f};
    std::thread t3{f};
    std::thread t4{f};
    t1.join();
    t2.join();
    t3.join();
    t4.join();
}
