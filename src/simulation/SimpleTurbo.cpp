#include <cstdio>
#include <cstdlib>
#include <iostream>
#include "Transcoder.h"

using namespace std;
using namespace itpp;

int main()
{
    bvec in, out;
    Transcoder *sender;

    sender = new Transcoder();
    in = randb(960);

    sender->encode(&in, 960, &out);
    sender->decode(&out, 960, &in);

    return 0;
}
