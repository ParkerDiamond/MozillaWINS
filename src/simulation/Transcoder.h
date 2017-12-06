#include <iostream>
#include <functional>
#include <itpp/comm/turbo.h>

using namespace std;
using namespace itpp;

class Transcoder
{
    private:
        Turbo_Codec codec;
        ivec generator, interleaver;
        int constraint;
        bvec ones;

    public:
        Transcoder();
        void encode(bvec *input, unsigned int len, bvec *output);
        void decode(bvec *input, unsigned int len, bvec *output);
        void check(bvec *input, unsigned int len, bvec *output, bvec *ground_truth);
};
