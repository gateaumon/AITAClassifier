# AITAClassifier

This is a personal project using Pytorch neural nets to train a classifier to
predict the judgement of submissions to the subreddit 
[r/AmItheAsshole](https://www.reddit.com/r/AmItheAsshole/).

In r/AmItheAsshole users submit interpersonal conflicts they have and ask other
users to judge whether they were the "asshole" in the situation. Posts are given
a flair with one of four judgements 18 hours after the post was submitted:

* Asshole
* Not the asshole
* Everyone sucks
* No assholes

Users put forth their judgements by leaving a comment on the post with an 
according code: 

* YTA (you're the asshole)
* NTA (not the asshole)
* ESH (everyone sucks here)
* NAH (no assholes here)

The winning  judgement is the top comment (meaning it has the most votes) after 
18 hours.

For this project I train a bidirectional neural net on the submission text and
corresponding judgement to try to predict the judgement on new submissions. I 
used Google Colab and Pytorch for the development of my neural net architecture.
