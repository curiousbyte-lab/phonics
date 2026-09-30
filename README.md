# Leo’s Sound Studio

An iPad-friendly phonics practice prototype. Enter an English word, hear the word, tap sound cards, and play a segmented blending demonstration.

## Run locally

No JavaScript dependencies or build step are required.

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. The dist folder can also be deployed to a static host. Hosting access rules belong to the host; the app does not implement authentication.

## Deploy to GitHub Pages

The GitHub Actions workflow publishes the contents of `dist/` whenever a commit is pushed to `main`.

1. Create a GitHub repository for this project. The repository can be public or private, subject to GitHub Pages availability for your account.
2. Make the initial commit, add the repository as this project's `origin`, then push the `main` branch:

   ```sh
   git add README.md requirements.txt scripts dist .github
   git commit -m "Prepare GitHub Pages deployment"
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main
   ```

3. In the repository, open **Settings → Pages** and set the build and deployment source to **GitHub Actions**.
4. Open the **Actions** tab and wait for **Deploy to GitHub Pages** to finish. The published URL appears in the workflow run and in **Settings → Pages**.

Subsequent pushes to `main` deploy automatically. To deploy without a new commit, run **Deploy to GitHub Pages** from the Actions tab using **Run workflow**.

## Contents

- dist/index.html, dist/style.css, dist/app.js: interface and playback.
- dist/dictionary.json: CMU pronunciation dictionary, including alternative pronunciations.
- dist/audio/: synthesized phoneme samples.
- dist/words/: synthesized MP3 audio for words with alternative pronunciations.
- scripts/generate_audio.py: audio generation script.

## Audio regeneration

```sh
python3 -m pip install -r requirements.txt
python3 scripts/generate_audio.py
```

The pre-generated dictionary and audio are included, so regeneration is optional.

## Prototype limitations

- American English dictionary pronunciations, without sentence context.
- Letter grouping uses rule matching and needs adult review. Unsupported alignments display phonetic symbols.
- Unknown words have no phoneme breakdown; browser word speech can still be attempted.
- Sounds are synthetic. Some consonants are short extracts from context words and need educational/audio review before using them as instructional models.
- Blending plays isolated clips with shorter gaps, then the word; it is not continuous human phonation.
- Browser speech and audio unlocking need verification on the target iPad.
- Inputs are processed in the page and are not uploaded by the app.

## Attribution

CMU Pronouncing Dictionary data is redistributed under dist/CMUDICT-LICENSE.txt; retain that notice. Audio was synthesized with eSpeak NG using espeakng-loader; those tools have their own third-party licenses. This repository does not bundle the synthesizer library.
