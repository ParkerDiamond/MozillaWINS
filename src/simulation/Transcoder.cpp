#include "Transcoder.h"

using namespace std;
using namespace itpp;

Transcoder::Transcoder()
{
    generator = ivec(2);
    generator(0) = 013;
    generator(1) = 015;
    constraint = 6;
    interleaver = wcdma_turbo_interleaver_sequence(320);
    codec.set_parameters(generator, generator, constraint, interleaver);
}


void Transcoder::encode(bvec *input, unsigned int len, bvec *output)
{
    for(int i=0;i<input->size();i++) cout << (*input)(i);
    cout << endl;

    codec.encode(*input, *output);
    cout << codec.get_Ncoded() << endl;
}

void Transcoder::decode(bvec *input, unsigned int len, bvec *output)
{
    codec.decode(to_vec(*input), *output); 
    for(int i=0;i<output->size();i++) (*output)(i) ^= 1;    
}

void Transcoder::check(bvec *input, unsigned int len, bvec *output, bvec *ground_truth)
{ 
    codec.decode(to_vec(*input), *output, *ground_truth);
    for(int i=0;i<output->size();i++) (*output)(i) ^= 1;        
}
