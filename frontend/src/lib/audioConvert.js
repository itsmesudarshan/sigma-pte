// Converts a recorded audio Blob (whatever format MediaRecorder produced —
// typically webm/opus in Chrome/Edge) into a 16kHz mono WAV file, entirely
// client-side using the standard Web Audio API. This is the exact format
// Azure's Pronunciation Assessment API requires (WAV/PCM or OGG/Opus, both
// 16kHz mono) — converting here avoids needing any server-side audio
// library (ffmpeg etc.) on the backend.

const TARGET_SAMPLE_RATE = 16000;

export async function convertBlobToWav16kMono(blob) {
  const arrayBuffer = await blob.arrayBuffer();

  // Decode whatever format the browser recorded (webm/opus, etc.) into
  // raw PCM audio data.
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  const decodingContext = new AudioContextClass();
  const decodedBuffer = await decodingContext.decodeAudioData(arrayBuffer.slice(0));
  decodingContext.close?.();

  // Resample to 16kHz mono using an OfflineAudioContext, since Azure
  // requires this exact sample rate and channel count.
  const durationSeconds = decodedBuffer.duration;
  const offlineContext = new OfflineAudioContext(1, Math.ceil(durationSeconds * TARGET_SAMPLE_RATE), TARGET_SAMPLE_RATE);
  const source = offlineContext.createBufferSource();
  source.buffer = decodedBuffer;

  // Downmix to mono if the recording had multiple channels
  if (decodedBuffer.numberOfChannels > 1) {
    const merger = offlineContext.createChannelMerger(1);
    source.connect(merger);
    merger.connect(offlineContext.destination);
  } else {
    source.connect(offlineContext.destination);
  }

  source.start(0);
  const resampledBuffer = await offlineContext.startRendering();
  const pcmSamples = resampledBuffer.getChannelData(0);

  const wavArrayBuffer = encodePcmAsWav(pcmSamples, TARGET_SAMPLE_RATE);
  return wavArrayBuffer;
}

// Writes a standard 44-byte WAV header followed by 16-bit PCM samples.
// No external library needed — this format is simple enough to hand-write.
function encodePcmAsWav(float32Samples, sampleRate) {
  const numSamples = float32Samples.length;
  const bytesPerSample = 2; // 16-bit PCM
  const blockAlign = bytesPerSample; // mono
  const byteRate = sampleRate * blockAlign;
  const dataSize = numSamples * bytesPerSample;
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);

  function writeString(offset, str) {
    for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
  }

  writeString(0, 'RIFF');
  view.setUint32(4, 36 + dataSize, true);
  writeString(8, 'WAVE');
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true); // fmt chunk size
  view.setUint16(20, 1, true); // PCM format
  view.setUint16(22, 1, true); // mono
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, byteRate, true);
  view.setUint16(32, blockAlign, true);
  view.setUint16(34, 16, true); // bits per sample
  writeString(36, 'data');
  view.setUint32(40, dataSize, true);

  // Convert float32 samples (-1.0 to 1.0) to 16-bit PCM integers
  let offset = 44;
  for (let i = 0; i < numSamples; i++) {
    const clamped = Math.max(-1, Math.min(1, float32Samples[i]));
    const intSample = clamped < 0 ? clamped * 0x8000 : clamped * 0x7fff;
    view.setInt16(offset, intSample, true);
    offset += 2;
  }

  return buffer;
}

export function arrayBufferToBase64(arrayBuffer) {
  let binary = '';
  const bytes = new Uint8Array(arrayBuffer);
  const chunkSize = 0x8000; // avoid call-stack limits on very large arrays
  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
  }
  return btoa(binary);
}
