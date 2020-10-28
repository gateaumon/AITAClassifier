import sys
from itertools import islice
import praw
import csv
import time
import datetime

# fields that I would like to collect for each submission
COL_LABELS = ['id', 'author', 'created_utc', 'num_comments', 'over_18', 'selftext', 'title', 'link_flair_text']


def process_file(filepath):
    """
    Reads Reddit submission IDs from file and creates a .csv file with submission
    data and metadata.
    :param filepath: path to file with submission IDs
    """
    # instantiate reddit
    reddit = praw.Reddit(client_id='<ID>',
                         client_secret='<SECRET>',
                         user_agent='<USERNAME>',
                         ratelimit_seconds='600')
    flairs = set()
    with open(filepath, 'r') as id_file, open('reddit_raw.csv', 'a') as reddit_csv:
        start = time.time()
        print('Processing started...')
        csv_writer = csv.writer(reddit_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(COL_LABELS)
        num_lines = 0
        while True:
            next_10_lines = list(islice(id_file, 10))
            if not next_10_lines:
                break
            # make submission IDs full IDs if not already
            ids = [i.strip() if i.startswith('t3_') else f't3_{i.strip()}' for i in next_10_lines]
            submissions = reddit.info(ids)
            for submission in submissions:
                num_lines += 1
                if validate_submission(submission):
                    flairs.add(submission.link_flair_text)
                    csv_writer.writerow([submission.id,
                                         submission.author,
                                         submission.created_utc,
                                         submission.num_comments,
                                         submission.over_18,
                                         submission.selftext,
                                         submission.title,
                                         submission.link_flair_text])
            end = time.time()
            print(f'{num_lines} files processed, {datetime.timedelta(seconds = int(round(end - start)))}')
    print('Processing finished.')
    print(f'Flairs found: {flairs}')
    with open('flairs.txt', 'w') as flair_file:
        for flair in flairs:
            flair_file.write(flair)
            flair_file.write('\n')


def validate_submission(submission):
    """
    Determines whether a submission has a value for all relevant fields
    :param submission: submission to check
    :return: whether the submission has an appropriate value for all relevant fields
    """
    return (submission.author and
            submission.created_utc and
            submission.link_flair_text and
            submission.num_comments and
            submission.over_18 is not None and
            submission.selftext != '[removed]' and
            submission.selftext is not None and
            submission.title)


def main():
    try:
        filepath = sys.argv[1]
    except IndexError:
        sys.stderr.write("Provide the path to the file with submission IDs.")
        sys.exit(1)
    process_file(filepath)


if __name__ == '__main__':
    main()
