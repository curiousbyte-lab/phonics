import ctypes as c,espeakng_loader as e,wave,pathlib
lib=c.CDLL(e.get_library_path())
lib.espeak_Initialize.argtypes=[c.c_int,c.c_int,c.c_char_p,c.c_int]
rate=lib.espeak_Initialize(2,0,str(e.get_data_path()).encode(),0)
CALL=c.CFUNCTYPE(c.c_int,c.POINTER(c.c_short),c.c_int,c.c_void_p)
chunks=[]
@CALL
def callback(p,n,event):
 if p and n: chunks.append(c.string_at(p,n*2))
 return 0
lib.espeak_SetSynthCallback(callback)
lib.espeak_SetVoiceByName(b'en-us')
lib.espeak_SetParameter(1,135,0)
lib.espeak_Synth.argtypes=[c.c_void_p,c.c_size_t,c.c_uint,c.c_int,c.c_uint,c.c_uint,c.c_void_p,c.c_void_p]
phon={'AA':'A:','AE':'a','AH':'V','AO':'O:','AW':'aU','AY':'aI','B':'b','CH':'tS','D':'d','DH':'D','EH':'E','ER':'3:','EY':'eI','F':'f','G':'g','HH':'h','IH':'I','IY':'i:','JH':'dZ','K':'k','L':'l','M':'m','N':'n','NG':'N','OW':'oU','OY':'OI','P':'p','R':'r\u02d0','S':'s','SH':'S','T':'t','TH':'T','UH':'U','UW':'u:','V':'v','W':'w','Y':'j','Z':'z','ZH':'Z','AX':'@'}
p=pathlib.Path(str(pathlib.Path(__file__).resolve().parents[1]/'dist/audio'));p.mkdir(exist_ok=True)
for code,sound in phon.items():
 chunks.clear(); sound = sound + ':' if code in ['M','N','NG','L','F','S','SH','TH','DH','V','Z','ZH'] else sound; text=('[[ '+sound+' ]]').encode();buf=c.create_string_buffer(text)
 result=lib.espeak_Synth(buf,len(text)+1,0,1,0,1|0x100, None,None)
 lib.espeak_Synchronize()
 with wave.open(str(p/(code+'.wav')),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(chunks))
 print(code,sum(map(len,chunks)))
# Context is needed for sonorants that the synthesizer suppresses in isolation.
for code,text in [('R','red'),('M','moo'),('N','noon'),('L','loo'),('NG','[[ NI ]]')]:
 chunks.clear();raw=text.encode();buf=c.create_string_buffer(raw);lib.espeak_Synth(buf,len(raw)+1,0,1,0,1|(0x100 if text.startswith('[[') else 0),None,None);lib.espeak_Synchronize()
 pcm=b''.join(chunks)[:int(rate*.09)*2]
 with wave.open(str(p/(code+'.wav')),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(pcm)
import cmudict,re,json
arp={'AA':'A:','AE':'a','AH':'V','AO':'O:','AW':'aU','AY':'aI','B':'b','CH':'tS','D':'d','DH':'D','EH':'E','ER':'3:','EY':'eI','F':'f','G':'g','HH':'h','IH':'I','IY':'i:','JH':'dZ','K':'k','L':'l','M':'m','N':'n','NG':'N','OW':'oU','OY':'OI','P':'p','R':'r','S':'s','SH':'S','T':'t','TH':'T','UH':'U','UW':'u:','V':'v','W':'w','Y':'j','Z':'z','ZH':'Z'}
whole=pathlib.Path(str(pathlib.Path(__file__).resolve().parents[1]/'dist/words'));whole.mkdir(exist_ok=True)
index={}
for word,variants in cmudict.dict().items():
 if not word.isalpha() or len(variants)<2:continue
 index[word]=len(variants)
 for i,ps in enumerate(variants):
  sounds=[]
  for ph in ps:
   base=re.sub('[012]','',ph);sound='@' if ph=='AH0' else arp[base]
   if '1' in ph:sound="'"+sound
   sounds.append(sound)
  raw=('[[ '+''.join(sounds)+' ]]').encode();chunks.clear();buf=c.create_string_buffer(raw);lib.espeak_Synth(buf,len(raw)+1,0,1,0,1|0x100,None,None);lib.espeak_Synchronize()
  wav=whole/(word+'-'+str(i)+'.wav')
  with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(chunks))
(whole/'index.json').write_text(json.dumps(index))
print('Multi-pronunciation audio words',len(index))

import lameenc
for file in whole.glob('*.wav'):
 with wave.open(str(file)) as w:
  rate=w.getframerate();pcm=w.readframes(w.getnframes())
 encoder=lameenc.Encoder();encoder.set_bit_rate(32);encoder.set_in_sample_rate(rate);encoder.set_channels(1);encoder.set_quality(5)
 file.with_suffix('.mp3').write_bytes(encoder.encode(pcm)+encoder.flush());file.unlink()
