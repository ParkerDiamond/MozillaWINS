#include "Transcoder.h"

using namespace std;
using namespace itpp;

Transcoder::Transcoder()
{
    generator = ivec(2);
    generator(0) = 013;
    generator(1) = 013;
    constraint = 4;
    interleaver = wcdma_turbo_interleaver_sequence(320);
    codec.set_parameters(generator, generator, constraint, interleaver);
    ones = ones_b(320);
}


void Transcoder::encode(bvec *input, unsigned int len, bvec *output)
{
    for(int i=0;i<input->size();i++) cout << (*input)(i);
    cout << endl;

    codec.encode(*input, *output);
}

void Transcoder::decode(bvec *input, unsigned int len, bvec *output)
{
    codec.decode(to_vec(*input), *output);
    for(int i=0;i<output->size();i++) (*output)(i) ^= 1;
    
    
    for(int i=0;i<output->size();i++) cout << (*output)(i);
    cout << endl;
}
