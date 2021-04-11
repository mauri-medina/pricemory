import argparse
import os
from datetime import datetime

from scrapy import spiderloader
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging

"""
Script to run all the project spiders

By default spiders are run sequentially, one after another, but other options are available.
To select how to run spiders pass the -t argument with the desire type

Crawler output file is set in script, 
by default it is located in the same path as the script and named as log
"""


def sequentially_run():
    """
    Run all project spider sequentially, one after another.
    """
    runner = CrawlerRunner(settings=settings)

    @defer.inlineCallbacks
    def crawl():
        for spider_name in spider_loader.list():
            spider = spider_loader.load(spider_name)
            yield runner.crawl(spider)

        reactor.stop()

    crawl()
    reactor.run()


def parallel_run():
    """
    Run all spiders in parallel, all at the same time.
    """
    process = CrawlerProcess(settings)
    for spider_name in spider_loader.list():
        process.crawl(spider_name)

    process.start()


parser = argparse.ArgumentParser(description='Run all defined spiders')
parser.add_argument('-t', '--type', type=str, required=False, default='sequentially', help='crawler run type')
args = parser.parse_args()

if __name__ == '__main__':

    logs_dir = 'log'
    logs_file = 'crawler_' + args.type + '_runner_' + datetime.now().strftime("%d-%m-%Y-%H_%M_%S") + '.log'

    try:
        os.makedirs(logs_dir)
    except FileExistsError:
        # directory already exists
        pass

    settings = get_project_settings()
    settings.set('LOG_FILE', os.path.join('.', logs_dir, logs_file))
    configure_logging(settings=settings)

    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    if args.type == 'sequentially':
        sequentially_run()
    elif args.type == 'parallel':
        parallel_run()
