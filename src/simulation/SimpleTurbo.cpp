#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <random>
#include "Transcoder.h"

using namespace std;
using namespace itpp;

extern "C" {
    void corrupt(vec &trans, double perc_corruption)
    {
        int ncorrupt = int(perc_corruption * trans.size());
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dis(0, trans.size() - 1);

        for(int i=0; i < ncorrupt; i++) {
            int idx = dis(gen);
            trans(idx) = -1 * trans(idx);
        }
    }

    // Encodes data, simulated bit errors, and decodes data in place

    void transmit(char *data, int len, double error)
    {
        Transcoder *coder;
        bvec in, out;
        vec trans;

        for(int i = 0; i < len; i++) {
            in = concat(in, dec2bin(8, data[i]));
        }

        coder = new Transcoder();
        coder->encode(in, trans);
        corrupt(trans, error);
        coder->decode(trans, out);

        for(int i = 0; i < len; i++) {
            data[i] = bin2dec(out(i*8, (i*8)+7));
        }

        return;
    }
}

/*
int main(int argc, char **argv)
{
    Transcoder *coder;
    bvec in, out;
    vec trans;
    double perc_corruption = 0.15;
    int corrupt_bits = 0;
    in = randb(320);

    coder = new Transcoder();

    coder->encode(in, trans);

    corrupt(trans, perc_corruption);

    coder->decode(trans, out);

    for(int i=0;i<in.size();i++) if ((in(i) ^ out(i)) != 0) corrupt_bits++;

    cout << perc_corruption << ',' << corrupt_bits << ',' << ((double)corrupt_bits)/out.size() << endl;

    return 0;
}

*/
