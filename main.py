import mido
import math



def midi_to_freq(note):
    """Converte numero nota MIDI in frequenza (Hz)"""
    return round(440 * (2 ** ((note - 69) / 12)), 2)

def extract_main_track(mid):
    """Trova la traccia principale (quella con più note uniche)"""
    best_track = None
    best_count = 0
    for track in mid.tracks:
        notes = [msg.note for msg in track if msg.type == 'note_on' and msg.velocity > 0]
        if len(notes) > best_count:
            best_count = len(notes)
            best_track = track
    return best_track

def convert_midi_to_arrays(file_path):
    mid = mido.MidiFile(file_path)
    track = extract_main_track(mid)
    print(f"[+] Traccia principale selezionata: {track.name if track.name else 'Senza nome'}")
    name = track.name if track.name else "Senza_nome"


    melody = []
    durations = []
    tempo = 500000  # default 120 BPM

    # estrai il tempo se definito
    for msg in mid.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
            break

    ticks_per_beat = mid.ticks_per_beat
    micros_per_tick = tempo / ticks_per_beat

    current_time = 0
    note_start_times = {}
    last_note_end = 0

    for msg in track:
        current_time += msg.time * micros_per_tick / 1e6  # secondi

        if msg.type == 'note_on' and msg.velocity > 0:
            # Se c'è una pausa tra l'ultima nota e questa, aggiungila
            if last_note_end and current_time > last_note_end:
                pause_duration = current_time - last_note_end
                melody.append(0)  # pausa
                durations.append(round(pause_duration * 1000))  # in ms

            note_start_times[msg.note] = current_time

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in note_start_times:
                start = note_start_times.pop(msg.note)
                duration = current_time - start
                melody.append(midi_to_freq(msg.note))
                durations.append(round(duration * 1000))
                last_note_end = current_time

    return melody, durations


def export_to_arduino_arrays(melody, durations, output_file=f"OUT.txt"):
    with open(output_file, "w") as f:
        f.write("float melody[] = {")
        f.write(", ".join(str(n) for n in melody))
        f.write("};\n\n")
        f.write("int durations[] = {")
        f.write(", ".join(str(d) for d in durations))
        f.write("};\n")
    print(f"[+] Esportato in '{output_file}' ({len(melody)} elementi totali, incluse pause)!")

if __name__ == "__main__":
    file_path = input("Trascina qui il file MIDI e premi invio: ").strip('"')
    melody, durations = convert_midi_to_arrays(file_path)
    export_to_arduino_arrays(melody, durations)
