
import os
import pickle

data_dir = '/home/michael/Documents/Data/GlobalPhone/German/phone_discovery/005'
temp_dir = '/home/michael/Documents/Data/temp/segalign'
temp_textgrid_dir = os.path.join(temp_dir, 'tg')
temp_mfcc_dir = os.path.join(temp_dir, 'mfcc')
temp_mean_dir = os.path.join(temp_dir, 'means')
temp_align_dir = os.path.join(temp_dir, 'ali')
temp_wav_dir = os.path.join(temp_dir, 'wav')

os.makedirs(temp_dir, exist_ok = True)
os.makedirs(temp_textgrid_dir, exist_ok = True)
os.makedirs(temp_mfcc_dir, exist_ok = True)
os.makedirs(temp_mean_dir, exist_ok = True)
os.makedirs(temp_align_dir, exist_ok = True)
os.makedirs(temp_wav_dir, exist_ok = True)

from acousticsim.utils import extract_audio

from acousticsim.representations.mfcc import Mfcc

from textgrid import TextGrid, IntervalTier

padding = 0

def norm(value, min, max):
    return (value - min)/(max - min)

def unnorm(norm_value, min, max):
    return norm_value * (max - min) + min

seg_ind = 0
for f in sorted(os.listdir(data_dir)):
    if not f.endswith('.TextGrid'):
        continue
    print(f)
    wav_file = f.replace('.TextGrid', '.adc.wav')
    textgrid_path = os.path.join(data_dir, f)
    wav_path = os.path.join(data_dir, wav_file)
    tg = TextGrid()
    tg.read(textgrid_path)

    word_tier = tg.getFirst('words')

    segmentation_tier = IntervalTier('segments', 0, word_tier.maxTime)
    durations = []
    for interval in word_tier:
        if interval.mark == '':
            continue
        durations.append(interval.maxTime - interval.minTime)
    max_duration = max(durations)
    min_duration = min(durations)

    min_thresh = 0.01
    max_thresh = 0.05
    segs = []

    for interval in word_tier:
        if interval.mark == '':
            continue
        print(interval.mark, interval.minTime, interval.maxTime)
        outpath = os.path.join(temp_wav_dir, interval.mark + '.wav')
        extract_audio(wav_path, outpath, interval.minTime, interval.maxTime, padding = padding)
        rep = Mfcc(outpath, freq_lims = (80, 7800), num_coeffs = 12, win_len = 0.025, time_step = 0.01)
        rep.is_windowed = True
        duration = interval.maxTime - interval.minTime
        thresh = unnorm(norm(duration, min_duration, max_duration), min_thresh, max_thresh)
        rep.segment(threshold = thresh)
        print(sorted(rep._segments.keys()))
        padded_begin = interval.minTime - padding
        if padded_begin < 0:
            padded_begin = 0
        for k in sorted(rep._segments.keys()):
            with open(os.path.join(temp_mfcc_dir, '{}.mfcc'.format(seg_ind)), 'wb') as fh:
                pickle.dump(rep[k[0],k[1]], fh)
            with open(os.path.join(temp_mean_dir, '{}.mean'.format(seg_ind)), 'wb') as fh:
                pickle.dump(rep._segments[k], fh)
            segs.append(str(seg_ind))
            seg_ind += 1
            begin = round(k[0] + padded_begin, 3)

            end = round(k[1] + padded_begin,3)
            print(begin, end)
            segmentation_tier.add(begin, end, '{}'.format(seg_ind))
    with open(os.path.join(temp_align_dir, '{}.seg'.format(f)), 'w') as fa:
        fa.write(' '.join(segs))
    tg.append(segmentation_tier)
    tg.write(textgrid_path.replace(data_dir, temp_textgrid_dir))
