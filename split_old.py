from mido import MidiFile, MidiTrack, Message

def split_midi_by_channel(input_file):
    mid = MidiFile(input_file)
    channels = {}

    # Scandisce ogni traccia e ogni messaggio
    for track in mid.tracks:
        for msg in track:
            if msg.type in ["note_on", "note_off", "program_change"]:
                ch = msg.channel
                if ch not in channels:
                    channels[ch] = MidiFile()
                    channels[ch].tracks.append(MidiTrack())
                channels[ch].tracks[0].append(msg)

    # Salva un file per ogni canale trovato
    for ch, new_mid in channels.items():
        output_file = f"{input_file[:-4]}_channel_{ch}.mid"
        new_mid.save(output_file)
        print(f"[✓] Canale {ch} salvato in: {output_file}")

    print(f"[✔] Divisione completata — trovati {len(channels)} strumenti/canali")

# ESEMPIO D'USO

song = input("Inserisci il nome del file MIDI (con estensione .mid): ")

split_midi_by_channel(song)
