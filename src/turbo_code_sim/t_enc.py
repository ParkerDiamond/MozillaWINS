import sys
import numpy
import commpy.channelcoding as comm

def print_trellis_info(trellis):
    print(trellis.number_states)
    print(trellis.number_inputs)
    print(trellis.next_state_table)
    print(trellis.output_table)

memory1 = numpy.array([2], dtype=int)
memory2 = numpy.array([2], dtype=int)
message = numpy.array([1,0], dtype=int)

gen1 = numpy.array([[05,07]], dtype=int)
gen2 = numpy.array([[13,15]], dtype=int)

t1 = comm.Trellis(memory1, gen1)
t2 = comm.Trellis(memory2, gen2)

inter = comm.RandInterlv(2,0)
t_enc = comm.turbo_encode(message, t1, t2, inter)
print(t_enc)

#def turbo_decode(sys_symbols, non_sys_symbols_1, non_sys_symbols_2, trellis,
#                 noise_variance, number_iterations, interleaver, L_int = None):


t_dec = comm.turbo_decode(t_enc[0],t_enc[1],t_enc[2], t1, 0.1, 1, inter)
print(t_dec)
