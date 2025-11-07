from mido import MidiFile, MidiTrack, Message

def cut_midi(input_file, output_file, fraction=1/1.1):
    # Carica il file MIDI
    mid = MidiFile(input_file)
    new_mid = MidiFile()

    # Calcola il limite in tick (1/3 della durata totale)
    total_ticks = max(sum(msg.time for msg in track) for track in mid.tracks)
    cutoff = total_ticks * fraction

    for track in mid.tracks:
        new_track = MidiTrack()
        elapsed = 0

        for msg in track:
            if elapsed + msg.time > cutoff:
                # Taglia il messaggio che sfora il limite
                msg = msg.copy(time=int(cutoff - elapsed))
                new_track.append(msg)
                break
            new_track.append(msg)
            elapsed += msg.time

        new_mid.tracks.append(new_track)

    # Salva il nuovo file MIDI tagliato
    new_mid.save(output_file)
    print(f"File MIDI tagliato salvato come: {output_file}")


name = input("Inserisci il nome del file MIDI da tagliare (con estensione .mid): ")

# ESEMPIO D’USO
cut_midi(name, "output_cut.mid", fraction=1/1.1)
