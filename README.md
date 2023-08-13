# IMPA
PyGame implementation of IMPA game from [TapTap](https://www.taptap.cn/app/171019).
The core game logic is implemented with C++ for effecient reinforcement learning.
![](assets/cover.webp)

# Prepare
The game is tested on Ubuntu20 and WSL.
```bash
sudo apt install pybind11-dev
pip3 install pygame
```
# Run IMPA!
Just run main.py with Python3. The C++ code will be compiled JIT.
```bash
python3 main.py
```

# Play Note
- Game Target: Just as the figure above. Make Red block minimal, Yellow block in middle and Blue block biggest.
- Click **Red Circle** to reset, **Yellow Circle** to next level (Only appears when target achieved).
- Diffculty: I use 14 hours to finish all 80 levels.
- The program will save your process automatically.
