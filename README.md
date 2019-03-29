# reddit-dl
A program written in Python that downloads a given amount of *image* posts from a subreddit.
## Usage:
```
python reddit-dl.py <type> <subreddit> <time_range> <limit>
```
`type:`        One of (hot, new, rising, controversial, top). Due to API limitations a maximum of 1000 *top* posts can be downloaded.

`subreddit:`   The subreddit you want to download from.

`time_range:`  One of (hour, day, week, month, year, all).

`limit:`       Amount of posts to download.