# edge-asset/img

Put the site photos here as `{Unsplash photo ID}.jpg`. When a file exists, every page
loads it first and only falls back to Unsplash if it is missing.

Pushing files to this folder (including uploads through the GitHub web UI) runs the
`edge-asset photos` workflow, which resizes the photos and rebuilds the pages.

| File name | Download page |
|---|---|
| GpJ9p1QH7O4.jpg | https://unsplash.com/photos/GpJ9p1QH7O4 |
| q1tyQip5AQQ.jpg | https://unsplash.com/photos/q1tyQip5AQQ |
| a8A-z_ZPEC0.jpg | https://unsplash.com/photos/a8A-z_ZPEC0 |
| rD28m9BmXVs.jpg | https://unsplash.com/photos/rD28m9BmXVs |
| Q6sCJFHCubc.jpg | https://unsplash.com/photos/Q6sCJFHCubc |
| -MVSfkR4xz4.jpg | https://unsplash.com/photos/-MVSfkR4xz4 |
| TJ4CndIc9z8.jpg | https://unsplash.com/photos/TJ4CndIc9z8 |
| pcYN7Pi8_BQ.jpg | https://unsplash.com/photos/pcYN7Pi8_BQ |
| 4UVtFIfK1eo.jpg | https://unsplash.com/photos/4UVtFIfK1eo |
| 4mEyvORkbN0.jpg | https://unsplash.com/photos/4mEyvORkbN0 |

`fetch_photos.sh` downloads them in one go from any machine that can reach unsplash.com
(Unsplash refuses GitHub's servers, so the workflow cannot download them itself).
