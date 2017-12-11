import matplotlib.pyplot as plt
import pandas
import sys

def graph(data):
    mat = data.as_matrix()

    plt.suptitle("Turbo Code Error Rates for Additive White Gaussian Noise (AWGN)")
    plt.subplot(211)
    plt.plot(mat[:,2], mat[:,0], '-', linewidth=5)
    plt.title("Noise Spectral Density vs Bit Error Rate (BER)")
    plt.xlabel("Noise (W/Hz)")
    plt.ylabel("BER")

    plt.subplot(212)
    plt.plot(mat[:,2], mat[:,1], 'r-', linewidth=5)
    plt.title("Noise Spectral Density vs Frame Error Rate (FER)")
    plt.xlabel("Noise (W/Hz)")
    plt.ylabel("FER")

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.savefig('noise_v_error.png')

def parse_csv(dataFile):
    with open(dataFile, 'rb') as f:
        data = pandas.read_csv(f)
    return data

if __name__ == "__main__":
    data = parse_csv(sys.argv[1])
    graph(data)
