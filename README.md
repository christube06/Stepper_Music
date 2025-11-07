# Stepper_Music
A code that convert midi file to be played in stepper motor


First you choose a midi file to be splitted in different channels using the "split.py" script.
You shouldn't put the original midi file in the "main.py" script because it can have different instrument that a single stepper can't play

After you choose the correct channel run the main script and put the midi file that have the melody.

The output is a OUT.txt file that have the "float melody []" and the "int duration []" list

You should put thoose in the .ino file instead of the default ones


RUNNING

Install dependency

```Sheel
pip install mido
```

Run the splitter

```Sheel
python split.py
```
Then you put the original midi file to split

OR if you don't want to preserve the timings run:
```Sheel
python split_old.py
```


Then when you chose the channel you want to play run:
```Sheel
python main.py
```

and put the extracted channel

when you have the output in the OUT.txt file you just copy and paste this in the ino file overwriting the default lists

And That's it.
Have fun playng music whit stepper
