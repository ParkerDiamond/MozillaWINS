/* Author: Parker Diamond
   Modified By: Kyle Birkeland
   COSC594: Special Topics (Distributed Systems)
   SARATOGA Turbo Codes */

#include "Transcoder.h"

using namespace std;
using namespace itpp;

int SIZE_BITS = 32;

Transcoder::Transcoder()
{
    /* The constructor specifies a Generator matrix with
       polynomials x^3 + x^2 + 1 and x^3 + x + 1. The
       interleaver is provided by IT++ by is given a frame
       size of 320 bits. */

    generator = ivec(2);
    generator(0) = 013;
    generator(1) = 015;
    constraint = 4;
    block_size = 320;

    interleaver = wcdma_turbo_interleaver_sequence(320);
    codec.set_parameters(generator, generator, constraint, interleaver);
    codec.set_adaptive_stop(true);
}

/* The add_size, get_size, and remove_size methods were all added by
   Kyle Birkeland in order to pad arbitrary length messages out to a
   multiple of the block length (320), which is necessary for successful
   encoding. */

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
    int last = size < input.size() - SIZE_BITS && size >= 0 ? SIZE_BITS + size - 1 : -1;
    input = input(SIZE_BITS, last);
}

/* The encode function takes a vector of bits, pads it to the nearest
   block length and then uses a Binary Phase Shift Keying, to modulate
   the bits into -1 and 1 values. The encoded and modulated bits are
   stored in the trans_symbols reference. */

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

/* The decode function is simply a wrapper to the IT++ Turbo_Codec
   decode function, which expects a sequence of real valued bit inputs.
   IT++ expects this to model signal inputs rather than bits, but it
   works for discrete event simulations as well. */

void Transcoder::decode(vec &trans_symbols, bvec &output)
{
    codec.decode(trans_symbols, output); 
    remove_size(output);
}
