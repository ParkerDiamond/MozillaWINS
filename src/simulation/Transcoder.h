/* Author: Joseph Parker Diamond
   Modified by: Kyle Birkeland
   COSC594: Special Topics (Distributed Systems)
   Micah Beck
   SARATOGA Turbo Codes */

#include <iostream>
#include <functional>
#include <itpp/itcomm.h>

using namespace std;
using namespace itpp;

/* This class provides a wrapper around the IT++
   Turbo encoding and decoding functionality as well
   as methods for padding input and modulating
   bit transmissions */
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
