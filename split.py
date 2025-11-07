from mido import MidiFile, MidiTrack, Message, MetaMessage

def extract_channel_with_timing(input_file, channel):
    mid = MidiFile(input_file)
    new_mid = MidiFile()
    new_track = MidiTrack()
    new_mid.tracks.append(new_track)

    for track in mid.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time

            # Copia anche i messaggi meta (tempo, chiave, ecc.)
            if msg.is_meta:
                new_track.append(msg)
                continue

            # Copia solo note appartenenti al canale scelto
            if hasattr(msg, "channel") and msg.channel == channel:
                msg = msg.copy(time=current_time)
                new_track.append(msg)
                current_time = 0  # reset del tempo accumulato

    output_file = f"{input_file[:-4]}_channel_{channel}_timed.mid"
    new_mid.save(output_file)
    print(f"File salvato: {output_file}")

# ESEMPIO D'USO
song = input("Inserisci il nome del file MIDI (con estensione .mid): ")


extract_channel_with_timing(song, channel=3)
