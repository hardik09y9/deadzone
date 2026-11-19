# DEADZONE — Nightmare Protocol

Browser-playable top-down zombie survival shooter, packaged as a Python Streamlit app.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Create an app from your repository, branch `main`, main file `app.py`.
4. Deploy. Streamlit provides a public URL.

## Controls
- WASD / arrow keys: move
- Mouse: aim
- Hold mouse button: shoot
- R: reload
- Shift: dash
- E: open/close field shop
- Click an upgrade in the shop to purchase it

Nightmare mode is fixed: enemies move quickly, hit hard, and scale with each wave. An Alpha boss spawns every fifth wave. Credits from kills can buy medkits, damage, ammo, magazine capacity and max health.
