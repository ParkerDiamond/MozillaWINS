#include "Transcoder.h"

using namespace std;
using namespace itpp;

int SIZE_BITS = 32;

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

void Transcoder::add_size(bvec &input)
{
    bvec bsize = dec2bin(SIZE_BITS, input.size());
    input.ins(0, bsize);
}

int Transcoder::get_size(bvec &input)
{
    return bin2dec(input(0, SIZE_BITS - 1));
}

void Transcoder::remove_size(bvec &input)
{
    int size = get_size(input);
    int last = size < input.size() - SIZE_BITS ? SIZE_BITS + size - 1 : -1;
    input = input(SIZE_BITS, last);
}

void Transcoder::encode(bvec &input, vec &trans_symbols)
{
    int padding;
    bvec padded_input, encoded;

    padded_input = bvec(input);
    add_size(padded_input);

    padding = padded_input.size() % block_size;
    if(padding) padded_input = concat(padded_input, zeros_b(block_size - padding));

    codec.encode(padded_input, encoded);
    bpsk.modulate_bits(encoded, trans_symbols);
}

void Transcoder::decode(vec &trans_symbols, bvec &output)
{
    codec.decode(trans_symbols, output); 
    remove_size(output);
}
