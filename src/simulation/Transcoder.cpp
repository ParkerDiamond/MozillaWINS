#include "Transcoder.h"

using namespace std;
using namespace itpp;

Transcoder::Transcoder()
{
    generator = ivec(3);
    generator(0) = 013;
    generator(1) = 015;
    constraint = 4;
    block_size = 320;

    interleaver = wcdma_turbo_interleaver_sequence(320);
    codec.set_parameters(generator, generator, constraint, interleaver);
}


void Transcoder::encode(bvec &input, vec &trans_symbols)
{
    int padding;
    bvec padded_input, encoded;

    padding = input.size() % block_size;
    if(padding) padded_input = concat(input, zeros_b(padding));
    else padded_input = input;

    codec.encode(padded_input, encoded);
    bpsk.modulate_bits(encoded, trans_symbols);
}

void Transcoder::decode(vec &trans_symbols, bvec &output)
{
    codec.decode(trans_symbols, output); 
}
