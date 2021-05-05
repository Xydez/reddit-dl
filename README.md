# reddit-dl
A program written in Python that downloads a given amount of *image* posts from a subreddit.

This was created during a time when memes were going to get banned from the internet forever due to [Article 13](https://en.wikipedia.org/wiki/Directive_on_Copyright_in_the_Digital_Single_Market#Draft_Article_13_(Directive_Article_17)) of the Directive on Copyright in the Digital Single Market created by the EU. Fortunately, they did not get banned and the stashing of gigabytes of memes was in vain. However, this repository still remains as a testament to those who sacrificed their hard drive space in order to freeze in time a loved era of popular culture that would soon vanish for all eternity.

## Usage:
```
python reddit-dl.py <type> <subreddit> <time_range> <limit>
```
`type:`        One of (hot, new, rising, controversial, top). Due to API limitations a maximum of 1000 *top* posts can be downloaded.

`subreddit:`   The subreddit you want to download from.

`time_range:`  One of (hour, day, week, month, year, all).

`limit:`       Amount of posts to download.
