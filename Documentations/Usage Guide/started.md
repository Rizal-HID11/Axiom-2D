# Getting Started

## Requirements
- Python 3.7 or newer
- Terminal / Command Prompt 

## Running AXM Files Guide

- **1.** Open Terminal
- **2.** Navigate to Axiom 2D root folder `(or your root folder that has axiom 2D there)`
- **3** Make sure you not change the location of `axiom.py` file!
- **4.** Run this command:
```bash
python axiom.py
```
The program will automatically read `GAME_CONFIG.json` and execute the configured `.axm` file.

---

## Creating an AXM File Guide 

- **1.** Create a new file with `.axm` extension 
- **2.** Write your AXM Code inside 
- **3.** Update GAME_CONFIG.json:
```json
{
	"AXM_FILE_TO_RUN": "your-file.axm"
}
```
- **4.** Do the **Running AXM Files Guide** again to run your AXM file.

---

## Your First AXM File
Create `hello.axm`:
```axm
// THIS MAY NOT WORK IF YOU MODIFY THE GAME_CONFIG.json file!
SAYF "Player health: @player.health"
SAYF "Enemy health: @enemy.health"
@enemy DAMAGE 10
IF @enemy.health < 100
  SAY "Enemy attacked!"
```

run it. Output:
```text
[AXIOM] Player health: @player.health
[AXIOM] Enemy health: @enemy.health
[AXIOM] Enemy attacked!
```
**The output would be not 100% similar if you turn on the DEBUG mode.**
---

## Debug Mode

To see tokens and AST output, set `DEBUG` to `true` in `GAME_CONFIG.json`:
```json
{
	"DEBUG": true
}
```
This is useful for debugging problematic code.
