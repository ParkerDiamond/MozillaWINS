#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <itpp/comm/turbo.h>

using namespace std;
using namespace itpp;

class GenericTurbo
{
    public:
	Turbo_Codec codec;
	ivec generator, interleaver;
	int constraint;

	GenericTurbo()
	{
		generator = ivec(2);
		generator(0) = 013;
		generator(1) = 013;
		constraint = 4;
		interleaver = wcdma_turbo_interleaver_sequence(320);
		codec.set_parameters(generator, generator, constraint, interleaver);
	}
};


int main()
{
	GenericTurbo *codec;
	bvec input, encoded, decoded;

	codec = new GenericTurbo();
	input = randb(972-12); 

	for(int i=0;i<input.size();i++) cout << input(i);
	cout << endl;

	codec->codec.encode(input, encoded);
	codec->codec.decode(to_vec(encoded), decoded);

	cout << codec->codec.get_Ncoded() << endl;
	
	cout << endl;
	for(int i=0;i<decoded.size();i++) 
	{
		decoded(i) ^= 1;
		cout << decoded(i);
	}
	cout << endl;

	return 0;
}
