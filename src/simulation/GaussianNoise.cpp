#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <itpp/itcomm.h>

using namespace std;
using namespace itpp;

int main(int argc, char **argv)
{
    Turbo_Codec coder;
    BPSK bpsk;
    BERC bit_errors;
    BLERC frame_errors;
    stringstream argparse;
    int block_size, max_bits;
    double EbN0;

    if(argc != 3)
    {  
        cout << "Usage: GaussianNoise EbN0 block_size" << endl;
        return -1;
    }
    else
    {
        argparse << argv[1];
        argparse >> EbN0;
        argparse.clear(); 

        argparse << argv[2];
        argparse >> block_size;
        argparse.clear(); 
    }

    // Initialize the Turbo Coder
    ivec generator = ivec(3);
    generator(0) = 013;
    generator(1) = 015;
    ivec interleaver = wcdma_turbo_interleaver_sequence(block_size);
    coder.set_parameters(generator, generator, 4, interleaver);

    // Initialize the AWGN Channel
    AWGN_Channel channel(EbN0);
    frame_errors.set_blocksize(block_size);
    
    for(int i=0;i<50;i++)
    {
        {
            bvec in = randb(2*block_size);
            vec modulated;
            bvec buffer, out;

            coder.encode(in, buffer);
            bpsk.modulate_bits(buffer, modulated);

            modulated = channel(modulated);
            coder.decode(modulated, out);

            bit_errors.count(in,out);
            frame_errors.count(in,out);
        }
    }

    cout << "Simulated " << frame_errors.get_total_blocks() 
         << " frames and " << bit_errors.get_total_bits() << " bits." << endl;
    
    cout << "Obtained " << bit_errors.get_errors() << " bit errors. " << endl
         << " BER: " << bit_errors.get_errorrate() << endl
         << " FER: " << frame_errors.get_errorrate() << endl;

    return 0;
}

