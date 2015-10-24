
import os
import shutil


base_dir = '/home/michael/Documents/Data/GlobalPhone/German'

adc_dir = os.path.join(base_dir, 'adc')

aln_dir = os.path.join(base_dir, 'aln', 'tri1_ali_fmllr')

data_dir = os.path.join(base_dir, 'phone_discovery')

speakers = os.listdir(adc_dir)

for s in speakers:
    if len(s) != 3:
        continue
    speaker_dir = os.path.join(adc_dir, s)
    data_speaker_dir = os.path.join(data_dir, s)
    os.makedirs(data_speaker_dir, exist_ok = True)
    files = os.listdir(speaker_dir)
    for f in files:
        if not f.endswith('.wav'):
            continue
        shutil.copy(os.path.join(speaker_dir, f), os.path.join(data_speaker_dir, f))

for f in os.listdir(aln_dir):
    s = f[2:5]
    data_speaker_dir = os.path.join(data_dir, s)
    shutil.copy(os.path.join(aln_dir, f), os.path.join(data_speaker_dir, f))
