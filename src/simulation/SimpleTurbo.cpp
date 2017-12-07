#include <cstdio>
#include <cstdlib>
#include <iostream>
#include "Transcoder.h"

using namespace std;
using namespace itpp;

int main()
{
    Transcoder *coder;
    bvec in, out;
    vec trans;
    
    in = randb(321);
 
    coder = new Transcoder();

    coder->encode(in, trans);

    for(int i=0;i<trans.size();i+=32)
    {
        if(trans(i) == -1) trans(i) = 1;
        else trans(i) = -1;
    }

    coder->decode(trans, out);


    for(int i=0;i<in.size();i++) cout << (in(i) ^ out(i));
    cout << endl;

    return 0;
}
