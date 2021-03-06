import argparse
import os
import re
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer


sentences = [
  # From July 8, 2017 New York Times:
  'Scientists at the CERN laboratory say they have discovered a new particle.',
  'There’s a way to measure the acute emotional intelligence that has never gone out of style.',
  'President Trump met with other leaders at the Group of 20 conference.',
  'The Senate\'s bill to repeal and replace the Affordable Care Act is now imperiled.',
  # From Google's Tacotron example page:
  'Generative adversarial network or variational auto-encoder.',
  'The buses aren\'t the problem, they actually provide a solution.',
  'Does the quick brown fox jump over the lazy dog?',
  'Talib Kweli confirmed to AllHipHop that he will be releasing an album in the next year.',
]
base_dir = os.getcwd()
log_dir  = 'LJlogs-tacotron'
checkpoint_file = 'model.ckpt-40000'
static_path = 'static'
audio_path = 'audio'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
hparams.parse('')
checkpoint = os.path.join(base_dir, log_dir, checkpoint_file)
print(checkpoint)
print(hparams_debug_string())
synth = Synthesizer()
synth.load(checkpoint)
checkpoint_1 = os.path.join(base_dir, 'LJlogs-tacotron', 'model.ckpt-40000')
checkpoint_2 = os.path.join(base_dir, 'california-12-logs', 'model.ckpt-112000')


def eval_text(text, voice_choice):
  file_path = 'output.wav'
  path = os.path.join(base_dir, static_path, audio_path, file_path)
  print('Synthesizing: %s' % path)
  print ('voice changed to  ', voice_choice) 
  if (voice_choice == 1) :
    synth.reload(checkpoint_1)
  else :
    synth.reload(checkpoint_2)

  with open(path, 'wb') as f:
    f.write(synth.synthesize(text))
  return file_path

def get_output_base_path(checkpoint_path):
  base_dir = os.path.dirname(checkpoint_path)
  m = re.compile(r'.*?\.ckpt\-([0-9]+)').match(checkpoint_path)
  name = 'eval-%d' % int(m.group(1)) if m else 'eval'
  return os.path.join(base_dir, name)

    

def run_eval(args):
  print(hparams_debug_string())
  synth = Synthesizer()
  synth.load(args.checkpoint)
  base_path = get_output_base_path(args.checkpoint)
  for i, text in enumerate(sentences):
    path = '%s-%d.wav' % (base_path, i)
    print('Synthesizing: %s' % path)
    with open(path, 'wb') as f:
      f.write(synth.synthesize(text))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Path to model checkpoint')
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.parse(args.hparams)
  run_eval(args)


if __name__ == '__main__':
  main()
