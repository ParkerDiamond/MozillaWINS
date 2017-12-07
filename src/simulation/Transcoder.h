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
        void add_size(bvec &input);
        int get_size(bvec &input);
        void remove_size(bvec &input);
        bvec &pad(bvec &input);

    public:
        Transcoder();
        void encode(bvec &input, vec &trans_symbols);
        void decode(vec &trans_symbols, bvec &output);
};
