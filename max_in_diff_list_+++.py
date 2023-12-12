from scipy.stats import norm
import numpy as np
import random

def normal(sig, K=4, height=64, min_mean_coverage=25):
    short = [sum(sig[i:i + K]) / K for i in range(0, len(sig), K)]
    top = max(2 * sum(short) / len(short), min_mean_coverage)
    return [min(height - 1, v * height / top) for v in short]

# Генератор сдвигов
new = open('shift_data.cov.tsv', 'r')

totalerr = 0
original = 0
counter = 0

size = 128
d = round(size/2)
# -1 чтобы размер вектора PDF совпал с размером вектора diffms
norm_pdf = [norm.pdf(x, 0, 25) for x in range(-d, d - 1)] 

# x = np.arrange(512)
for line in new:
    cols = line.replace('\n', '').split('\t')
    if len(cols) != 6: continue
    num, kind, side, sig, mod_sig, offset = cols
    sig = [int(v) for v in sig.split(',')]
    mod_sig = [int(v) for v in mod_sig.split(',')]
    mod_sig_sam = normal(mod_sig)
    mod_sig = mod_sig_sam

    # if (kind == 'Loss') and (side =='left'):
    #     plt.plot(x, mod_sig,label=str(side))
    #     plt.legend()
    if (kind == 'Loss') and side =='right':
        # print(mod_sig)
        diffms = np.diff(mod_sig)
        diffms = np.array([abs(x) for x in diffms])
        diffms = diffms * norm_pdf

        extr = list(diffms).index(max(diffms))  # положение экстремума
        extrpos = (len(mod_sig) / 2 - extr) # дальность экстремума от центра

        totalerr += abs(int(offset) - extrpos)
        original += abs(int(offset))
        counter += 1

print(totalerr / counter)
print(original / counter)
