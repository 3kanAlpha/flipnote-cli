import os
import sys
import datetime

PPM_PALETTE = [
   0xFFFFFFFF, # 0x0 Not used / White
   0x525252FF, # 0x1 Dark Grey
   0xFFFFFFFF, # 0x2 White
   0x9C9C9CFF, # 0x3 Light Grey
   0xFF0000FF, # 0x4 Pure Red
   0x7F0000FF, # 0x5 Dark Red
   0xFF7F7FFF, # 0x6 Light Red / Pink
]

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

PREVIEW_WIDTH = 64
PREVIEW_HEIGHT = 48

TIMESTAMP_BASE = datetime.datetime(2000, 1, 1, 0, 0, 0)

class FlipnotePPM:
  def __init__(self, content_bytes):
    self.content_bytes = content_bytes
    # Ref: https://www.dsibrew.org/wiki/Flipnote_Files/PPM#File_Header
    self.anim_length = int.from_bytes(self.content_bytes[4:8], byteorder='little')
    self.audio_length = int.from_bytes(self.content_bytes[8:12], byteorder='little')
    self.frames = int.from_bytes(self.content_bytes[12:14], byteorder='little') + 1
    self.locked = (self.content_bytes[16] == 1)
    self.orig_author_name = self.content_bytes[20:42].decode('utf-16-le') # UCS-2
    self.author_name = self.content_bytes[42:64].decode('utf-16-le') # UCS-2
    self.user_name = self.content_bytes[64:86].decode('utf-16-le') # UCS-2
    self.orig_author_id = bytes_to_hexstr(self.content_bytes[86:86+8][::-1])
    self.edit_author_id = bytes_to_hexstr(self.content_bytes[94:94+8][::-1])
    self.flipnote_id = self.content_bytes[105:118].decode()
    timestamp = int.from_bytes(self.content_bytes[154:158], byteorder='little')
    self.timestamp = TIMESTAMP_BASE + datetime.timedelta(seconds=timestamp, hours=9)
    self.preview_bitmap = self.content_bytes[160:160+1536]
  
  def decode_preview(self):
    pass

def bytes_to_hexstr(b: bytes) -> str:
  return ''.join(f'{byte:02x}' for byte in b)

def main():
  file_path = 'examples/LEDA09_0AFC7CC402C15_030.ppm'
  
  with open(file_path, mode='rb') as reader:
    content = reader.read()
  
  ppm = FlipnotePPM(content)
  print('Size of animation data:', ppm.anim_length)
  print('Size of audio data:', ppm.audio_length)
  print('# of frames:', ppm.frames)
  print('is Locked:', ppm.locked)
  print('Author name:', ppm.orig_author_name)
  print('Author ID:', ppm.orig_author_id)
  print('ID:', ppm.flipnote_id)
  print('Timestamp:', ppm.timestamp)

if __name__ == '__main__':
  main()