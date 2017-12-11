/*  Author: Parker Diamond
    COSC 594: Special Topics (Distributed Systems)
    SARATOGA Turbo Code Effectiveness */

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <itpp/itcomm.h>

using namespace std;
using namespace itpp;

/* This program takes as inputs 2 integers as command line
   arguments: the noise level in Watts/Hz and the a block
   size corresponding to the desired frame size. The program
   will then simulate a Turbo coded transmissions over a noisy
   channel by adding Gaussian distributed white noise to the
   transmission. */

int main(int argc, char **argv)
{
    Turbo_Codec coder;
    BPSK bpsk;
    BERC bit_errors;
    BLERC frame_errors;
    stringstream argparse;
    int block_size, max_bits, noise;

    if(argc != 3)
    {  
        cout << "Usage: GaussianNoise noise block_size" << endl;
        return -1;
    }
    else
    {
        argparse << argv[1];
        argparse >> noise;
        argparse.clear(); 

        argparse << argv[2];
        argparse >> block_size;
        argparse.clear(); 
    }

    /* Initialize the Turbo Coder with our default Generator
       matrix and set the interleaver length to the frame size.
       Initialize as well the frame error counter with the frame
       size. */

    ivec generator = ivec(3);
    generator(0) = 013;
    generator(1) = 015;
    ivec interleaver = wcdma_turbo_interleaver_sequence(block_size);
    coder.set_parameters(generator, generator, 4, interleaver);

    frame_errors.set_blocksize(block_size);

    cout << "BER,FER,Noise" << endl;
    
    /* Starting with the provided noise level, iterate down to a
       noise level of zero while transmitting 4 frames on the noisy
       channel. */

    for(int i=noise;i>=0;i--)
    {
        /* Initialize a new channel with the desired noise level
           and clear the error counts from the previous channel. */
        AWGN_Channel channel(i);
        bit_errors.clear();
        frame_errors.clear();

        for(int j=0;j<50;j++)
        {
            /* Run 50 trials of sending/receiving in the noisy channel
               and count the errors for each trial. */
            {
                bvec in = randb(4*block_size);
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

        /* Report the bit errors and frame errors of the channel for
           the noise level. */
        cout << bit_errors.get_errorrate() << ","
             << frame_errors.get_errorrate() << ","
             << i << endl;
    }
 
    return 0;
}

