from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise

# 哒哒声（节拍器式短脉冲）
ticking = Sine(800).to_audio_segment(duration=50)  # 800Hz短脉冲
ticking = ticking.fade_out(100).append(AudioSegment.silent(duration=450))  # 间隔0.5秒
(ticking * 20).export("ticking.mp3", format="mp3")  # 生成20次循环

# 嗡嗡声（持续低频正弦波）
humming = Sine(120).to_audio_segment(duration=3000)  # 120Hz持续3秒
humming.export("humming.mp3", format="mp3")

# 吱吱声（高频脉冲+噪声）
squeak = Sine(3000).to_audio_segment(duration=100).fade_out(50)
squeak = squeak.overlay(WhiteNoise().to_audio_segment(duration=100))
(squeak.append(AudioSegment.silent(200)) * 15).export("squeaking.mp3", format="mp3")

# 咔嗒声（瞬态脉冲）
click = WhiteNoise().to_audio_segment(duration=500)  # 5ms白噪声
click = click.apply_gain(+200)  # 增强音量
(click.append(AudioSegment.silent(200)) * 30).export("clicking.mp3", format="mp3")