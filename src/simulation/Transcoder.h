#include <iostream>
#include <functional>
#include <itpp/itcomm.h>

using namespace std;
using namespace itpp;

class Transcoder
{
    private:
        BPSK bpsk;
        Turbo_Codec codec;
        ivec generator, interleaver;
        int constraint, block_size;

    public:
        Transcoder();
        void encode(bvec &input, vec &trans_symbols);
        void decode(vec &trans_symbols, bvec &output);
};
