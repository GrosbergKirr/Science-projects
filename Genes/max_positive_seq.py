import matplotlib.pyplot as plt
import numpy as np
import random

totalerr = 0
randtotal = 0
counter = 0
new = open('shift_data.cov.tsv', 'r')
for line in new:
    cols = line.replace('\n', '').split('\t')
    if len(cols) != 6: continue
    num, kind, side, sig, mod_sig, offset = cols
    sig = [int(v) for v in sig.split(',')]
    mod_sig = [int(v) for v in mod_sig.split(',')]

    def normal(sig1, K=4, height=64, min_mean_coverage=25):
        short = [sum(sig1[i:i + K]) / K for i in range(0, len(sig), K)]
        top = max(2 * sum(short) / len(short), min_mean_coverage)
        return [min(height - 1, round(v * height / top)) for v in short]
    mod_sig_sam = normal(mod_sig)
    if (kind == 'Loss') and (side == 'right'):
        diffms = np.diff(mod_sig)
        n = 0
        maks = 0
        for i in range(0, len(diffms)):
            if (diffms[i] > 0) or (diffms[i] == 0):
                n += 1
                if n > maks:
                    maks = n
                    ind = i
            else:
                n = 0
        extrpos = int(abs(len(mod_sig) / 2 - ind))  # дальность экстремума от центра
        totalerr += abs(int(offset) - extrpos)
        counter += 1
        ### Random number
        rand = int(random.normalvariate(-0, 25))
        randtotal += abs(rand - int(offset))
print(totalerr / counter)
print(randtotal / counter)